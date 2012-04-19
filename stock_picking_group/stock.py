# -*- coding: utf-8 -*-

from osv import fields, osv


class stock_picking_group_blanco(osv.osv):
    _name = "stock.picking.group"
stock_picking_group_blanco()


class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit = _name

    _columns = {
        "picking_group_id": fields.many2one("stock.picking.group", string="Picking Group"),
    }
stock_picking()


class stock_picking_group(osv.osv):
    _name = "stock.picking.group"
    _inherit = _name
             
    def _get_naming(self, pickingtype):         
        # TODO replace with live sequence prefix (codes "Picking IN", "Picking INT", "Picking OUT")
        naming = {'internal': 'INT/', 'out': 'OUT/', 'in': 'IN/'}
        return naming[pickingtype]
                                                       
    def _get_list(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            r = []
            for pick in session.picking_ids:
                r.append(pick.name)
            res[session.id] = ", ".join(r)
        return res
    
    
    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            res[session.id] = self._get_naming(session.type) + 'GRP' + str(session.id)
        return res
    
    def _get_move_ids(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            move_ids = {}
            for p in session.picking_ids:
                for m in p.move_lines:
                    move_ids[m.id] = m.id
            res[session.id] = move_ids.keys()
        print "res",res
        return res
    
    def _get_info(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            res[session.id] = {'type': 'unknown', 'address_id': None}
            if (session.picking_ids):
                first_picking = session.picking_ids[0]
                res[session.id] = {'type': first_picking.type, 'address_id': first_picking.address_id.id}
        return res
    
    _columns = {
        "name": fields.function(_get_name, string="Reference", type='char', size=75, method=True, store=True),
        "list": fields.function(_get_list, string="Pickings", type='char', size=255, method=True, store=True),
        "type": fields.function(_get_info, multi="type", string="Type", type='char', size=75, method=True, store=True),
        "address_id": fields.function(_get_info, multi="address_id", string="Address", type='many2one', relation="res.partner.address", size=75, method=True, store=True),
        "picking_ids": fields.one2many("stock.picking", "picking_group_id", name="Picking group"),
        "move_ids": fields.function(_get_move_ids, string="Moves", type='many2many', relation="stock.move", size=75, method=True, store=False),
    }
    

    def _check_grouped_compatible_picking(self, cr, uid, ids, context=None):
        for g in self.browse(cr, uid, ids, context=context):
            pickings = [p.id for p in g.picking_ids]
            check = self._check_compatible_picking(cr, uid, pickings, context)
            if (not check):
                return False  
        # all ok? then true
        return True

    def _check_compatible_picking(self, cr, uid, picking_ids, context=None):
        if (len(picking_ids) < 2):
            # one or no item? is compatible with itself
            return True

        picking_obj = self.pool.get("stock.picking")

        # Without Loss Of Generality, we take the first item to compare all later ones to
        wlog_id = picking_ids.pop()
        wlog = picking_obj.browse(cr, uid, wlog_id, context=context)
         
        for p in picking_obj.browse(cr, uid, picking_ids, context=context):
            if (wlog.type <> p.type):
                return False
            
            if (wlog.company_id.id <> p.company_id.id):
                return False
            
            wlog_address = wlog.address_id and wlog.address_id.id or None
            p_address = p.address_id and p.address_id.id or None
            if (wlog_address <> p_address):
                return False
        ## no problems occured
        return True
     
    _constraints = [
        (_check_grouped_compatible_picking, 'The pickings you chose are not compatible (type or address varies)', ['picking_ids']),
    ]
            
        
stock_picking_group()
