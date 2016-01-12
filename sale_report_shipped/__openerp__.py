# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
