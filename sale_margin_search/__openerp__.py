# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2013+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Adds type and customer/supplier selection to invoice analysis",
    "version": "1.0",
    "depends": ["sale_margin"],
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    "category": "Sales & Purchases",
    "description": """Adds type and customer/supplier selection to invoice analysis, and adds menu items for direct access""",
    "init_xml": [],
    'update_xml': ["report/report_margin_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}
