# -*- coding: UTF-8 -*-
'''
@author: Dieckhoff
'''

from osv import osv, fields
import time
import pooler
from datetime import datetime, timedelta
from tools.translate import _


class tem_listing_bylocation_location(osv.osv_memory):
    _name = "tem.listing.bylocation.location"

    _rec_name = "date_end"
         
    def _get_due_equipments(self, cr, uid, ids, field_name, arg, context):
        res = {}
        equipment_obj = self.pool.get("tem.equipment")
        
        for bll in self.browse(cr, uid, ids):

            dom = []
            dom.append(('usage_site','=',bll.location_id.id))
            if (bll.date_start):
                dom.append(('next_inspection','>=',bll.date_start))
            if (bll.date_end):
                dom.append(('next_inspection','<=',bll.date_end))
            
            due_equipment = equipment_obj.search(cr, uid, dom)
            
            due = []
            for d in equipment_obj.browse(cr, uid, due_equipment):
                if (d.usage_site.printreports):
                    due.append(d.id)

            res[bll.id] = due
        return res
    
    _columns = {
        "location_id": fields.many2one("tem.location", "Location", required=True),
        "date_start": fields.date("Date start"),
        "date_end": fields.date("Date end", required=True),
        "due_equipment_ids": fields.function(_get_due_equipments, type='one2many', obj='tem.equipment', method=True, string="Due Equipment",),
    }                                
        
tem_listing_bylocation_location()


class tem_listing_bylocation(osv.osv_memory):
    _name = 'tem.listing.bylocation'
    _description = 'Listing by Location'
    
    _rec_name = "date_end"
    
    def _search_locations(self, cr, uid, ids, name, args, context=None):
        res = {}

        bylocation_location_obj = self.pool.get("tem.listing.bylocation.location")
        
        location_obj = self.pool.get("tem.location")
        all_locations = location_obj.search(cr, uid, [])

        for i in self.browse(cr, uid, ids):
            lines = []
          
            for l in location_obj.browse(cr, uid, all_locations):
                data = { "location_id": l.id, "date_start": i.date_start, "date_end": i.date_end }
                bll = bylocation_location_obj.create(cr, uid, data)

                                
                # print only the ones which will have due_equipment_ids 
                bll_this = bylocation_location_obj.browse(cr, uid, bll)
                if (len(bll_this.due_equipment_ids) > 0):
                    lines.append(bll)
            
            res[i.id] = lines

        return res
    
    _columns = {
        "date_start": fields.date("Date start"),
        "date_end": fields.date("Date end", required=True),
        "location_ids": fields.function(_search_locations, relation='tem.listing.bylocation.location', type="many2many", string='Locations', method=True),
    }
    
    _defaults = {
        "date_end": lambda *a: (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
    }
    
tem_listing_bylocation()

