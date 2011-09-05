# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    'name' : 'Sales Order References overview for merged of picked pickings',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock','sale'],
    'category' : 'Generic Modules',
    'description': """
This module presents an overview for merged or (re-)picked pickings.
Merges are done by stock_merge_picking module, recombined picks are done by stock_picking_picker.
    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ["view/stock_view.xml"],
    'active': False,
    'installable': True
}
