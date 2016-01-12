# -*- coding: utf-8 -*-

from osv import fields, osv

class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_related_picking_ids(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        stock_move = self.pool.get("stock.move")
        
        for record in self.browse(cr, uid, ids, context=context):
            pickings = {}
            for ol in record.order_line:
                for m in ol.move_ids:
                    if (m.picking_id):
                        pickings[m.picking_id.id] = True
            
            
            premerge_ids = stock_move.search(cr, uid, [('premerge_sale_id','=',record.id)], context=context)
            for p in stock_move.browse(cr,uid,premerge_ids,context=context):
                if (p.picking_id.id):
                    pickings[p.picking_id.id] = True
                
            result[record.id] = pickings.keys()
        return result


    # OpenERP uses a SQL query here. That works ok, but as they expect the sale id on stock.picking, not stock.move,
    # it won't work with merged pickings. If they had used their own framework instead of manual SQL, it would work fine.
    # So I'm not justify stock_merge_picking here, but replace a shortcoming of OpenERP :)
    def _picked_rate(self, cr, uid, ids, name, arg, context=None):
        if not ids:
            return {}
        res = {}
          
        for so in self.browse(cr, uid, ids, context=context):
            # I define: percentage of COUNT of lines (and consecutive moves) fulfilled, not product quantity.
            
            # variables for sale order lines           
            count_lines = 0.0
            count_lines_done = 0.0
            
            for line in so.order_line:
                # found a line
                count_lines += 1.0

                # variables for related stock moves - note: untouched by picking merges.
                count_moves = 0.0
                count_moves_done = 0.0
                
                for move in line.move_ids:
                    # found a move
                    count_moves += 1.0
                    
                    if (move.state == 'done'):
                        # found a DONE move
                        count_moves_done += 1.0

                # if we encountered any moves                
                if (count_moves > 0.0):
                    # "return" percentage of done moves
                    count_lines_done += count_moves_done / count_moves
                
            # if we encountered any line
            if (count_lines > 0.0):
                # return percentage of lines, subrelated on done moves                
                res[so.id] = (count_lines_done / count_lines) * 100
        
        # Yes, there may be more elegant ways then using serveral variables, but it's easy to read and debug this way,
        # and the python parser can anyway optimize much better than any human could. kiss principle.
        return res
        

    


    _columns = {
        'related_picking_ids': fields.function(_get_related_picking_ids, method=True, type='many2many', relation="stock.picking", string="Related Pickings"),
        'picked_rate': fields.function(_picked_rate, method=True, string='Picked', type='float'),
    }
        
sale_order()



