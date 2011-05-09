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

class boilerplate_wizard_sale(osv.osv_memory):
    _name = "boilerplate.wizard.sale"
    _description = "Add Boilerplate"
    
    remote_name = _("Sales Order")
    remote_model = "sale.order"
    remote_note = "note"
    remote_product_id = False
    remote_partner_id = "partner_id"
    
    _columns = {
        "boilerplate_id": fields.many2one("boilerplates.text","Boilerplate"),
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }        
  
    def do_boilerplate(self, cr, uid, ids, context=None):

        for session in self.browse(cr, uid, ids):
            
            # look for wrongly chosen boilerplate
            bp_pid = session.boilerplate_id.product_id
            if (bp_pid):
                if (self.remote_product_id):
                    remote_pid = getattr(session.remote_id, self.remote_product_id)
                    if (not remote_pid or (bp_pid.id != remote_pid.id)):
                        raise osv.except_osv(_('Product mismatch'),_('Product set on the Boilerplate does not match this ') + self.remote_name)
                else:
                    raise osv.except_osv(_('Product mismatch'),_('Product set on the Boilerplate does not match this ') + self.remote_name)
            
            bp_pid = session.boilerplate_id.partner_id
            if (bp_pid):
                if (self.remote_partner_id):
                    remote_pid = getattr(session.remote_id, self.remote_partner_id)
                    if (not remote_pid or (bp_pid.id != remote_pid.id)):
                        raise osv.except_osv(_('Partner mismatch'),_('Partner set on the Boilerplate does not match this ') + self.remote_name)
                        return { 'type': 'ir.actions.act_window_close' }
                else:
                    raise osv.except_osv(_('Partner mismatch'),_('Partner set on the Boilerplate does not match this ') + self.remote_name)
                    return { 'type': 'ir.actions.act_window_close' }


            
            # ok, add notes
            oldnotes = getattr(session.remote_id, self.remote_note)
            if (not oldnotes):
                oldnotes = ""
            newnotes = oldnotes + "\n" + session.boilerplate_id.text
    
            remote_pool = self.pool.get(self.remote_model)
            remote_pool.write(cr, uid, [session.remote_id.id], {self.remote_note: newnotes})
                
        return {'type': 'ir.actions.act_window_close'}

boilerplate_wizard_sale()

