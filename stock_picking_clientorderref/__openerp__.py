# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
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
{
    "name": "Add Customer Reference from Sales Order to Stock Picking overview",
    "version": "1.05",
    "depends": ["stock","sale"],
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    "category": "Warehouse",
    "description": "Add Customer Reference from Sales Order to Stock Picking overview",
    "init_xml": [],
    'update_xml': ["view/stock_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}