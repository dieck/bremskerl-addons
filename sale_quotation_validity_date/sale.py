
from osv import osv, fields

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = _name
    
    _columns = {
        'quotation_validity': fields.date("Quotation validity", help="Date until which the quotation is regarded valid.",
                                          readonly=True, states={'draft': [('readonly', False)]}),
    }
            
sale_order()
