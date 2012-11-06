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
    'name' : 'Merge Picking: Sales Handling (DEPRECATED)',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock_merge_picking','sale','stock_sale_order_references'],
    'category' : 'Generic Modules',
    'description': """
This module allow the merging of picking lists from different Sales Orders and introduces a new relation for tracking them. 

Deprecated due to side effects. We now use stock_picking_group.

    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ["view/sale_view.xml", "view/stock_view.xml"],
    'active': False,
    'installable': True
}
