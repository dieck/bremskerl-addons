# -*- coding: utf-8 -*-
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
{
    "name": "Add product WVA number",
    "version": "1.01",
    "depends": ["product"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Inventory Control",
    "description": """Add field for WVA number.
    WVA numbers are a reference and assignment system for brake linings, clutch facings, brake shoes and other friction materials which will especially be used in road vehicles but also in mechanical engineering. 
    """,
    "init_xml": [],
    'update_xml': ["view/product_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}