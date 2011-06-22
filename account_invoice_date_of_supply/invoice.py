# -*- coding: utf-8 -*-

from osv import osv, fields

class invoiceline(osv.osv):
    _name = "account.invoice.line"
    _inherit = _name
    
    _columns = {
        'dateofsupply': fields.date("Date of Supply", help="Date of Supply or Service Rendered as required by some tax laws if not the same as the invoice date."),
    }
        
invoiceline()
