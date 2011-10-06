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
import netsvc

class stock_move_repick_wizard(osv.osv_memory):
    _name = "stock.move.repick.wizard"
    _description = "Stock Move RePick"
    
    def do_create_picking(self, cr, uid, ids, context=None):
        picking_pool = self.pool.get("stock.picking")
        move_pool = self.pool.get("stock.move")
        wf_service = netsvc.LocalService("workflow")
        
        wlog_move = move_pool.browse(cr, uid, context['active_ids'][0], context)
        
        new_picking = {
            # required fields
            "type": wlog_move.picking_id.type,
            "move_type": wlog_move.picking_id.move_type,
            "state": "draft", # need to start at draft and work my way "up" with workflows
            
            "company_id": wlog_move.picking_id.company_id.id,
            "invoice_state": wlog_move.picking_id.invoice_state or 'none',

            # optional, but equal fields
            "stock_journal_id": wlog_move.picking_id.stock_journal_id.id or None,
            "location_id": wlog_move.picking_id.location_id.id or None,
            "location_dest_id": wlog_move.picking_id.location_dest_id.id or None,
            "address_id": wlog_move.picking_id.address_id.id or None,

            # optional, may not be set            
            "auto_picking": False, # need to continue manually
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
        old_pickings = []
            
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
            move_changes[move.id] = {"name": move.name or None,
                                     "id": move.id or None,
                                     "picking_id": move.picking_id.id or None,
                                     "picking_id_note": move.picking_id.note or None,
                                     "repick_origin": move.origin or None,
                                     "repick_backorder_id": move.backorder_id.id or None,
                                     "repick_sale_id": move.picking_id.sale_id.id or None}
            
            # remember old picking ids for later processing
            old_pickings.append(move.picking_id.id or None)
                            

        new_picking["note"] = "RePicked moves: " + ', '.join(note_moves) + "\n"
            
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

        # create picking
        new_picking_id = picking_pool.create(cr, uid, new_picking)
        
        # set workflow        
        if (wlog_move.picking_id.state == 'confirmed') or (wlog_move.picking_id.state == 'assigned'):
            wf_service.trg_validate(uid, 'stock.picking', new_picking_id, 'button_confirm', cr)
            # workflow to state "assigned" has false trigger, so should be automatically done
            # picking_pool.force_assign(cr, uid, [new_picking_id], context)

#FIXME TODO  ok, now it's DONE at stock.picking, moves stay assigned...

        # get data        
        new_picking = picking_pool.browse(cr, uid, new_picking_id)
        
        # change move assigns (and write repick stored data)
        for i,c in move_changes.iteritems():
            chg = {"picking_id": new_picking_id,
                   "repick_origin": c["repick_origin"],
                   "repick_backorder_id": c["repick_backorder_id"],
                   "repick_sale_id": c["repick_sale_id"]}
            move_pool.write(cr, uid, [i], chg)
            picking_id_note = c["picking_id_note"] or ""
            chg = {"note": picking_id_note.strip()
                   + "\nMoved " + c["name"] + " ("+ str( c["id"]) +") to " + new_picking.name + "\n"}
            picking_pool.write(cr, uid, [c["picking_id"]], chg)
        
        # find now "empty" pickings and set them to done
        for pck in picking_pool.browse(cr, uid, old_pickings):
            if (len(pck.move_lines)==0):
                pck.action_done()
                
        # return appropriate view        
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

stock_move_repick_wizard()

