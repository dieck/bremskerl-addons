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
    _inherits = { "tem_location": "tem.location" }
     
    def _get_due_equipments(self, cr, uid, ids, field_name, arg, context):
        res = {}
        equipment_obj = self.pool.get("tem.equipment")
        
        for loc in self.browse(cr, uid, ids):

            dom = []
            dom.append(('location_id','=',loc.id))
            if (loc.date_start):
                dom.append(('next_inspection','>=',loc.date_start))
            if (loc.date_end):
                dom.append(('next_inspection','<=',loc.date_end))
            
            due_equipment = equipment_obj.search(cr, uid, dom)

            res[loc.id] = due_equipment
        return res
    
    _columns = {
        "date_start": fields.date("Date start"),
        "date_end": fields.date("Date end"),                
        "due_equipment_ids": fields.function(_get_due_equipments, type='one2many', obj='tem.equipment', method=True, string="Due Equipment",),
    }                                
        
tem_listing_bylocation_location()


class tem_listing_bylocation(osv.osv_memory):
    _name = 'tem.listing.bylocation'
    _description = 'Listing by Location'
    
    _rec_name = "date_end"
    
    def _search_locations(self, cr, uid, ids, name, args, context=None):
        result = {}
        
        location_obj = self.pool.get("tem.listing.bylocation.location")
        all_locations = location_obj.search(cr, uid, [])
        
        ds = None
        de = None
        for i in self.browse(cr, uid, ids, context=context):
            ds = i.date_start
            de = i.date_end
            result[i.id] = all_locations

        location_obj.update(cr, uid, all_locations, {"date_start": ds, "date_end": de})

        return result
    
    _columns = {
        "date_start": fields.date("Date start", required=True),
        "date_end": fields.date("Date end", required=True),
        "location_ids": fields.function(_search_locations, relation='tem.listing.bylocation.location', type="many2many", string='Personen'),
    }
    
    _defaults = {
        "date_start": lambda *a: time.strftime('%Y-%m-%d'),
        "date_end": lambda *a: (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
    }
    
tem_listing_bylocation()

