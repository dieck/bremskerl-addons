# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2012+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################

{
    'name' : 'Group Pickings',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock'],
    'category' : 'Warehouse',
    'description': """
This module allows you to group stock pickings (Incoming Shipments, Delivery Orders, Internal Moves).

Only type (in, out, internal) and address must be the same to allow grouping,
in order to print a single set of delivery papers for multiple transactions.

    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['security/ir.model.access.csv',
                    'view/picking_group_view.xml',
                    'view/stock_view.xml'],
    'active': False,
    'installable': True
}
