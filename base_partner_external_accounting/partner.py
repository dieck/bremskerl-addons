
from osv import osv, fields

class base_partner_external_accounting_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'creditor': fields.char("Creditor ID", size=10),
        'debtor': fields.char("Debtor ID", size=10),
    }
        
    def _check_creditor_or_debtor(self, cr, uid, ids):
        for session in self.browse(cr, uid, ids):
            if (not ((session.creditor) or (session.debtor))):
                return False
        return True
    
    _constraints = [(_check_creditor_or_debtor,
                     'You must either set creditor or debtor reference.',
                     ['creditor','debtor'])
                ]    
            
base_partner_external_accounting_partner()
