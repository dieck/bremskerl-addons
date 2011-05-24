# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
#
#    Merge Picking up to v5 of OpenERP was written by Axelor, www.axelor.com
#    This is a complete rewrite.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard(osv.osv_memory):
    _name = "boilerplate.wizard.mrp.order"
    _inherit = "boilerplate.wizard"

    remote_name = _("MRP Order")
    remote_model = "mrp.production"
    remote_note = "note"
    remote_product_id = "product_id"
    remote_partner_id = False

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard()

class boilerplate_wizard_bom(osv.osv_memory):
    _name = "boilerplate.wizard.mrp.bom"
    _inherit = "boilerplate.wizard"

    remote_name = _("MRP BoM")
    remote_model = "mrp.bom"
    remote_note = "note"
    remote_product_id = "product_id"
    remote_partner_id = False

    _columns = {
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }    

boilerplate_wizard_bom()