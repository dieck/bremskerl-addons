# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = _name
        
    def _check_clientorderref_and_partnerid(self, cr, uid, ids):
        for o in self.browse(cr, uid, ids):
            res = self.search(cr, uid, [ ('client_order_ref','=',o.client_order_ref),
                                         ('partner_id','=',o.partner_id.id)
                                       ])
            # Result may contain the current order if it's active: we remove it here.
            if o.id in res:
                res.remove(o.id)
            if len(res):
                # If we have any results left
                # we have duplicate entries
                return False
        return True
    
    _constraints = [(_check_clientorderref_and_partnerid,
                    _('Client order ref has to be unique per partner.'),
                    ['client_order_ref','partner_id'])
                   ]
  
    _sql_constraints = [ ('clorref_prt_uniq', 'unique (client_order_ref, partner_id)', """Client order ref has to be unique per partner."""), ]

    def copy(self, cr, uid, id, default=None, context=None):
        if context is None:
            context={}

        if not default:
            default = {}
        if 'client_order_ref' not in default:
            default = default.copy()
            product = self.read(cr, uid, id, ['client_order_ref'], context=context)
            default['client_order_ref'] = product['client_order_ref'] + _(' (copy)')

        return super(sale_order, self).copy(cr=cr, uid=uid, id=id, default=default, context=context)
        
sale_order()
