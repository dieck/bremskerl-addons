# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _


class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name

    _columns = {
        'picker_origin': fields.char('Original Picking Origin', size=64, help="Reference of the document that produced the picking this move was previously part of.", select=True),
        'picker_backorder_id': fields.many2one('stock.picking', 'Original Picking Back Order of', help="If the original picking was split this field links to the picking that contains the other part that has been processed already.", select=True),
    }

    def action_picking_picker(self, cr, uid, ids, context=None):
        # nothing to process
        if len(context['active_ids']) == 0:
            return {}

        # test all, even if single item                
        for item in self.browse(cr, uid, context['active_ids'], context):            
            if ((item.state == 'done') or (item.state == 'cancel')):
                raise osv.except_osv(_('Operation forbidden'),_('You cannot pick done or cancelled moves.'))
            if ((item.picking_id.state == 'done') or (item.picking_id.state == 'cancel')):
                raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the picking is done or cancelled.'))
        
        # more than one to process: check for compatibility
        if len(context['active_ids']) >= 2:
            active_ids = context['active_ids']
            wlog_id = active_ids.pop()
            wlog_item = self.browse(cr, uid, wlog_id, context)
            
            for item in self.browse(cr, uid, active_ids, context):
                
                # fields for move
                if (wlog_item.company_id.id != item.company_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves from different companies.'))

                if (wlog_item.company_id.id != item.company_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves from different companies.'))

                if (wlog_item.company_id.id != item.company_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves from different companies.'))

                
                # required fields for picking, must be equal
                if (wlog_item.picking_id.type != item.picking_id.type):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves from different picking types.'))

                if (wlog_item.picking_id.move_type != item.picking_id.move_type):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different delivery methods.'))

                if (wlog_item.picking_id.state != item.picking_id.state):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different states.'))

                if (wlog_item.picking_id.company_id.id != item.picking_id.company_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings belong to different companies.'))


                # optional fields for picking, but must be equal
                if (wlog_item.picking_id.stock_journal_id.id != item.picking_id.stock_journal_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have stock journals.'))

                if (wlog_item.picking_id.location_id.id != item.picking_id.location_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different locations.'))

                if (wlog_item.picking_id.location_dest_id.id != item.picking_id.location_dest_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different destination locations.'))
                
                if (wlog_item.picking_id.auto_picking != item.picking_id.auto_picking):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves to different auto-picking settings.'))

                if (wlog_item.picking_id.address_id.id != item.picking_id.address_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves to different delivery addresses.'))

                if (wlog_item.picking_id.invoice_state != item.picking_id.invoice_state):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different invoice states.'))

        # everything is ok

        # present "yes/no" dialog
        data_pool = self.pool.get('ir.model.data')
        view_result = data_pool.get_object_reference(cr, uid, 'stock_picking_picker', 'picking_picker_form_yesno')
        view_id = view_result and view_result[1] or False

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking.picker.wizard',
            'views': [(view_id, 'form')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }
        
stock_move()


