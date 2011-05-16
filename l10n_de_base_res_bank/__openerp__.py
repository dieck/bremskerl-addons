##############################################################################
#
#    OpenERP Module l10n_de_base_res_bank
#    Copyright (C) 2011 Marco Dieckhoff
#
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
#
#    The list of Bankleitzahlen in data/res.bank.csv was provided by the german Bundesbank.
#    Copyright: Deutsche Bundesbank, Frankfurt am Main, Deutschland
#    http://www.bundesbank.de/zahlungsverkehr/zahlungsverkehr_bankleitzahlen_download.php
#    Der offizielle Bankleitzahlen-Änderungsdienst erfolgt für Zahlungsdienstleister
#    durch einen gesicherten Download aus dem ExtraNet der Deutschen Bundesbank.
#    Ergänzend stellt die Deutsche Bundesbank die Bankleitzahlendatei unverbindlich
#    ins Internet ein. Bitte beachten Sie bei der Verwendung der Bankleitzahlendatei
#    die Hinweise im Disclaimer http://www.bundesbank.de/info/info_impressum.php
#
#    Stand der Liste / List last updated 19.01.2011; gültig ab 07.03.2011 bis 05.06.2011
#
##############################################################################
{
    "name": "Localization: German Banks",
    "version": "1.0",
    "depends": ["base" ],
    "author": "Marco Dieckhoff",
    "category": "Localisation",
    "description": """Adding German Bankleitzahl to views, and adding a list of Bankleitzahlen as prepared data
    """,
    "init_xml": [],
    'update_xml': ["data/res.bank.csv",
                   "view/bank_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}