# -*- coding: UTF-8 -*-
'''
@author: Dieckhoff
'''

from osv import osv, fields
import decimal_precision as dp
import time
import pooler
from datetime import datetime, timedelta
from tools.translate import _


class res_user(osv.osv):
    _name = "res.users"
    _inherit = _name

    def _is_tem_inspector(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for u in self.browse(cr, uid, ids):
            res[u.id] = False
            for g in u.groups_id:
                if g.name == "Test Equipment / Inspector":
                    res[u.id] = True
        return res
    
    _columns = {
        "is_tem_inspector": fields.function(_is_tem_inspector, string="Is TEM inspector", type='boolean', method=True,
                                            store={'res.users': (lambda self, cr, uid, ids, c={}: ids, ['groups_id'], 10)}),
                # needs store, otherwise it won't work as domain condition on tem.inspections
    }
res_user()


class tem_res_responsibles(osv.osv):
    _name = "tem.res.responsibles"
    _order = "name"
    
    _columns = {
        "name": fields.char("Name", size=64, required=True),
        "type": fields.selection([('employee','Employee'),
                                 ('department','Department'),
                                 ('manufacturer','Manufacturer'),
                                 ('contractor','Contractor')],
                                "Type", required=True),
        "user_id": fields.many2one('res.users', "User", ondelete='set null'),
        "partner_id": fields.many2one('res.partner', 'Partner', ondelete='set null'),
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
        for rsp in self.browse(cr, uid, ids, context=context):
            if ( (rsp.type == 'employee') and not (rsp.user_id and rsp.user_id.id) ) :
                return False
        return True

    def _check_partnerid(self, cr, uid, ids, context=None):
        for rsp in self.browse(cr, uid, ids, context=context):
            if ( ((rsp.type == 'manufacturer') or (rsp.type == 'contractor')) and not (rsp.partner_id and rsp.partner_id.id) ) :
                return False
        return True
     
    _constraints = [
        (_check_userid, 'For Employee type, you have to set a related user', ['user_id']),
        (_check_partnerid, 'For Manufacturer and Contractor type, you have to set a related partner', ['partner_id']),
    ]

    
tem_res_responsibles()

class tem_res_units(osv.osv):
    _name = "tem.res.units"
    _order = "name"

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
    _name = "tem.location"
    _order = "name"

    _columns = {
        "name": fields.char("Location Name", size=64, required=True),
        "category": fields.selection([('account','Internal Acocunt'),
                                          ('customer','Customer'),
                                          ('supplier','Supplier')],
                                          "Category", required=True),
        "description": fields.char("Description", size=128),
        
        "cost_unit": fields.integer("Cost Unit"),
        "partner_id": fields.many2one("res.partner", "Partner", ondelete='set null'),
        
        "type_storage": fields.boolean("Storage"),
        "type_usage": fields.boolean("Usage Site"),
        "type_calibration": fields.boolean("Calibration Site"),
        "type_rigging": fields.boolean("Rigging Site"),

        "active": fields.boolean("Active"),
        "printreports": fields.boolean("Show on printed reports"),        
    }
    _defaults = {
        "active": lambda *a: True,
        "printreports": lambda *a: True,
    }                      
tem_location()



class tem_equipment_group(osv.osv):
    _name = "tem.equipment.group";
    _order = "name"

    def _get_interval_text(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for grp in self.browse(cr, uid, ids):
            r = "" 
            if (grp.interval):
                r += unicode(grp.interval)
            if (grp.interval_repeat):
                r += u" "+unicode(grp.interval_repeat)
            res[grp.id] = r or False
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
        "measuring_resolution_unit_id": fields.many2one("tem.res.units", "Resolution unit", ondelete='restrict'),
       
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

    # do not delete, just mark deleted  
    def unlink(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'deleted'}, context=context)
        return True
  
    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for eqp in self.browse(cr, uid, ids):
            r = u"" 
            if (eqp.id_number):
                r += unicode(eqp.id_number)
            if (eqp.description):
                r += u" ("+unicode(eqp.description)+")"
            res[eqp.id] = r
        return res
    
    def _is_active(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        for eqp in self.browse(cr, uid, ids):
            res[eqp.id] = ((eqp.state == 'new') or (eqp.state == 'available') or (eqp.state == 'disabled'))
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


    def _get_interval_local_text(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for eq in self.browse(cr, uid, ids):
            r = "" 
            if (eq.interval_local):
                r += unicode(eq.interval_local)
            if (eq.interval_local_repeat):
                r += u" "+unicode(eq.interval_local_repeat)
            res[eq.id] = r or False
        return res

    def _get_interval(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for eq in self.browse(cr, uid, ids):
            if (eq.interval_local):
                res[eq.id] = { 'interval': eq.interval_local,
                               'interval_repeat': eq.interval_local_repeat,
                               'interval_text': eq.interval_local_text,
                              }
            elif (eq.group_id.interval):
                res[eq.id] = { 'interval': eq.group_id.interval,
                               'interval_repeat': eq.group_id.interval_repeat,
                               'interval_text': eq.group_id.interval_text,
                              }
            else:
                res[eq.id] = { 'interval': None,
                               'interval_repeat': None,
                               'interval_text': None,
                              }
        return res
    

    _columns = {
        "id_number": fields.char("TEM Ident no.", size=32, required=True),
        "description": fields.char("Equipment", size=64, required=True),
        
        "name": fields.function(_get_name, string="Equipment name", type='char', size=75, method=True),
        "active": fields.function(_is_active, string="Active", type='boolean', method=True,
                                  store={'tem.equipment': (lambda self, cr, uid, ids, c={}: ids, ['state'], 10)},
                                  help="Active status is derived from the state: scrapped and lost are considered inactive."),

        #char("test1", size=32), 
        #function(_get_name, string="Equipment name", type='char', size=75, method=True),
        "group_id": fields.many2one("tem.equipment.group", "Type", required=True, ondelete='restrict'),
        "interval_local": fields.float("Interval", digits=(8,1) ),
        "interval_local_repeat": fields.selection([
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
        "interval_local_text": fields.function(_get_interval_local_text, string="Interval", type='char', size=50, method=True),
        
        "interval_group_text": fields.related("group_id", "interval_text", type="char", size=50, string="Interval"),
        
        "interval": fields.function(_get_interval, string="Interval", type='float', size=50, method=True, multi='_get_interval'),
        "interval_repeat": fields.function(_get_interval, string="Interval type", type='char', size=50, method=True, multi='_get_interval'),
        "interval_text": fields.function(_get_interval, string="Interval", type='char', size=50, method=True, multi='_get_interval'),
        "interval_origin": fields.function(_get_interval, string="Interval origin", type='char', size=50, method=True, multi='_get_interval'),
        
        "state": fields.selection([
                                   ('new','New'),
                                   ('available','Available'),
                                   ('disabled','Disabled'),
                                   ('scrapped','Scrapped'),
                                   ('lost','Cannot be found'),
                                   ('deleted','Marked deleted'),
                                   ],
                                   "State"),# required=True),
        "manufacturer_id": fields.many2one("res.partner","Manufacturer", ondelete='set null'),
        "measuring_range": fields.char("Range", size=64),
        "measuring_resolution": fields.char("Resolution", size=64, help="Maximal fraction of measurements readings. E.g. a scale might be read in a resolution of 0.1."),
        "measuring_rangeresolution_unit_id": fields.many2one("tem.res.units", "Range & Resolution unit", ondelete='restrict'),
        "measuring_precision": fields.char("Precision", size=64),
        "measuring_precision_unit_id": fields.many2one("tem.res.units", "Precision unit", help="Inherent maximal deviation of measurements. E.g. if a scale reads in a resolution of 0.1, but with 0.2 deviation, the reading 0.5 might be in between 0.3 and 0.7.", ondelete='restrict'),
        
        
        "storage_location": fields.many2one("tem.location", "Storage location", domain=[('type_storage','=',True)], ondelete='restrict'),
        "usage_site": fields.many2one("tem.location", "Usage site", domain=[('type_usage','=',True)], ondelete='restrict'),
        
        "supplier_id": fields.many2one("res.partner","Supplier", domain=[('supplier','=',True)], ondelete='set null'),
        "order_no": fields.char("Order no.", size=64),
        "serial_no": fields.char("Serial no.", size=64),
        "service_contract": fields.char("Service Contract", size=64),
        
        "purchase_date": fields.date("Purchased"),
        "purchase_price": fields.float('Purchase Price', digits_compute=dp.get_precision('TEM Prices')),
        "purchase_currency_id": fields.many2one('res.currency', 'Currency', ondelete='restrict'),
        "purchase_invoice_id": fields.many2one("account.invoice","Purchase Invoice", domain=[('type','=','in_invoice')], ondelete='set null'),
        
        "cal_company_id": fields.many2one("res.partner","Involved Company", domain=[('supplier','=',True)], ondelete='set null'),

        "notes": fields.text("Notes"),
        
    }
    
    _defaults = {
        "state": lambda *a: 'new',
        "measuring_precision_unit_id": _get_percent,
    }
    
    def _check_measuring_rangeresolution_unit_id(self, cr, uid, ids, context=None):
        for eqp in self.browse(cr, uid, ids, context=context):
            if ( ((eqp.measuring_range) or (eqp.measuring_resolution)) and not (eqp.measuring_rangeresolution_unit_id and eqp.measuring_rangeresolution_unit_id.id) ) :
                return False
        return True

    def _check_measuring_precision_unit_id(self, cr, uid, ids, context=None):
        for eqp in self.browse(cr, uid, ids, context=context):
            if ( (eqp.measuring_precision) and not (eqp.measuring_precision_unit_id and eqp.measuring_precision_unit_id.id) ) :
                return False
        return True
     
    _constraints = [
        (_check_measuring_rangeresolution_unit_id, 'If you set a Range or Resolution, you have to set the unit.', ['measuring_range','measuring_resolution','measuring_rangeresolution_unit_id']),
        (_check_measuring_precision_unit_id, 'If you set a Precision, you have to set the unit.', ['measuring_precision','measuring_precision_unit_id']),
    ]
    
    _sql_constraints = [ ('default_idnumber_uniq', 'unique (id_number)', _("Ident no. has to be unique.")), ]

tem_equipment()


class tem_inspection_references(osv.osv):
    _name = "tem.inspection.references"

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for ref in self.browse(cr, uid, ids):
            res[ref.id] = unicode(ref.group_id.name) + u" " + unicode(ref.property) + u": " + unicode(ref.reference_value)
        return res

    _columns = {
        "name": fields.function(_get_name, string="Reference Value", type='char', size=100, method=True,),    
        "group_id": fields.many2one("tem.equipment.group", "Type", required=True, ondelete='cascade'),
        "property": fields.char("Property", help="Short note on what to measure", size=50, required=True, translate=True),
        "reference_value": fields.char("Reference Value", size=50, required=True),
        "unit_id": fields.many2one("tem.res.units", "Unit"),
        "boundary_lower": fields.char("Lower Boundary", size=50),
        "boundary_upper": fields.char("Upper Boundary", size=50),
        "apply_to": fields.char("Apply To", size=50,
                                help="Notes on when to apply this reference value, if some reference values do not apply to all items in the equipment group."),
    }
tem_inspection_references()

class tem_inspection_tools(osv.osv):
    _name = "tem.inspection.tools"

    _columns = {
        "name": fields.char("Description", size=150, required=True),    
        "equipment_id": fields.many2one("tem.equipment", "Equipment", ondelete='set null'),
    }
tem_inspection_tools()


class tem_inspection(osv.osv):
    _name = "tem.inspection"
    _order = "date DESC"

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for insp in self.browse(cr, uid, ids):
            r = [] 
            if (insp.date):
                r.append(unicode(insp.date))
            if (insp.result):
                r.append(unicode(insp.result))
            if (insp.equipment_id):
                r.append(unicode(insp.equipment_id.name))
            res[insp.id] = u" // ".join(r)
        return res
    
    
    def _get_interval_text(self, cr, uid, equipment_id):
        if not equipment_id:
            return False
        eq_obj = self.pool.get('tem.equipment')
        eqp = eq_obj.browse(cr, uid, equipment_id)
        return eqp.interval_text
              

    def _get_next_real_date(self, dt, day, month, year):
        count = 0
        # go back at max a full week
        while (count < 7):
            count += 1                
            try:
                dnew = dt.replace(day=day, month=month, year=year)
                return dnew
            except ValueError:
                # just change the days, so "Last of Month" will be "Last of Month in $month mon"
                if (day > 0):
                    day -= 1
                else:
                    day = 1
        return dt

    def _get_next_date(self, cr, uid, context={}, equipment_id={}):
        # datetime object for deriving the default next test date
        dt = datetime.today()
        
        # we need to have an equipment_id.
        # Either from context, or by variable from on_change
        eqid = None
        
        if (equipment_id):
            eqid = equipment_id
                            
        if (context.get('active_model','') == 'tem.equipment'):
            eqid = context.get('equipment_id', context.get('active_id', None))

        # no equipment set? direct access, not coming from eq        
        if (not eqid):
            # return current date/time
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        equipment = self.pool.get('tem.equipment').browse(cr, uid, [eqid], context=context)[0]
        
        # get interval count and type
        intvl =  equipment and equipment.interval or 0
        intvl_type = equipment and equipment.interval_repeat or None

        # nothing to do? return "today"
        if (intvl == 0 or intvl_type is None):
            return time.strftime('%Y-%m-%d %H:%M:%S') 
         
        # year and month are directly converted
        if (intvl_type == 'yr'):
            dt = dt.replace(year=(dt.year + intvl))

        elif (intvl_type == 'mon'):
            
            dmon = dt.month + intvl
            dyr = dt.year
            while (dmon > 12): # convert month to years
                dyr += 1
                dmon -= 12
	    # Problem (#15740): will not recalculate days, so "day is out of range for month" error may occur, e.g. with 31st February
            dt = self._get_next_real_date(dt, day=dt.day, month=int(dmon), year=dyr)
        
        else:
            # week, days, hours and minutes are handled via timedelta (got problems with days in months otherwise :))
            td = timedelta(days=0)
                            
            if (intvl_type == 'wk'):
                td = timedelta(weeks=intvl)
                
            elif (intvl_type == 'dy'):
                td = timedelta(days=intvl)
                
            elif (intvl_type == 'hr'):
                td = timedelta(hours=intvl)
            
            elif (intvl_type == 'min'):
                td = timedelta(minutes=intvl)

            # calculate new date
            dt = dt + td

        # if it's a Saturday or Sunday, set to Friday before (test equipment needs to be prepared for start of work on Monday)
        # TODO make configurable (with install wizard?)
        if (dt.weekday() > 4): # Saturday = 5, Sunday = 6
            dt -= timedelta(days=dt.weekday()-4)

        return dt.strftime('%Y-%m-%d %H:%M:%S')

               
    def on_change_equipment_id(self, cr, uid, ids, equipment_id):
        return {'value': {'interval_text': self._get_interval_text(cr, uid, equipment_id),
                          'next': self._get_next_date(cr, uid, equipment_id=equipment_id),
                          'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                          'references_ids': self._get_references_ids_defaults(cr, uid, {'active_model':'tem.equipment','active_id':equipment_id}),
                          }}
    
    def _get_references_ids(self, cr, uid, ids, field_name, arg, context={}):
        result = {}
        for insp in self.browse(cr, uid, ids, context=context):
            r = []
            if (insp.equipment_id):
                if (insp.equipment_id.group_id):
                    for rf in insp.equipment_id.group_id.references_ids:
                        r.append(rf.id)
            result[insp.id] = r
        return result
    
    def _get_references_ids_defaults(self, cr, uid, context=None):
        # button click: _get_references_ids_defaults context {'lang': 'de_DE', 'tz': False, 'active_model': 'tem.equipment', 'search_default_Active': 1, 'active_ids': [468], 'active_id': 468}
        # new on one2many widget:_get_references_ids_defaults, context {'lang': 'de_DE', 'equipment_id': 1129, 'tz': False}

        if (not context):
            # no context? no active_ids, no data to show
            return []

        eqid = context.get('equipment_id', None)

        if (not eqid):
            if (context.get('active_model','') == 'tem.equipment'):
                eqid = context.get('active_id',None)

        if (not eqid):
            # neither new nor button clicked
            return []

        equipment_obj = self.pool.get("tem.equipment")
        eq = equipment_obj.browse(cr, uid, eqid, context=context)

        if (not eq):
            # could not browse active id
            return []

        res = []
        # group_id is required, so no check neccessary
        for rf in eq.group_id.references_ids:
            res.append(rf.id)
        return res


    
    
    _columns = {
        "name": fields.function(_get_name, string="Inspection", type='char', size=100, method=True),
        "equipment_id": fields.many2one("tem.equipment", "Equipment", required=True, ondelete='restrict'),
        "by_id": fields.many2one("res.users", "Inspected by", required=True, ondelete='restrict', domain=[("is_tem_inspector","=",True)] ),
        "date": fields.datetime("Inspection date", required=True),
        "next": fields.datetime("Next Inspection Due", required=True),
        "interval_text": fields.related("equipment_id", "interval_text",  type='char', string="Scheduled Interval", readonly=True),
        "description": fields.char("Short Description", size=64, translate=True,),
        "result": fields.selection([("defer","Deferred"),("pass","Passed"),("fail","Failed")], "Inspection Result", required=True),
        "maint": fields.boolean("Needs Maintenance/Repair"),
        "scrap": fields.boolean("To be scrapped"),
        "notes": fields.text("Notes"),
        "tool_id": fields.many2one("tem.inspection.tools", string="Tool", help="Tool (appliance/calibre) used to calibrate the test equipment.", required=True),
        "references_ids": fields.function(_get_references_ids, string="Reference values", type='many2many', relation="tem.inspection.references", method=True),
    }

    _defaults = {
        "references_ids": _get_references_ids_defaults,
        "date": lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        "next": _get_next_date,
        "by_id": lambda self,cr,uid,context: uid,
    }
    

    # set equipment state to available on pass, disabled on fail    
    def create(self, cr, uid, data, context=None):
        # create inspection first
        created = super(tem_inspection, self).create(cr, uid, data, context)
        
        # look for result settings
        state = None
        if (data.get('result','') == 'pass'):
            state = "available"
        if (data.get('result','') == 'fail'):
            state = "disabled"
            # will be scrapped? only on failed
            if (data.get('scrap',False)):
                state = "scrapped"
        # at defer, stay the same

               
        # nothing to do?
        if (state == None):
            return created
               
        # read equipment id from inspection
        insp = self.browse(cr, uid, created, context=context)
        eqid = insp and insp.equipment_id and insp.equipment_id.id
        
        if (not eqid):
            # should never happen, but better to be sure than sorry
            return created
        
        eqstate = insp and insp.equipment_id and insp.equipment_id.state
        
        if (eqstate == state):
            # nothing changed
            return created
        
        # change state
        eq_obj = self.pool.get('tem.equipment')
        eq_obj.write(cr, uid, [eqid], {'state': state}, context=context)
        return created


    # set equipment state to available on pass, disabled on fail    
    def write(self, cr, uid, ids, vals, context=None):
        # write data
        written = super(tem_inspection, self).write(cr, uid, ids, vals, context=context)
        
        # if result was not changed, do nothing
        if (vals.get('result','') == ''):
            return written

        eq_obj = self.pool.get('tem.equipment')
        
        # read equipment id from inspection
        for insp in self.browse(cr, uid, ids, context=context):
            eqid = insp and insp.equipment_id and insp.equipment_id.id
            eqstate = insp and insp.equipment_id and insp.equipment_id.state

            # look for result settings
            state = None
            if (insp.result == 'pass'):
                state = "available"
            if (insp.result == 'fail'):
                state = "disabled"
                # will be scrapped? only on failed
                if (insp.scrap):
                    state = "scrapped"
            # at defer, stay the same
        
            # nothing to do
            if (eqstate == state):
                continue
            
            # change state
            eq_obj.write(cr, uid, [eqid], {'state': state}, context=context)
            
        return written
        
    
tem_inspection()


class tem_inspection_measurements(osv.osv):
    _name = "tem.inspection.measurements"
    _order = "date"

    def _get_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for insp in self.browse(cr, uid, ids):
            r = [] 
            if (insp.measurement):
                r.append(unicode(insp.measurement) + u" " + unicode(insp.measurement_unit_id.name))
            if (insp.note):
                r.append(unicode(insp.note))
            if not r:
                r = [u'Name update follows']
            res[insp.id] = unicode(" // ").join(r)
        return res
    
    _columns = {
        "name": fields.function(_get_name, string="Inspection", type='char', size=100, method=True,),    
        "inspection_id": fields.many2one("tem.inspection", "Inspection", required=True, ondelete='cascade'),
        "user_id": fields.many2one("res.users", "Inspected by", required=True, ondelete='restrict'),
        "date": fields.datetime("Inspection date", required=True),
        "property": fields.char("Property", size=50, required=True, translate=True),
        "measurement": fields.float("Measurement"),
        "measurement_unit_id": fields.many2one("tem.res.units","Unit", ondelete='restrict'),
        "note": fields.char("Note",size=250),
    }
    
    _defaults = {
        "date": lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        "user_id": lambda self,cr,uid,context: uid,
        "property": _('Property'),
    }
    
    def _check_measuring_unit_id(self, cr, uid, ids, context=None):
        for msr in self.browse(cr, uid, ids, context=context):
            if ( (msr.measurement) and not (msr.measurement_unit_id and msr.measurement_unit_id.id) ) :
                return False
        return True
     
    _constraints = [
        (_check_measuring_unit_id, 'If you set a measurement value, you have to set the unit.', ['measurement','measurement_unit_id']),
    ]
    
tem_inspection_measurements()

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
        for eqp in self.browse(cr, uid, ids):
            cr.execute("SELECT MAX(date) FROM tem_inspection WHERE equipment_id=%s", (eqp.id,))
            res[eqp.id] = cr.fetchone()[0] or False
        return res
    
    def _get_next_inspection(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for eqp in self.browse(cr, uid, ids):
            cr.execute("SELECT DATE_PART('epoch',MAX(next)) FROM tem_inspection WHERE equipment_id=%s", (eqp.id,))
            next_inspection = cr.fetchone()[0] or False
            res[eqp.id] = {'next_inspection': (datetime.fromtimestamp(next_inspection)).strftime('%Y-%m-%d'), 
                           'inspection_due': (next_inspection <= time.time()),
                           'inspection_soon': ((next_inspection > time.time()) and (next_inspection <= (time.time()+14*24*60*60) ) ),
                           }
        return res
    
    _columns = {
        "inspection_ids": fields.one2many("tem.inspection","equipment_id","Inspections"),
                                         
        "last_inspection": fields.function(_get_last_inspection, string="Last Inspection", type='date', method=True,
                                           store={'tem.inspection':(_get_equipment_from_inspection,['date'],10)}),
        "next_inspection": fields.function(_get_next_inspection, string="Next Inspection", type='date', method=True, multi='_get_next_inspection',
                                           store={'tem.inspection':(_get_equipment_from_inspection,['next'],10)}),
        "inspection_due": fields.function(_get_next_inspection, string="Next Inspection due", type='boolean', method=True, multi='_get_next_inspection',
                                           store={'tem.inspection':(_get_equipment_from_inspection,['next'],10)}),
        "inspection_soon": fields.function(_get_next_inspection, string="Next Inspection soon", type='boolean', method=True, multi='_get_next_inspection',
                                           store={'tem.inspection':(_get_equipment_from_inspection,['next'],10)}),
    }
tem_equipment_update1()



class tem_equipment_group_o2m(osv.osv):
    _name = "tem.equipment.group";
    _inherit = _name
    
    _columns = {
        "equipment_ids": fields.one2many("tem.equipment","group_id","Equipment"),
        "references_ids": fields.one2many("tem.inspection.references","group_id","Reference values"),
    }                                
    
tem_equipment_group_o2m()

class tem_location_o2m(osv.osv):
    _name = "tem.location";
    _inherit = _name
     
    def _get_related_equipments(self, cr, uid, ids, field_name, arg, context):
        res = {}
        equipment_obj = self.pool.get("tem.equipment")
        for loc in self.browse(cr, uid, ids):
            li = []
            
            storage_ids = equipment_obj.search(cr, uid, [('storage_location.id','=',loc.id)], context=context)
            li.extend(storage_ids)
            
            usage_ids = equipment_obj.search(cr, uid, [('usage_site.id','=',loc.id)], context=context)
            li.extend(usage_ids)
            
            res[loc.id] = li
        return res
    
    _columns = {
        "related_equipment_ids": fields.function(_get_related_equipments, type='one2many', obj='tem.equipment', method=True, string="Related Equipment",),
    }                                
        
tem_location_o2m()

class tem_inspection_o2m(osv.osv):
    _name = "tem.inspection";
    _inherit = _name
    
    _columns = {
        "measurement_ids": fields.one2many("tem.inspection.measurements","inspection_id","Measurements"),
    }       
    
    def _check_measurements(self, cr, uid, ids):
        for insp in self.browse(cr, uid, ids):
            if ((insp.result == "pass") or (insp.result == "fail")):
                if (len(insp.measurement_ids)<1):
                    return False
        return True
    
    _constraints = [
        (_check_measurements, "\n\n" + 'You need to set at least one measurement on a passed or failed inspection.' + "\n", ['measurement_ids']),
    ]
     
tem_inspection_o2m()    



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
        "date_end": lambda *a: (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
    }
    
tem_listing_bylocation()

