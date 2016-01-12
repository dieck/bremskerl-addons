
from osv import osv, fields
import re

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = _name
    
    def _get_defaults(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        
        values_obj = self.pool.get('ir.values')
        
        for record in self.browse(cr, uid, ids, context=context):

            incoterm = False 
            incoterms = values_obj.search(cr, uid, [('key','=','default'),
                                            ('key2','=','partner_id='+str(record.id)),
                                            ('model','=','sale.order'),
                                            ('name','=','incoterm')])
            if incoterms:
                value = values_obj.browse(cr, uid, incoterms[0])
                # format for numeric data as this relation is "I<Nr>\n."
                if value.value_unpickle:
                    p = re.compile('I(\d+)[\r\n]\.')
                    m = p.match(value.value_unpickle)
                    if m:
                        incoterm = int(m.group(1)) or False
             
            result[record.id] = {'default_incoterm_id': incoterm}
        return result
   
    _columns = {
        'default_incoterm_id': fields.function(_get_defaults, method=True, multi="default_incoterm_id", readonly=True,
                                type='many2one', relation='stock.incoterms', string="Default Sales Order Incoterm"),
    }
        
            
res_partner()


