from osv import osv, fields

class project_related(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
    
    def _get_subprojects(self, cr, uid, ids, field_name, arg, context):
        res = {}
        project_obj = self.pool.get("project.project")
        for session in self.browse(cr, uid, ids):
            project_ids = project_obj.search(cr, uid, [('analytic_account_id.parent_id','=',session.analytic_account_id.id)])
            res[session.id] = project_ids
        return res

    def _get_parentproject(self, cr, uid, ids, field_name, arg, context):
        res = {}
        project_obj = self.pool.get("project.project")
        for session in self.browse(cr, uid, ids):
            project_ids = project_obj.search(cr, uid, [('analytic_account_id.id','=',session.analytic_account_id.parent_id.id)])
            if (len(project_ids)>0):
                res[session.id] = project_ids[0]
            else:
                res[session.id] = False
        return res


    _columns = {
        'subproject_ids': fields.function(_get_subprojects, type='one2many', obj='project.project', method=True, string="Subprojects",),
        'parent_project_id': fields.function(_get_parentproject, type='many2one', obj='project.project', method=True, string="Parent Project",),
    }

project_related()

