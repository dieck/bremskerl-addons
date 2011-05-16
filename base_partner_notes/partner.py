
from osv import osv, fields

class base_partner_notes(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'note_sale': fields.text("Note for Sale Orders"),
        'note_purchase': fields.text("Note for Purchase Orders"),
        'note_invoice': fields.text("Note for Invoices"),
        'note_delivery': fields.text("Note for Delivery Orders"),
    }
            
base_partner_notes()
