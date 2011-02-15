from osv import osv, fields

class project_viewchildren_analyticaccount(osv.osv):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    _columns = {
        "project_ids": fields.one2many("project.project", "analytic_account_id", "Associated projects"),
    }
project_viewchildren_analyticaccount()
