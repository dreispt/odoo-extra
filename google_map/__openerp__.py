# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Google Maps',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'description': """This module adds a Map button on the partner’s form in order to open its address directly in the Google Maps view""",
    'author': 'BHC & OpenERP',
    'website': 'www.bhc.be',
    'depends': ['base'],
    'init_xml': [],
    'images': ['images/google_map.png','images/map.png','images/earth.png'],
    'update_xml': [
                   'google_map_view.xml',
                  ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
