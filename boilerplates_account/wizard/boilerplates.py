# -*- encoding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard(osv.osv_memory):
    _name = "boilerplate.wizard.account.invoice"
    _inherit = "boilerplate.wizard"

    remote_name = _("Invoice")
    remote_model = "account.invoice"
    remote_note = "comment"
    remote_product_id = False
    remote_partner_id = "partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard()

