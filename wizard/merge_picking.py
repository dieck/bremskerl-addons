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

class stock_picking_merge_wizard(osv.osv_memory):
    _name = "stock.picking.merge.wizard"
    _description = "Merge Stock Pickings"
    
    _columns = {
        "target_picking_id": fields.many2one("stock.picking","Target Picking"),
        "picking_ids": fields.many2many("stock.picking","wizard_stock_move_picking_merge_chosen","merge_id","picking_id"),

        "target_picking_id_state": fields.related("target_picking_id", "state", type="char", string="Target Picking State"),
        "target_picking_id_type": fields.related("target_picking_id", "type", type="char", string="Target Picking Type"),
        "target_picking_id_invoice_state": fields.related("target_picking_id", "invoice_state", type="char", string="Target Picking Invoice State"),

        # basic stock.picking relations are related here, they are used for the many2many field domain
        # all non-basic relations are checked after being choosen, in do_check
        "target_picking_id_backorder_id": fields.related("target_picking_id", "backorder_id", type="many2one", relation='stock.picking', string="Target Picking Backorder"),
        "target_picking_id_stock_journal_id": fields.related("target_picking_id", "stock_journal_id", type="many2one", relation='stock.journal', string="Target Picking Journal ID"),
        "target_picking_id_location_id": fields.related("target_picking_id", "location_id", type="many2one", relation='stock.location', string="Target Picking Location"),
        "target_picking_id_location_dest_id": fields.related("target_picking_id", "location_dest_id", type="many2one", relation='stock.location', string="Target Picking Destination Location"),
        "target_picking_id_address_id": fields.related("target_picking_id", "address_id", type="many2one", relation='res.partner.address', string="Target Picking Adress"),
        "target_picking_id_company_id": fields.related("target_picking_id", "company_id", type="many2one", relation='res.company', string="Target Picking Company"),
        
        "commit_merge": fields.boolean("Commit merge"),
    }        
  
    def return_view(self, cr, uid, name, res_id):
        data_pool = self.pool.get('ir.model.data')
        result = data_pool.get_object_reference(cr, uid, 'stock_merge_picking', name)
        view_id = result and result[1] or False
        r = {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking.merge.wizard',
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
        
        fields_pool = self.pool.get("ir.model.fields")

        for session in self.browse(cr, uid, ids):
            target = session.target_picking_id
            for merge in session.picking_ids:
                # look for incompatible moves
                for move in merge.move_lines:
                    if (move.state == 'done'):
                        raise osv.except_osv(_('Warning'),
                              _('The following picking can not be merged due to moves in state done:') + " " + str(merge.name))
                        return self.return_view(cr, uid, 'merge_picking_form_target', ids[0])
                    
                # test all many2one fields for compability,as we can't link to different targets from one merged object!
                # search for all related fields
                fields_search = fields_pool.search(cr, uid, [('ttype','=','many2one'),('model','=','stock.picking'),('relation','<>',self._name)])
                for field in fields_pool.browse(cr, uid, fields_search, context):
                    print "context", context
                    print "field desc", field.field_description
                    related_target_id = getattr(target, field.name)
                    related_merge_id = getattr(merge, field.name)
                    if (related_target_id.id != related_merge_id.id):
                        desc = field.field_description
                        desc = self.pool.get(field.model)._columns[field.name].string
                        raise osv.except_osv(_('Warning'),
                                _('The picking %s can not be merged due to different %s (%s) references.') % (str(merge.name), desc, field.name) )
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
        fields_pool = self.pool.get("ir.model.fields")
    
        for session in self.browse(cr, uid, ids):
            target = session.target_picking_id
            
            target_changes = {"date_done": target.date_done }

            # prepare notes, esp. if not existing           
            if (target.note):
                target_changes['note'] = target.note + ";\n"
            else:
                target_changes['note'] = ""
            target_changes['note'] += "This is a merge target."

            for merge in session.picking_ids:
                # fetch notes

                linenote = " Merged " + str(merge.name)
                if (merge.origin != target.origin):
                    linenote += ", had Origin " + str(merge.origin)
                
                if (merge.date != target.date):
                    linenote += ", from " + str(merge.date)

                if (merge.note):
                    linenote += ", Notes: " + str(merge.note)

                target_changes['note'] += linenote + ";\n"


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
                # not explicitly neccessary anymore, as it will be done by the many2one updates on all fields below
                #for move in merge.move_lines:
                #    move_pool.write(cr, uid, [move.id], {"picking_id": target.id})

                    
                ## update all relations to the old picking to look for the new one
                
                # search for all related fields.
                # we don't need to handle one2many: backlinked references had to be equal in order to be compatible.
                fields_search = fields_pool.search(cr, uid, [('relation','=','stock.picking'),('model','<>',self._name),
                                                             '|',('ttype','=','many2one'),('ttype','=','many2many')])
                
                # go through these fields
                for field in fields_pool.browse(cr, uid, fields_search):
                    # find the model they're in
                    model_pool = self.pool.get(field.model)
                    
                    # this can happen if you deinstalled modules by deleting their code, so they left something behind in the definition.
                    if (not model_pool):
                        continue
                    
                    # handle many2one: simply replace the id 
                    if (field.ttype == 'many2one'):
                        # find all entries that are old
                        model_search = model_pool.search(cr, uid, [(field.name,'=',merge.id)])
                        # and update them in one go
                        model_pool.write(cr, uid, model_search, {field.name: target.id})

                    # handle many2many:  
                    if (field.ttype == 'many2many'):
                        # find all entries that are old (don't know how yet, so I'll have to take 'em all
                        model_search = model_pool.search(cr, uid, []) # (field.name,'=',merge.id)
                        # and update them in one go
                        model_pool.write(cr, uid, model_search, {field.name: [(3,merge.id),(4,target.id)]})
                    
                # updated everything, so now I can get rid of the object
                picking_pool.unlink(cr, uid, [merge.id])

            # /for merge
            picking_pool.write(cr, uid, [target.id], target_changes)
                
        return {'type': 'ir.actions.act_window_close'}

stock_picking_merge_wizard()

