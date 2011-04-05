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
import netsvc

class wiz_stock_picking_merge(osv.osv_memory):
    _name = "stock.move.picking.merge"
    _description = "Merge Stock Pickings"
    
    _columns = {
        "target_picking_id": fields.many2one("stock.picking","Target Picking"),
        "picking_ids": fields.many2many("stock.picking","wizard_stock_move_picking_merge_chosen","merge_id","picking_id"),

        "target_picking_id_type": fields.related("target_picking_id", "type", type="char", string="Target Picking Type"),
        "target_picking_id_state": fields.related("target_picking_id", "state", type="char", string="Target Picking State"),
        "target_picking_id_address_id": fields.related("target_picking_id", "address_id", type="many2one", relation='res.partner.address', string="Target Picking Adress"),
        
        "commit_merge": fields.boolean("Commit merge"),
    }        
  
  
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
# does not work. gives an error: "can't adapt type browse_record" when finding no compatible data.
# Works with two datasets with address_id=null, though, so traversing seems not to be the problem...
#                                                ('address_id','=',session.target_picking_id.address_id) ])
#            if (similiar_ids):
#                found = True
                                                
# so I'll do it manually.
                                               ])
               
            for similiar in picking_pool.browse(cr, uid, similiar_ids):
                # ok if addresses are similiar
                if (similiar.address_id.id == session.target_picking_id.address_id.id):
                    found = True
        
        if not found: 
            raise osv.except_osv(_('Note'),_('There are no compatible pickings to be merged.'))
            return self.return_view(cr, uid, 'merge_picking_form_init', ids[0])
        # else:
        return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])
    
    def do_check(self, cr, uid, ids, context=None):
        # maybe check if pickings are compatible with the target one, by type, state, address_id
        # but this should not happen, as the domain constraints won't allow incompatible pickings chosen to merge
        return self.return_view(cr, uid, 'merge_picking_form_checked', ids[0])        
    
    def do_merge(self, cr, uid, ids, context=None):
        # bail out if checkbox not set
        for session in self.browse(cr, uid, ids):
            if not session.commit_merge: 
                raise osv.except_osv(_('Unchecked'),_('You did not check the Commit Merge checkbox.'))
                return self.return_view(cr, uid, 'merge_picking_form_checked', ids[0])
        # merge 
        #TODO merge
        
        return True

               
    def find_max_invid(self,cr,uid,ids,address_id,state,type):
        stk_move_obj = self.pool.get('stock.picking')
        stk_move = self.pool.get('stock.move')

        cr.execute("select max(id) from stock_picking where type='%s' and state='%s' and address_id=%d" % (type,state,address_id))
        max_picking_id=cr.fetchall()[0][0]
    
        cr.execute('select * from stock_picking where id=%d' %(max_picking_id))
        rec_dict=cr.dictfetchall()
    
        rec_dict[0].__delitem__('perm_id')
        rec_dict[0].__delitem__('create_uid')
        rec_dict[0].__delitem__('create_date')
        rec_dict[0].__delitem__('write_date')
        rec_dict[0].__delitem__('write_uid')
        rec_dict[0].__delitem__('id')
    
        rec_dict[0]['name']="OUT:"+str(max_picking_id+1)
        rec_dict[0]['state']="draft"
    
        cr.execute("select * from stock_picking pc where type='%s' and state='%s' and address_id=%d" % (type,state,address_id))
        picking_info=cr.dictfetchall()
    
        if len(picking_info) > 1:
            cr_id=stk_move_obj.create(cr,uid,rec_dict[0],context=None)
    
            for picking in picking_info:
                pick_ids=stk_move.search(cr,uid,[('picking_id','=',picking['id'])])
    
                for pick_id in pick_ids:
                    stk_move.write(cr,uid,pick_id,{'picking_id':cr_id})
    
                wf_service = netsvc.LocalService("workflow")
                wf_service.trg_validate(uid, 'stock.picking', picking['id'], 'button_cancel', cr)
    
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(uid, 'stock.picking', cr_id, 'button_confirm', cr)
    
            stk_move_obj.action_assign(cr,uid,[cr_id])
        return True

    def find_partner(self,cr,uid,ids,context=None):
        state = 'assigned'
        type = 'out'
    
        cr.execute("select address_id from stock_picking where type='%s' and state='%s' and address_id is not null group by address_id,state,type" % (type,state))
        partner_ids=cr.dictfetchall()
    
        for partner in partner_ids:
            self.find_max_invid(self,cr,uid,ids,partner['address_id'],state,type)
    
        return {}


wiz_stock_picking_merge()

