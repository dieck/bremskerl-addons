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
    'name' : 'Picking Picker',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock'],
    'category' : 'Warehouse',
    'description': "This module allows you to pick stock moves from Warehouse - Product Moves - Receive/Deliver Products and combine them into a new picking (Incoming Shipment / Delivery Order).",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : [ 'view/stock_view.xml',
                    ],
    'active': False,
    'installable': True
}
