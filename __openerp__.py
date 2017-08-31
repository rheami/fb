# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Prospect Leads',
    'version': '1.0',
    'summary': 'Outil de gestions des campagnes Facebook',
    'category': 'Tools',
    'description':
        """
Prospect Leads
==============

Outil de gestions des campagnes Facebook et vente des leads.
        """,
    'website': '',
    'author': 'Michel Rheault, Osha',
    'license': 'AGPL-3',
    'depends' : ['sale_stock'],
    'data' : [
        'views/prospectleads.xml',
        'views/fb_page.xml',
        'views/res_users.xml'
    ],
    'application': True,
}