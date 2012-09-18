# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2012+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "View defaults set for this specific partner",
    "version": "1.0",
    "depends": ["base", "stock"],
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    "category": "Base",
    "description": """View defaults set for this specific partner
        As of now, shows: Incoterms (including backlink from stock incoterms)
    """,
    "init_xml": [],
    'update_xml': ["view/partner_view.xml",
                   "view/stock_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}