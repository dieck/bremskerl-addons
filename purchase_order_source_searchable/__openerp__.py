# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "View Purchase Orders: Source document always directly searchable",
    "version": "1.0",
    "depends": ["purchase"],
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    "category": "Purchases",
    "description": """
    View Purchase Orders: Source document always directly searchable
    """,
    "init_xml": [],
    'update_xml': [
                   "view/purchase_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}