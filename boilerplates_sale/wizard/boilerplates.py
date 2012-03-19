# -*- encoding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard_line(osv.osv_memory):
    _name = "boilerplate.wizard.sale.order.line"
    _inherit = "boilerplate.wizard"

    remote_name = _("Sale Order Line")
    remote_model = "sale.order.line"
    remote_note = "notes"
    remote_product_id = "product_id"
    remote_partner_id = "order_partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard_line()


class boilerplate_wizard_order(osv.osv_memory):
    _name = "boilerplate.wizard.sale.order"
    _inherit = "boilerplate.wizard"

    remote_name = _("Sale Order")
    remote_model = "sale.order"
    remote_note = "note"
    remote_product_id = "product_id"
    remote_partner_id = "partner_id"

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard_order()
