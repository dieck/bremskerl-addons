# -*- coding: utf-8 -*-

from osv import osv, fields

class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'
    _name = 'mrp.bom'

    _columns = {
        'raw_materials_location_id': fields.many2one('stock.location', 'Raw Materials Location'),
    }

mrp_bom()
