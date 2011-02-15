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
    "name": "Add external accounting references to partners",
    "version": "1.01",
    "depends": ["base"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Base",
    "description": """Add mandatory external accounting references to partners.
    """,
    "init_xml": [],
    'update_xml': ["view/partner_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}