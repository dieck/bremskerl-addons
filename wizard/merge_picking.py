# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
#
#    Merge Picking up to v5 of OpenERP was written by Axelor, www.axelor.com
#    This is a complete rewrite.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

class wiz_stock_picking_merge(osv.osv_memory):
    _name = "stock.move.picking.merge"
    _description = "Merge Stock Pickings"
    
    _columns = {
        "target_picking_id": fields.many2one("stock.picking","Target Picking"),
        "picking_ids": fields.many2many("stock.picking","wizard_stock_move_picking_merge_chosen","merge_id","picking_id"),

        "target_picking_id_state": fields.related("target_picking_id", "state", type="char", string="Target Picking State"),
        "target_picking_id_type": fields.related("target_picking_id", "type", type="char", string="Target Picking Type"),
        "target_picking_id_invoice_state": fields.related("target_picking_id", "invoice_state", type="char", string="Target Picking Invoice State"),

        "target_picking_id_backorder_id": fields.related("target_picking_id", "backorder_id", type="many2one", relation='stock.picking', string="Target Picking Backorder"),
        "target_picking_id_stock_journal_id": fields.related("target_picking_id", "stock_journal_id", type="many2one", relation='stock.journal', string="Target Picking Journal ID"),
        "target_picking_id_location_id": fields.related("target_picking_id", "location_id", type="many2one", relation='stock.location', string="Target Picking Location"),
        "target_picking_id_location_dest_id": fields.related("target_picking_id", "location_dest_id", type="many2one", relation='stock.location', string="Target Picking Destination Location"),
        "target_picking_id_address_id": fields.related("target_picking_id", "address_id", type="many2one", relation='res.partner.address', string="Target Picking Adress"),
        "target_picking_id_company_id": fields.related("target_picking_id", "company_id", type="many2one", relation='res.company', string="Target Picking Company"),
        
        "commit_merge": fields.boolean("Commit merge"),
    }        
  
    def module_installed(self, cr, uid, name):
        mod_pool = self.pool.get("ir.module.module")
        search_mod = mod_pool.search(cr, uid, [("name","=",name)])
        for mod in mod_pool.browse(cr, uid, search_mod):
            if (mod.state == 'installed'):
                return True
        return False
  
    def return_view(self, cr, uid, name, res_id):
        data_pool = self.pool.get('ir.model.data')
        result = data_pool.get_object_reference(cr, uid, 'merge_picking_v6', name)
        view_id = result and result[1] or False
        r = {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.move.picking.merge',
            'views': [(view_id, 'form')],
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': res_id,
        }
        return r
    
    def do_target(self, cr, uid, ids, context=None):
        # look if we got compatible views
        picking_pool = self.pool.get('stock.picking')
       
        found = False
        for session in self.browse(cr, uid, ids):
            similiar_ids = picking_pool.search(cr, uid, [('id','<>',session.target_picking_id.id),
                                                ('state','=',session.target_picking_id.state),
                                                ('type','=',session.target_picking_id.type),
                                                ('invoice_state','=',session.target_picking_id.invoice_state),
                                                
# related fields do not work. give an error: "can't adapt type browse_record" when finding no compatible data.
# Works with two datasets with like address_id=null, though, so traversing seems not to be the problem...
#                                                ('address_id','=',session.target_picking_id.address_id) ])
#            if (similiar_ids):
#                found = True
                                                
# so I'll do it manually for related fields
                                               ])

            # check for compability on related fields address, backorder, stock journal, location, location dest & company               
            for similiar in picking_pool.browse(cr, uid, similiar_ids):
                similiarOK = True
                
                if (similiar.address_id.id <> session.target_picking_id.address_id.id):
                    similiarOK = False

                if (similiar.backorder_id.id <> session.target_picking_id.backorder_id.id):
                    similiarOK = False
                    
                if (similiar.stock_journal_id.id <> session.target_picking_id.stock_journal_id.id):
                    similiarOK = False
                    
                if (similiar.location_id.id <> session.target_picking_id.location_id.id):
                    similiarOK = False
                    
                if (similiar.location_dest_id.id <> session.target_picking_id.location_dest_id.id):
                    similiarOK = False
                    
                if (similiar.company_id.id <> session.target_picking_id.company_id.id):
                    similiarOK = False
                    
                if (similiarOK):
                    found = True
        
        if not found: 
            raise osv.except_osv(_('Note'),_('There are no compatible pickings to be merged.'))
            return self.return_view(cr, uid, 'merge_picking_form_init', ids[0])
        # else:
        return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])
    
    
    def do_check(self, cr, uid, ids, context=None):
        # check if pickings are compatible again with the attributes
        # depending on additional modules!
        # I could not bring those to the domain, as there are no optional module dependencies in OpenERP for XML
        for session in self.browse(cr, uid, ids):
            target = session.target_picking_id
            for merge in session.picking_ids:
                # look for incompatible moves
                for move in merge.move_lines:
                    if (move.state == 'done'):
                        raise osv.except_osv(_('Warning'),
                              _('The following picking can not be merged due to moves in state done:') + " " + str(merge.name))
                        return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])
                    
                if (self.module_installed(cr, uid, "purchase")) and (target.purchase_id.id != merge.purchase_id.id):
                    raise osv.except_osv(_('Warning'),
                          _('The following picking can not be merged due to different purchase order references:') + " " + str(merge.name))
                    return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])

                if (self.module_installed(cr, uid, "sale")) and (target.sale_id.id != merge.sale_id.id):
                    raise osv.except_osv(_('Warning'),
                          _('The following picking can not be merged due to different sale order references:') + " " + str(merge.name))
                    return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])
         
        return self.return_view(cr, uid, 'merge_picking_form_checked', ids[0])        
    
    
    def do_merge(self, cr, uid, ids, context=None):
        # bail out if checkbox not set
        for session in self.browse(cr, uid, ids):
            if not session.commit_merge: 
                raise osv.except_osv(_('Unchecked'),_('You did not check the Commit Merge checkbox.'))
                return self.return_view(cr, uid, 'merge_picking_form_checked', ids[0])

        # merge
        picking_pool = self.pool.get("stock.picking")
        move_pool = self.pool.get("stock.move")
    
        for session in self.browse(cr, uid, ids):
            target = session.target_picking_id
            
            target_changes = {"date_done": target.date_done }

            # prepare notes, esp. if not existing           
            target_changes['note'] = str(target.note)
            if (target.note):
                target_changes['note'] += ";\n"
            target_changes['note'] += "This is a merge target."
            
            for merge in session.picking_ids:

                # fetch notes
                linenote = "Merged " + str(merge.name)
                if (merge.origin != target.origin):
                    linenote += ", had Origin " + str(merge.origin)
                
                if (merge.date != target.date):
                    linenote += ", from " + str(merge.date)
                
                # handle changeable values
                
                # if any one merge has partial delivery, deliver the whole picking as partial (direct)
                if (merge.move_type == 'direct'):
                    target_changes['move_type'] = 'direct'
                
                # date_done = MAX(date_done)
                if (target_changes['date_done'] < merge.date_done):
                    target_changes['date_done'] = merge.date_done
                
                # if any one merge is NOT auto_picking, then the target is not.
                # should never occur, as auto_picking would set it to done instantly, which can't be merged
                if (not (merge.auto_picking)):
                    target_changes['auto_picking'] = False
                
                # combine moves
                for move in merge.move_lines:
                    move_pool.write(cr, uid, [move.id], {"picking_id": target.id})
                
                target_changes['note'] += linenote 
            # for merge
            
            picking_pool.write(cr, uid, [target.id], target_changes)
                
        return True

wiz_stock_picking_merge()

