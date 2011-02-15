
from osv import osv, fields

class project_viewchildren_project(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
     
    def _get_child_ids(self, cr, uid, ids, field_name, arg, context):
        res = {}
        analytic_account_obj = self.pool.get('account.analytic.account')
        for prj_session in self.browse(cr, uid, ids):
            aa_child_ids = analytic_account_obj.search(cr, uid, [ ('parent_id','=',prj_session.analytic_account_id.id) ])
            aa_res = {}       
            for aa_session in analytic_account_obj.browse(cr, uid, aa_child_ids):
                aa_res.extend(aa_session.project_ids) 

            res[prj_session.id] = aa_res
        return res
    
    
    _columns = {
    #    "child_ids": fields.one2many("project.project", "analytic_account_id.parent_id", "Child projects"),
    #    "child_ids" : fields.boolean("test"),
  #      "child_ids": fields.related("analytic_account_id","child_ids","project_ids",
   #                               type='one2many',
    #                              #relation="account.analytic.account",
     #                             string="Child projects",
      #                            readonly=True),
      
       "child_ids": fields.function(_get_child_ids,
                                   string="Child projects",
                                   type='one2many',
                                   method=True),
    }    
   
 
project_viewchildren_project()
