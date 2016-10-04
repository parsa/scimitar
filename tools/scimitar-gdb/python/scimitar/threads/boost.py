# -*- coding: utf-8 -*-
#
# Scimitar: Ye Distributed Debugger
# 
# Copyright (c) 2016 Parsa Amini
# Copyright (c) 2016 Hartmut Kaiser
# Copyright (c) 2016 Thomas Heller
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#
import gdb


class Unordered(object):
    '''Common representation of Boost.Unordered types in Boost 1.52.'''

    def __init__(self, value, extractor):
        self.value = value
        self.extractor = extractor
        self.node_type = None
        self.value_type = None
        self.extra_node = False
        self._init_types()

    def __len__(self):
        if self.value['_M_buckets']:
            return int(self.value['_M_element_count'])
        else:
            return 0

    def __iter__(self):
        buckets = self.value['_M_buckets']
        if buckets:
            start_bucket = buckets + self.value['_M_bucket_count']
            start_node = start_bucket.dereference()['_M_nxt']
            if self.extra_node:
                start_node = start_node.dereference()['_M_nxt']
            return self._iterator(
                start_node, self.node_type, self.value_type, self.extractor
            )
        else:
            return iter([])

    def empty(self):
        return not self.value['table_']['buckets_']

    def _init_types(self):
        key_type = self.value.type.template_argument(0)
        value_type = self.value.type.template_argument(1)
        self.value_type = self.extractor.make_type(key_type, value_type)

        table = self.value['table_'].type.fields()[0]
        assert table.is_base_class
        allocators = table.type['allocators_']
        assert allocators

        self.node_type = allocators.type.template_argument(
            1
        ).template_argument(0)
        bucket_type = allocators.type.template_argument(0).template_argument(
            0
        ).strip_typedefs()

        self.extra_node = (
            str(bucket_type) == 'boost::unordered::detail::bucket'
        )

    class _iterator(object):
        '''Iterator for Boost.Unordered types'''

        def __init__(self, start_node, node_type, value_type, extractor):
            #assert start_node
            self.node = None
            self.next_node = start_node
            self.node_type = node_type
            self.value_type = value_type
            self.extractor = extractor

        def __iter__(self):
            return self

        def next(self):
            # sorry, no next node available
            if not self.next_node or self.next_node == self.node:
                raise StopIteration()

            # fetch next node
            self.node = self.next_node
            self.next_node = self.node.dereference()['next_']

            mapped = self._value()
            return (self.extractor.key(mapped), self.extractor.value(mapped))

        def _value(self):
            assert self.node
            node = self.node.dereference().cast(self.node_type)
            return node['value_base_']['data_'].cast(self.value_type)


class Map(Unordered):

    def __init__(self, value):
        super(Map, self).__init__(value, self._extractor())

    class _extractor(object):

        def key(self, node):
            return node['first']

        def value(self, node):
            return node['second']

        def make_type(self, key, value):
            return gdb.lookup_type('std::pair<%s, %s>' % (key.const(), value))


class Set(Unordered):

    def __init__(self, value):
        super(Set, self).__init__(value, self._extractor())

    class _extractor(object):

        def key(self, node):
            return None

        def value(self, node):
            return node

        def make_type(self, key, value):
            return key

# vim: :ai:sw=4:ts=4:sts=4:et:ft=python:fo=corqj2:sm:tw=79:
