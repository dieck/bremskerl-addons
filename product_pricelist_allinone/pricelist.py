# -*- encoding: utf-8 -*-

from osv import fields,osv

class product_pricelist(osv.osv):
    _inherit = "product.pricelist"
    _name = _inherit
    
    def _ppaio_partner_ids(self,cr,uid,ids,field,arg,context=None):
        res = {}
        
        partner_obj = self.pool.get('res.partner')
        allpartners = partner_obj.search(cr, uid, [], context=context)
        
        for pricelist in self.browse(cr,uid,ids,context=context):
            partnerids = []
            
            for partner in partner_obj.browse(cr,uid,allpartners,context=context):
                prclstid = partner.property_product_pricelist and partner.property_product_pricelist.id or False
                if (prclstid):
                    if (prclstid == pricelist.id):
                        partnerids.append(partner.id)
                    
            res[pricelist.id] = partnerids
        return res
    
    _columns = {
        "partner_ids": fields.function(_ppaio_partner_ids,type='one2many',relation="res.partner",string="Partners",method=True),
    }
    
product_pricelist()

class product_pricelist_item(osv.osv):
    _inherit = "product.pricelist.item"
    _name = _inherit
    
    def _ppaio_partner_names(self,cr,uid,ids,field,arg,context=None):
        res = {}
        for pricelistitem in self.browse(cr,uid,ids,context=context):
            partnernames = []
            for partner in pricelistitem.partner_ids:
                partnernames.append(partner.name)
            res[pricelistitem.id] = ", ".join(partnernames)
        return res
    
    _columns = {
        "price_version_name": fields.related("price_version_id", "name", readonly=True, type="char", string="Version Name"),
        "price_version_date_start": fields.related("price_version_id", "date_start", readonly=True, type="date", string="Version Start"),
        "price_version_date_end": fields.related("price_version_id", "date_end", readonly=True, type="date", string="Version End"),
        "price_version_active": fields.related("price_version_id", "active", readonly=True, type="boolean", string="Version Active"),
        
        "pricelist_id": fields.related("price_version_id", "pricelist_id", readonly=True, type="many2one", relation="product.pricelist", string="Pricelist"),

        "pricelist_idid": fields.related("price_version_id", "pricelist_id", "name", readonly=True, type="integer", string="List ID"),
        "pricelist_name": fields.related("price_version_id", "pricelist_id", "name", readonly=True, type="char", string="List Name"),
        "pricelist_type": fields.related("price_version_id", "pricelist_id", "type", readonly=True, type="char", string="List Type"),
        "pricelist_cur": fields.related("price_version_id", "pricelist_id", "currency_id", readonly=True, type="many2one", relation="res.currency", string="List Currency"),

        "partner_ids": fields.related("price_version_id", "pricelist_id", "partner_ids", type='one2many', relation="res.partner", string="Partners"),
        "partner_names": fields.function(_ppaio_partner_names,type='string',size="250",string="Partners",method=True),
    
        }

product_pricelist_item()
