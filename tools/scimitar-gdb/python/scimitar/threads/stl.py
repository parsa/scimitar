import gdb
import itertools
from itertools import imap, izip


def find_type(orig, name):
    typ = orig.strip_typedefs()
    while True:
        search = str(typ) + '::' + name
        try:
            return gdb.lookup_type(search)
        except RuntimeError:
            pass
        # The type was not found, so try the superclass.  We only need
        # to check the first superclass, so we don't bother with
        # anything fancier here.
        field = typ.fields()[0]
        if not field.is_base_class:
            raise ValueError("Cannot find type %s::%s" % (str(orig), name))
        typ = field.type


class Iterator:

    def next(self):
        return self.__next__()


def format_count(i):
    return '[%d]' % i


class StdHashtableIterator(Iterator):

    def __init__(self, hash_):
        self.node = hash_['_M_before_begin']['_M_nxt']
        self.node_type = find_type(
            hash_.type.target().target(), '__node_type'
        ).pointer()

    def __iter__(self):
        return self

    def __next__(self):
        if self.node == 0:
            raise StopIteration
        elt = self.node.cast(self.node_type).dereference()
        self.node = elt['_M_nxt']
        val = elt['_M_storage']
        val = val.cast(elt.type.template_argument(0))
        return val


class StdUnorderedSet:

    def __init__(self, val):
        self.val = val

    def hashtable(self):
        return self.val['_M_h']

    def __len__(self):
        return int(self.hashtable()['_M_element_count'])

    def __iter__(self):
        counter = imap(format_count, itertools.count())
        return izip(counter, StdHashtableIterator(self.hashtable()))


class UnorderedMapPrinter:

    def __init__(self, val):
        self.val = val

    def hashtable(self):
        return self.val['_M_h']

    def __len__(self):
        return int(self.hashtable()['_M_element_count'])

    @staticmethod
    def flatten(list):
        for elt in list:
            for i in elt:
                yield i

    @staticmethod
    def format_one(elt):
        return (elt['first'], elt['second'])

    def children(self):
        counter = imap(format_count, itertools.count())
        # Map over the hash table and flatten the result.
        data = self.flatten(
            imap(self.format_one, StdHashtableIterator(self.hashtable()))
        )
        # Zip the two iterators together.
        return izip(counter, data)

    def display_hint(self):
        return 'map'
