# -*- encoding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard(osv.osv_memory):
    _name = "boilerplate.wizard.stock.picking"
    _inherit = "boilerplate.wizard"

    remote_name = _("Stock Picking")
    remote_model = "stock.picking"
    remote_note = "note"
    remote_product_id = False
    remote_partner_id = "partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard()
