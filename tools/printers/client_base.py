import gdb
import re
import sys
import datetime
import ctypes

class ClientBasePrinter(object):
    def __init__(self, expr, val):
        self.val = val
        self.expr = expr
        self.Ppx = val['shared_state_']['px']
        self.px = self.Ppx.dereference()

    def display_hint(self):
        return self.expr

    def to_string(self):
        state_ = None
        if self.Ppx:
            state_ = str(self.px['state_'])
                
        return "(%s) {{ %s }} %#02x" % (self.expr, state_, self.val.address)

    def children(self):
        result = [] 
        if self.Ppx:
            state_ = int(self.px['state_'])
            if state_ == 3:
                P_type = gdb.lookup_type('hpx::naming::id_type').pointer()
                result.extend([
                    ('value', self.px.dereference()['storage_']['data_']['buf'].cast(P_type).dereference()),
                ])
            elif state_ == 5:
                P_type = gdb.lookup_type('boost::exception_ptr').pointer()
                result.extend([
                    ('exception', self.px.dereference()['storage_']['data_']['buf'].cast(P_type).dereference()),
                ])
            else:
                result.extend([
                    ('count', self.px.dereference()['count_']),
                ])
                
        return result

def lookup_type(val):
    type_ = val.type

    if type_.code == gdb.TYPE_CODE_PTR:
        type_ = type.dereference()

    type_ = type_.unqualified().strip_typedefs()

    expr = str(type_)
    m = re.match('^(const )?hpx::components::client_base<(.*)>( \*)?( const)?$', expr)
    if m:
        return ClientBasePrinter(expr, val)
    return None

gdb.pretty_printers.append(lookup_type)

