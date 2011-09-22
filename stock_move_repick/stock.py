# -*- coding: utf-8 -*-

from osv import fields, osv
from tools.translate import _


class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = _name

    _columns = {
        'repick_origin': fields.char('Original Picking Origin', size=64, help="Reference of the document that produced the picking this move was previously part of, before re-picking.", select=True),
        'repick_backorder_id': fields.many2one('stock.picking', 'Original Picking Back Order of', help="If the original picking before re-picking was split this field links to the picking that contains the other part that has been processed already.", select=True),
        'repick_sale_id': fields.many2one('sale.order', 'Pre-RePick Sales Order Reference'),
    }

    def action_repick(self, cr, uid, ids, context=None):
        # nothing to process
        if len(context['active_ids']) == 0:
            return {}

        # test all, even if single item                
        for item in self.browse(cr, uid, context['active_ids'], context):            
            if ((item.state == 'done') or (item.state == 'cancel')):
                raise osv.except_osv(_('Operation forbidden'),_('You cannot pick done or cancelled moves.'))
            if ((item.picking_id.state == 'done') or (item.picking_id.state == 'cancel')):
                raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the picking is done or cancelled.'))
        
        same_picking = True

        wlog_id = context['active_ids'][0]
        wlog_item = self.browse(cr, uid, wlog_id, context)

        wlog_picking_id = wlog_item.picking_id.id or None
        wlog_type = wlog_item.picking_id.type or None

        # there must not be a move in the "same_picking" pickings that's not selected for recombination 
        for ml in wlog_item.picking_id.move_lines:
            if (ml.id not in context['active_ids']):
                same_picking = False
        
        # more than one to process: check for compatibility
        if len(context['active_ids']) >= 2:
            
            for item in self.browse(cr, uid, context['active_ids'], context):
                
                # test if it's already the same picking for all moves
                if (wlog_item.picking_id.id != item.picking_id.id):
                    same_picking = False
                # there must not be a move in the "same_picking" pickings that's not selected for recombination 
                for ml in item.picking_id.move_lines:
                    if (ml.id not in context['active_ids']):
                        same_picking = False
                
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
                
                if (wlog_item.picking_id.address_id.id != item.picking_id.address_id.id):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves to different delivery addresses.'))

                if (wlog_item.picking_id.invoice_state != item.picking_id.invoice_state):
                    raise osv.except_osv(_('Operation forbidden'),_('You cannot pick moves where the pickings have different invoice states.'))

        data_pool = self.pool.get('ir.model.data')

        # if the chosen moves already combine one picking,
        if (same_picking):
            # return appropriate view        
            view_names = {'out': 'view_picking_out_form',
                          'in': 'view_picking_in_form', 
                          'internal': 'view_picking_form'
                          }
            view_result = data_pool.get_object_reference(cr, uid, 'stock', view_names[wlog_type])
            view_id = view_result and view_result[1] or False
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'views': [(view_id, 'form')],
                'res_model': 'stock.picking',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': wlog_picking_id,
                'context': context,
            }
        
        # everything is ok

        # present "yes/no" dialog
        view_result = data_pool.get_object_reference(cr, uid, 'stock_move_repick', 'move_repick_form_yesno')
        view_id = view_result and view_result[1] or False
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.move.repick.wizard',
            'views': [(view_id, 'form')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }
        
stock_move()


