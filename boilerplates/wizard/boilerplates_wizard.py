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
    
    def _lang_get(self, cr, uid, context={}):
        obj = self.pool.get('res.lang')
        ids = obj.search(cr, uid, [], context=context)
        res = obj.read(cr, uid, ids, ['code', 'name'], context)
        return [(r['code'], r['name']) for r in res] + [('','')]
    
    _columns = {
        "boilerplate_id": fields.many2one("boilerplates.text","Boilerplate"),
        "remote_id": fields.many2one(remote_model, "Remote model"),
        "lang": fields.selection(_lang_get, type='char', string="Language"),
    }        

    
    def is_translateable(self, browse):
        # following a hint of Vo Minh Thu in https://bugs.launchpad.net/openobject-server/+bug/780584
        # it is still possible for a non-custom field to see if it is translatable by inspecting the _columns attribute of the model.
        if (browse):
            cols = getattr(browse, "_columns") or False
            remotefield = cols[self.remote_note] or False
            return (remotefield.translate) 
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
            
            
            
            if (self.is_translateable(session.remote_id)):
                # do the whole show, add accordingly in all translations
                
                # if no sublanguage defined, self.browse with context will return default language
                # means: If unset before, secondary language translations have double content:
                #   default language + translated entry.
                # Therefore, I test here if the default store matches
                default_notes_to_add = u""

                # get default language text
                for transession in self.browse(cr, uid, [session.id], context={}):
                    default_notes_to_add = unicode(transession.boilerplate_id.text)
    
                    # if field was previously empty, first insert will put it to ALL databases.
                    oldnotes = getattr(transession.remote_id, self.remote_note)
                    if (not oldnotes):
                        remote_pool.write(cr, uid, [transession.remote_id.id], {self.remote_note: default_notes_to_add}, context={})
    
                res_lang = self.pool.get('res.lang')
                lang_ids = res_lang.search(cr, uid, [])
                for lang in res_lang.browse(cr,uid,lang_ids):
                    ctx = context
                    ctx['lang'] = lang.code
                    
                    for translated_session in self.browse(cr, uid, [session.id], context=ctx):
                        oldnotes = getattr(translated_session.remote_id, self.remote_note)
                   
                        if (oldnotes):
                            oldnotes = oldnotes + "\n"
                        else:
                            oldnotes = str("").encode('utf-8')
                        
                        notes_to_add = unicode(translated_session.boilerplate_id.text)
                     
                        # default_notes_to_add match old/last: bail out, already added default translation before
                        if (oldnotes.strip().endswith(default_notes_to_add)):
                            oldnotes = oldnotes[:oldnotes.rfind(default_notes_to_add)]
                            
                        if (not oldnotes.strip().endswith(notes_to_add)):
                            newnotes = oldnotes + translated_session.boilerplate_id.text
                            remote_pool.write(cr, uid, [translated_session.remote_id.id], {self.remote_note: newnotes}, context=ctx)

            else:
                # NOT self.is_translateable(session.remote_id) => use language as defined by current user
                
                ctx = context # includes user default language
                # if language was set on wizard, use it
                if (session.lang):
                    ctx['lang'] = session.lang
                    
                for translated_session in self.browse(cr, uid, [session.id], context=ctx):
                    oldnotes = getattr(session.remote_id, self.remote_note)
                    if (oldnotes):
                        oldnotes = oldnotes + "\n"
                    else:
                        oldnotes = str("").encode('utf-8')
                                
                    notes_to_add = unicode(translated_session.boilerplate_id.text)
                        
                    if (not oldnotes.strip().endswith(notes_to_add)):
                        newnotes = oldnotes + translated_session.boilerplate_id.text
                        remote_pool.write(cr, uid, [session.remote_id.id], {self.remote_note: newnotes}, context=context)
                
        return {'type': 'ir.actions.act_window_close'}

boilerplate_wizard()

