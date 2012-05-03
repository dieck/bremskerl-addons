# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
# based on sale/report/sale_report from openobject-addons/6.0
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
##############################################################################

{
    'name' : 'Sales Report with Shipped Quantities',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['sale'],
    'category' : 'Sales',
    'description': """
This module adds reporting for Sales with summed shipped quantities.
    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['security/ir.model.access.csv', 'view/sale_report_view.xml'],
    'active': False,
    'installable': True
}
