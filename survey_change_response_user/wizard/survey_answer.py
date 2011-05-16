# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################

from osv import osv,fields

class survey_uid_changer_wizard(osv.osv_memory):
    _name = "survey.uid.changer.wizard"
  
    _columns = {
        'survey_ids': fields.many2many('survey.response', 'survey_uid_changer_wizard_rel', 'response_id', 'wizard_id', 'Survey Responses', required=True),
        'user_id': fields.many2one('res.users', 'Survey User', required=True),
    }
    
    def _get_default_survey(self, cr, uid, context=None):
        survey_response = self.pool.get('survey.response')
        
        latest_survey = None
        
        my_surveys = survey_response.search(cr, uid, [("user_id",'=',uid)])
        for sr in survey_response.browse(cr, uid, my_surveys):
            if (latest_survey == None):
                latest_survey = sr
            if (sr.date_create >= latest_survey.date_create):
                latest_survey = sr

        return [latest_survey.id]
        
        
    _defaults = {
        'survey_ids': _get_default_survey
    }
    
    
    def do_changeuid(self, cr, uid, ids, context=None):
        survey_response = self.pool.get('survey.response')
        for wiz in self.browse(cr,uid,ids,context=context):
            ids = []
            for sr in wiz.survey_ids:
                ids.append(sr.id)
            survey_response.write(cr,uid,ids,{'user_id': wiz.user_id.id},context=context)
        return {'type': 'ir.actions.act_window_close'}
    
survey_uid_changer_wizard()
