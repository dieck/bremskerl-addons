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
    "name": "Boilerplates",
    "version": "1.0",
    "depends": ["base", "base_tools", "product" ],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Custom",
    "description": """
This addon, together with it's modular extensions, provides boilerplates for multiple fields.

Boilerplates can be organized in Categories and set to belong to a specific product or partner.
You can setup texts in Tools / Boilerplates.

Modular extensions provide actions on different forms to add these boilerplates directly to existing text fields, thus being used natively, e.g. in reports. 
    """,
    "init_xml": [],
    'update_xml': ["security/boilerplates_security.xml",
                   "security/ir.model.access.csv",
                   "data/boilerplates_data.xml", 
                   "view/boilerplates_view.xml",
                   "wizard/boilerplates_wiz_view.xml"],
    'demo_xml': ["data/boilerplates_demo.xml"],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}