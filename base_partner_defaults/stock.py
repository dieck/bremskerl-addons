
from osv import osv, fields
import re

class stock_incoterms(osv.osv):
    _name = "stock.incoterms"
    _inherit = _name
    
    def _get_defaults(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        
        values_obj = self.pool.get('ir.values')
        
        for record in self.browse(cr, uid, ids, context=context):

            incoterm = [] 
            incoterms = values_obj.search(cr, uid, [('key','=','default'),
                                            ('key2','like','partner_id=%'),
                                            # does not work ('value_unpickle','=','I'+str(record.id)+"\n."),
                                            ('model','=','sale.order'),
                                            ('name','=','incoterm')])
            for i in values_obj.browse(cr, uid, incoterms):
                # format for numeric data as this relation is "I<Nr>\n."
                
                # test for I + this_id + [\r\n].
                if i.value_unpickle:
                    p = re.compile('I(\d+)[\r\n]\.')
                    m = p.match(i.value_unpickle)
                    if m:
                        if int(m.group(1)) != record.id:
                            continue
                    # get partner id
                    p = re.compile('partner_id=(\d)')
                    m = p.match(i.key2)
                    if m:
                        # and add numeric id, if ok
                        k2p = int(m.group(1))
                        if k2p:
                            incoterm.append(k2p)
             
            result[record.id] = {'default_partner_id': incoterm}
        return result
   
    _columns = {
        'default_partner_id': fields.function(_get_defaults, method=True, multi="default_partner_id", readonly=True,
                                type='one2many', relation='res.partner', string="Used as default for"),
    }
        
            
stock_incoterms()


