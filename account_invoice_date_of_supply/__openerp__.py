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
    "name": "Adds a field for date of supply / service rendered to invoice lines",
    "version": "1.0",
    "depends": ["account"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Finance",
    "description": "Adds a field for date of supply / service rendered to invoice lines",
    "init_xml": [],
    'update_xml': ["view/account_invoice_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}