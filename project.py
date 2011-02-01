
from osv import osv, fields

class project_viewchildren(osv.osv):
    _name = "project.project"
    _inherit = "project.project"
    
    _columns = {
        "child_ids": fields.one2many("project.project", "parent_id", "Is parent to these projects"),
    }
project_viewchildren()
