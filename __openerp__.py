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
    "name": "Add multiple notes to partners, to be added on documents",
    "version": "1.0",
    "depends": ["base"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Base",
    "description": """Add multiple notes to partners, to be added on documents
    """,
    "init_xml": [],
    'update_xml': ["view/partner_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}