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
import time

class stock_picking_picker_wizard(osv.osv_memory):
    _name = "stock.picking.picker.wizard"
    _description = "Pick Stock Pickings"
    
    def do_create_picking(self, cr, uid, ids, context=None):
        picking_pool = self.pool.get("stock.picking")
        move_pool = self.pool.get("stock.move")
        
        wlog_move = move_pool.browse(cr, uid, context['active_ids'][0], context)
        
        new_picking = {
            # required fields
            "type": wlog_move.picking_id.type,
            "move_type": wlog_move.picking_id.move_type,
            "state": wlog_move.picking_id.state,
            "company_id": wlog_move.picking_id.company_id.id,

            # optional, but equal fields
            "stock_journal_id": wlog_move.picking_id.stock_journal_id.id or None,
            "location_id": wlog_move.picking_id.location_id.id or None,
            "location_dest_id": wlog_move.picking_id.location_dest_id.id or None,
            "address_id": wlog_move.picking_id.address_id.id or None,
            "invoice_state": wlog_move.picking_id.invoice_state or None,

            # optional, may not be set            
            "auto_picking": True,
            "origin": None,
            "backorder_id": None,
            "note": "",
            "date": time.strftime('%Y-%m-%d %H:%M:%S'),
            "date_done": None, # only set on done pickings, which can't be processed anyway
            "move_lines": None,
        }
        
        origins = []
        backorder_ids = []
        note_moves = []
        move_changes = {}
            
        for move in move_pool.browse(cr, uid, context['active_ids'], context):
            # list of origins
            origins.append(move.picking_id.origin or None)
            # list of backorder_ids
            backorder_ids.append(move.backorder_id.id or None)
            # if one item is set to manual picking, the whole picking is
            if (not(move.picking_id.auto_picking)):
                new_picking["auto_picking"] = False
            # notes
            note_moves.append(move.name + " [" + str(move.id) + "]")
            # changes for updates/writes later
            move_changes[move.id] = {"picker_origin": move.origin or None,
                                  "picker_backorder_id": move.backorder_id.id or None}                

        new_picking["note"] = "Incorporated moves: " + ', '.join(note_moves) + "\n"
            
        origins = list(set(origins)) # unique
        origins = [o for o in origins if o != None] # filter None
        new_picking["origin"] = ','.join(origins)
        if (len(new_picking["origin"])>64):
            new_picking["origin"] = new_picking["origin"][0:60] + "..."
            new_picking["note"] += "\nFull list of origins: " + ', '.join(origins)

        backorder_ids = list(set(backorder_ids)) # unique
        backorder_ids = [bo for bo in backorder_ids if bo != None] # filter None
        if (len(backorder_ids) == 1):
            # single/same backorder found, use that
            new_picking["backorder_id"] = backorder_ids[0]


        new_picking_id = picking_pool.create(cr, uid, new_picking)
        
        for i,c in move_changes.iteritems():
            c["picking_id"] = new_picking_id
            move_pool.write(cr, uid, [i], c)

        
        view_names = {'out': 'view_picking_out_form',
                      'in': 'view_picking_in_form', 
                      'internal': 'view_picking_form'
                      }
        data_pool = self.pool.get('ir.model.data')
        view_result = data_pool.get_object_reference(cr, uid, 'stock', view_names[new_picking['type']])
        view_id = view_result and view_result[1] or False
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'stock.picking',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': new_picking_id,
            'context': context,
        }

stock_picking_picker_wizard()

