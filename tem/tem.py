# -*- coding: UTF-8 -*-
'''
@author: Dieckhoff
'''

from osv import osv, fields
import decimal_precision as dp
import time
import pooler
from datetime import datetime, timedelta

class tem_res_responsibles(osv.osv):
    _name = "tem.res.responsibles"
    _columns = {
        "name": fields.char("Name", size=64, required=True),
        "type": fields.selection([('employee','Employee'),
                                 ('department','Department'),
                                 ('manufacturer','Manufacturer'),
                                 ('contractor','Contractor')],
                                "Type", required=True),
        "user_id": fields.many2one('res.users', "User"),
        "partner_id": fields.many2one('res.partner', 'Partner'),
        "description": fields.char("Description", size=256, translate=True,),
        "active": fields.boolean('Active', required=True),
    }
  
    _defaults = {
        "active": lambda *a: True,
        "type": lambda *a: "employee",
    }
    
    _sql_constraints = [
        ('name_uniq', 'unique (name)', """Responsibles Name has to be unique."""),
    ]

    def _check_userid(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            if ( (session.type == 'employee') and not (session.user_id and session.user_id.id) ) :
                return False
        return True

    def _check_partnerid(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            if ( ((session.type == 'manufacturer') or (session.type == 'contractor')) and not (session.partner_id and session.partner_id.id) ) :
                return False
        return True
     
    _constraints = [
        (_check_userid, 'For Employee type, you have to set a related user', ['user_id']),
        (_check_partnerid, 'For Manufacturer and Contractor type, you have to set a related partner', ['partner_id']),
    ]

    
tem_res_responsibles()

class tem_res_units(osv.osv):
    _name = "tem.res.units"
    _columns = {
        "name": fields.char("Unit", size=64, required=True),
        "description": fields.char("Description", size=64, translate=True,),
        "active": fields.boolean('Active'),
    }
    _defaults = {
        "active": lambda *a: True,
    }
tem_res_units()

class tem_location(osv.osv):
    _name = "tem.location";
    _columns = {
        "name": fields.char("Location Name", size=64, required=True),
        "category": fields.selection([('account','Internal Acocunt'),
                                          ('customer','Customer'),
                                          ('supplier','Supplier')],
                                          "Category", required=True),
        "description": fields.char("Description", size=128),
        
        "cost_unit": fields.integer("Cost Unit"),
        
        "type_storage": fields.boolean("Storage"),
        "type_usage": fields.boolean("Usage Site"),
        "type_calibration": fields.boolean("Calibration Site"),
        "type_rigging": fields.boolean("Rigging Site"),

        "incoming_due": fields.boolean("Incoming Due", help="Equipment is due to inspection when incoming to this location"),
        "never_due": fields.boolean("Never Due", help="Equipment is never due in this location"),
        
        "active": fields.boolean("Active"),    
    }
    _defaults = {
        "active": lambda *a: True,
    }                      
tem_location()



class tem_equipment_group(osv.osv):
    _name = "tem.equipment.group";

    def _get_interval_text(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            r = "" 
            if (session.interval):
                r += str(session.interval)
            if (session.interval_repeat):
                r += " "+str(session.interval_repeat)
            res[session.id] = r or False
        return res
    
    _columns = {
        "name": fields.char("Group", size=64, required=True, translate=True),
        "standard": fields.char("Test standard", size=64, translate=True),
        "standard_link": fields.char("Test standard specifications", size=260),
        "interval": fields.float("Interval", digits=(8,1) ),
        "interval_repeat": fields.selection([
                                   ('prdord','Production Orders'),
                                   ('need','as needed'),
                                   ('wh','Working Hours'),
                                   ('prdcycl','Production Cycle'),
                                   ('yr','Years'),
                                   ('delbt','Delivery Batches'),
                                   ('min','Minutes'),
                                   ('mon','Months'),
                                   ('inspord','Inspection Orders'),
                                   ('qrt','Quarter'),
                                   ('sec','Moved'),
                                   ('hr','Hours'),
                                   ('dy','Days'),
                                   ('wk','Weeks')],
                                   "Interval type", ), # required=True has to be set on view, is no sql "NOT NULL"
        "interval_text": fields.function(_get_interval_text, string="Interval", type='char', size=50, method=True),
        "measuring_range": fields.char("Range", size=64),
        "measuring_resolution": fields.char("Resolution", size=64),
        "measuring_resolution_unit_id": fields.many2one("tem.res.units", "Resolution unit"),
       
        "inspection_plan": fields.text("General Inspection Plan", translate=True),
        "notes": fields.text("Notes"),


        "active": fields.boolean("Active"),    
    }
    
    _defaults = {
        "active": lambda *a: True,
    }
tem_equipment_group()
 



class tem_equipment(osv.osv):
    _name = "tem.equipment"
  
    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            r = "" 
            if (session.id_number):
                r += str(session.id_number)
            if (session.description):
                r += " ("+str(session.description)+")"
            res[session.id] = r
        return res
    
    def _is_active(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            res[session.id] = ((session.state == 'new') or (session.state == 'available') or (session.state == 'disabled'))
        return res

    # _get_currency        
    # @author: from account.invoice,     
    # @copyright: Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
    def _get_currency(self, cr, uid, context=None):
        user = pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, [uid], context=context)[0]
        if user.company_id:
            return user.company_id.currency_id.id
        return pooler.get_pool(cr.dbname).get('res.currency').search(cr, uid, [('rate','=', 1.0)])[0]
    
    
    def _get_percent(self, cr, uid, context=None):
        units = pooler.get_pool(cr.dbname).get('tem.res.units')
        percent = units.search(cr, uid, [('name','=','%')], context=context)
        for u in units.browse(cr, uid, percent, context=context):
            return u.id
        return False

        
    _columns = {
        "id_number": fields.char("TEM Ident no.", size=32, required=True),
        "description": fields.char("Equipment", size=64, required=True),
        
        "name": fields.function(_get_name, string="Equipment name", type='char', size=75, method=True),
        "active": fields.function(_is_active, string="Active", type='boolean', method=True),

        #char("test1", size=32), 
        #function(_get_name, string="Equipment name", type='char', size=75, method=True),
        "group_id": fields.many2one("tem.equipment.group", "Type", required=True),
        "interval_text": fields.related("group_id", "interval_text",  type='char', string="Interval", readonly=True),
        "state": fields.selection([
                                   ('new','New'),
                                   ('available','Available'),
                                   ('disabled','Disabled'),
                                   ('scrapped','Scrapped'),
                                   ('lost','Cannot be found'),
                                   ],
                                   "State"),# required=True),
        "manufacturer_id": fields.many2one("res.partner","Manufacturer"),
        "measuring_range": fields.char("Range", size=64),
        "measuring_resolution": fields.char("Resolution", size=64, help="Maximal fraction of measurements readings. E.g. a scale might be read in a resolution of 0.1."),
        "measuring_rangeresolution_unit_id": fields.many2one("tem.res.units", "Range & Resolution unit"),
        "measuring_precision": fields.char("Precision", size=64),
        "measuring_precision_unit_id": fields.many2one("tem.res.units", "Precision unit", help="Inherent maximal deviation of measurements. E.g. if a scale reads in a resolution of 0.1, but with 0.2 deviation, the reading 0.5 might be in between 0.3 and 0.7."),
        
        
        "storage_location": fields.many2one("tem.location", "Storage location", domain=[('type_storage','=',True)]),
        "usage_site": fields.many2one("tem.location", "Usage site", domain=[('type_usage','=',True)]),
        
        "supplier_id": fields.many2one("res.partner","Supplier", domain=[('supplier','=',True)]),
        "order_no": fields.char("Order no.", size=64),
        "serial_no": fields.char("Serial no.", size=64),
        "service_contract": fields.char("Service Contract", size=64),
        
        "purchase_date": fields.date("Purchased"),
        "purchase_price": fields.float('Purchase Price', digits_compute=dp.get_precision('TEM Prices')),
        "purchase_currency_id": fields.many2one('res.currency', 'Currency'),
        "purchase_invoice_id": fields.many2one("account.invoice","Purchase Invoice", domain=[('type','=','in_invoice')]),
        
        "cal_responsible_id": fields.many2one("tem.res.responsibles","Responsible"),
        "cal_company_id": fields.many2one("res.partner","Involved Company", domain=[('supplier','=',True)]),

        "notes": fields.text("Notes"),
        
    }
    
    _defaults = {
        "situation": lambda *a: 'new',
        "measuring_precision_unit_id": _get_percent,
    }
    
    def _check_measuring_rangeresolution_unit_id(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            if ( ((session.measuring_range) or (session.measuring_resolution)) and not (session.measuring_rangeresolution_unit_id and session.measuring_rangeresolution_unit_id.id) ) :
                return False
        return True

    def _check_measuring_precision_unit_id(self, cr, uid, ids, context=None):
        for session in self.browse(cr, uid, ids, context=context):
            if ( (session.measuring_precision) and not (session.measuring_precision_unit_id and session.measuring_precision_unit_id.id) ) :
                return False
        return True
     
    _constraints = [
        (_check_measuring_rangeresolution_unit_id, 'If you set a Range or Resolution, you have to set the unit.', ['measuring_range','measuring_resolution','measuring_rangeresolution_unit_id']),
        (_check_measuring_precision_unit_id, 'If you set a Precision, you have to set the unit.', ['measuring_precision','measuring_precision_unit_id']),
    ]
    
    _sql_constraints = [ ('default_idnumber_uniq', 'unique (id_number)', """Ident no. has to be unique."""), ]

tem_equipment()


class tem_inspection(osv.osv):
    _name = "tem.inspection"
    
    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            r = [] 
            if (session.date):
                r.append(str(session.date))
            if (session.result):
                r.append(str(session.result))
            if (session.equipment_id):
                r.append(str(session.equipment_id.name))
            res[session.id] = " // ".join(r)
        return res
    
    def on_change_equipment_id(self, cr, uid, ids, equipment):
        if not equipment:
            return {'value': {'interval_text': False}}
        eq_ids = self.pool.get('tem.equipment')
        for eq in eq_ids.browse(cr, uid, [equipment]):
            data = {'interval_text': eq.interval_text}
        return {'value': data}
    
    _columns = {
        "name": fields.function(_get_name, string="Inspection", type='char', size=100, method=True),
        "equipment_id": fields.many2one("tem.equipment", "Equipment", required=True),
        "by_id": fields.many2one("res.users", "Inspected by", required=True),
        "date": fields.datetime("Inspection date", required=True),
        "next": fields.datetime("Next Inspection Due", required=True),
        "interval_text": fields.related("equipment_id", "interval_text",  type='char', string="Scheduled Interval", readonly=True),
        "description": fields.char("Short Description", size=64, translate=True,),
        "result": fields.selection([("defer","Deferred"),("pass","Passed"),("fail","Failed")], "Inspection Result", required=True),
        "maint": fields.boolean("Needs Maintenance/Repair"),
        "scrap": fields.boolean("To be scrapped"),
        "notes": fields.text("Notes"),
    }


    def default_get(self, cr, uid, fields_list, context=None):
        res = super(tem_inspection, self).default_get(cr, uid, fields_list, context)
#        print "res",res
#        print "context", context
#        print "fields_list", fields_list
        
        #self.compute_date(cr, uid, context=context)
        return res

    def _get_next_date(self, cr, uid, context):
        equipment = self.pool.get('tem.equipment').browse(cr, uid, [context['equipment_id']], context=context)[0]
        
        # get interval count and type
        intvl =  equipment and equipment.group_id and equipment.group_id.interval or 0
        intvl_type = equipment and equipment.group_id and equipment.group_id.interval_repeat or None

        # nothing to do? return "today"
        if (intvl == 0 or intvl_type is None):
            return time.strftime('%Y-%m-%d %H:%M:%S') 
        
        # datetime object for deriving the default next test date
        dt = datetime.today()
       
         
        # year and month are directly converted
        if (intvl_type == 'yr'):
            dt = dt.replace(year=(dt.year + intvl))

        elif (equipment and equipment.group_id and equipment.group_id.interval_repeat == 'mon'):
            
            dmon = dt.month + intvl
            dyr = dt.year
            while (dmon > 12): # convert month to years
                dyr += 1
                dmon -= 12
            dt = dt.replace(year=dyr,month=int(dmon))
        
        else:
            # week, days, hours and minutes are handled via timedelta (got problems with days in months otherwise :))
            td = timedelta(days=0)
                
            if (equipment and equipment.group_id and equipment.group_id.interval_repeat == 'wk'):
                td = timedelta(weeks=intvl)
                
            elif (equipment and equipment.group_id and equipment.group_id.interval_repeat == 'dy'):
                td = timedelta(days=intvl)
                
            elif (equipment and equipment.group_id and equipment.group_id.interval_repeat == 'hr'):
                td = timedelta(hours=intvl)
            
            elif (equipment and equipment.group_id and equipment.group_id.interval_repeat == 'min'):
                td = timedelta(minutes=intvl)

            # calculate new date
            dt = dt + td


        # if it's a Saturday or Sunday, set to Friday before (test equipment needs to be prepared for start of work on Monday)
        # TODO make configurable (with install wizard?)
        if (dt.weekday() > 4): # Saturday = 5, Sunday = 6
            dt -= timedelta(days=dt.weekday()-4)

        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    _defaults = {
        "date": lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        "next": _get_next_date,
    }
tem_inspection()


class tem_equipment_update1(osv.osv):
    _name = "tem.equipment"
    _inherit = "tem.equipment" 
    _order = "next_inspection"
    
    def _get_equipment_from_inspection(self, cr, uid, ids, context={}):
        res = {}
        insp_ids = self.pool.get('tem.inspection').browse(cr,uid,ids,context=context)
        for i in insp_ids:
            res[i.equipment_id.id] = True
        return res.keys()

    def _get_last_inspection(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            cr.execute("SELECT MAX(date) FROM tem_inspection WHERE equipment_id=%s", (session.id,))
            res[session.id] = cr.fetchone()[0] or False
        return res
    
    def _get_next_inspection(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for session in self.browse(cr, uid, ids):
            cr.execute("SELECT DATE_PART('epoch',MAX(next)) FROM tem_inspection WHERE equipment_id=%s", (session.id,))
            next_inspection = cr.fetchone()[0] or False
            res[session.id] = {'next_inspection': (datetime.fromtimestamp(next_inspection)).strftime('%Y-%m-%d'), 'inspection_due': (next_inspection <= time.time()) }
        return res
    
    _columns = {
        "inspection_ids": fields.one2many("tem.inspection","equipment_id","Inspections"),
                                         
        "last_inspection": fields.function(_get_last_inspection, string="Last Inspection", type='date', method=True,
                                           store={'tem.inspection':(_get_equipment_from_inspection,['date'],10)}),
        "next_inspection": fields.function(_get_next_inspection, string="Next Inspection", type='date', method=True, multi='_get_next_inspection',
                                           store={'tem.inspection':(_get_equipment_from_inspection,['next'],10)}),
        "inspection_due": fields.function(_get_next_inspection, string="Next Inspection due", type='boolean', method=True, multi='_get_next_inspection',
                                           store={'tem.inspection':(_get_equipment_from_inspection,['next'],10)}),
    }
tem_equipment_update1()




