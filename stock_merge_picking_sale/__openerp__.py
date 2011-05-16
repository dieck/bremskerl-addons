# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
#
#    Merge Picking up to v5 of OpenERP was written by Axelor, www.axelor.com
#    This is a complete rewrite.
#
##############################################################################
{
    'name' : 'Merge Picking: Sales Handling',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock_merge_picking','sale'],
    'category' : 'Generic Modules',
    'description': """
This module allow the merging of picking lists from different Sales Orders and introduces a new relation for tracking them. 
    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ["view/sale_view.xml", "view/stock_view.xml"],
    'active': False,
    'installable': True
}
