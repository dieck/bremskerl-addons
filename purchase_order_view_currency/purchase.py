# -*- encoding: utf-8 -*-

from osv import fields
from osv import osv

#
# Model definition
#
class purchase_order_view_currency_purchase_order(osv.osv):
    _name = "purchase.order"
    _inherit = "purchase.order"

    def _get_currency(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for order in self.browse(cr, uid, ids):
            res[order.id] = order.pricelist_id.currency_id.code
        return res
    
    _columns = {
        'currency_code': fields.function(_get_currency, method=True, string='Currency', type='char'),
    }
purchase_order_view_currency_purchase_order()

