# -*- coding: utf-8 -*-

from osv import osv, fields

class purchase_order_line(osv.osv):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"

    def action_open_boilerplates(self, cr, uid, ids, context=None):
        data_pool = self.pool.get('ir.model.data')
        result = data_pool.get_object_reference(cr, uid, 'boilerplates_purchase', 'boilerplates_wiz_line')
        view_id = result and result[1] or False
        id = ids and ids[0] or False
        r = {
            'name': 'Add Boilerplate',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'boilerplate.wizard.purchase.order.line',
            'views': [(view_id, 'form')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'domain': [('remote_id', '=', id)],
            'context': {'search_default_filter_usability_purchase':1}
        }
        return r

purchase_order_line()
