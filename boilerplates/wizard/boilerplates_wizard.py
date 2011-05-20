# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class boilerplate_wizard(osv.osv_memory):
    _name = "boilerplate.wizard"
    _description = "Add Boilerplate"
    
    remote_name = _("Dummy")
    remote_model = "will.not.work"
    remote_note = "note"
    remote_product_id = False
    remote_partner_id = False
    
    _columns = {
        "boilerplate_id": fields.many2one("boilerplates.text","Boilerplate"),
        "remote_id": fields.many2one(remote_model, "Remote model"),
    }        
  
    #TODO does not work!
    # see http://www.openerp.com/forum/topic24970.html
    # and https://bugs.launchpad.net/openobject-server/+bug/780584
    def is_translateable(self, cr, uid, model, field):
        ir_model_fields = self.pool.get("ir.model.fields")
        model_id = ir_model_fields.search(cr, uid, [('model','=',model),('name','=',field)])
        for m in ir_model_fields.browse(cr, uid, model_id):
            if (m.translate):
                return True
        return False

    def browselanguages(self, cr, uid):
        res_lang = self.pool.get("res.lang")
        all_res_lang = res_lang.search(cr, uid, [])
        return res_lang.browse(cr, uid, all_res_lang)

  
    def do_boilerplate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        for session in self.browse(cr, uid, ids, context=context):
            
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
            
            # ok, add notes, maybe per language
            remote_pool = self.pool.get(self.remote_model)
            
            
            # add accordingly in all translations
            
            #TODO use is_translateable if https://bugs.launchpad.net/openobject-server/+bug/780584 is fixed
            res_lang = self.pool.get('res.lang')
            lang_ids = res_lang.search(cr, uid, [])
            for lang in res_lang.browse(cr,uid,lang_ids):
                ctx = context
                ctx['lang'] = lang.code
                
                for transession in self.browse(cr, uid, [session.id], context=ctx):
                    oldnotes = getattr(transession.remote_id, self.remote_note)
                    if (not oldnotes):
                        oldnotes = ""
                        
                    notes_to_add = str(transession.boilerplate_id.text)
                    if (not oldnotes.endswith(notes_to_add)):
                        newnotes = oldnotes + "\n" + transession.boilerplate_id.text
                        remote_pool.write(cr, uid, [transession.remote_id.id], {self.remote_note: newnotes}, context=ctx)
                
        return {'type': 'ir.actions.act_window_close'}

boilerplate_wizard()

