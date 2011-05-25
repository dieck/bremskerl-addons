# -*- encoding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard(osv.osv_memory):
    _name = "boilerplate.wizard.purchase.order"
    _inherit = "boilerplate.wizard"

    remote_name = _("Purchases Order")
    remote_model = "purchase.order"
    remote_note = "notes"
    remote_product_id = False
    remote_partner_id = "partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard()

class boilerplate_wizard_lines(osv.osv_memory):
    _name = "boilerplate.wizard.purchase.order.line"
    _inherit = "boilerplate.wizard"

    remote_name = _("Purchases Order Line")
    remote_model = "purchase.order.line"
    remote_note = "notes"
    remote_product_id = "product_id"
    remote_partner_id = "partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard_lines()

