# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Facebook Leads',
    'version': '1.0',
    'summary': 'Outil de gestions des campagnes Facebook',
    'category': 'Tools',
    'description':
        """
Facebook Leads
==============

Outil de gestions des campagnes Facebook et vente des leads.
        """,
    'website': '',
    'author': 'Michel Rheault, Osha',
    'license': 'AGPL-3',
    # 'depends' : ['sale_stock'],
    'data' : [
        'views/debug.xml',
        'views/fb_config.xml',
        'views/fb_leads.xml',
        'views/fb_page.xml',
        'views/res_users.xml',
        'wizard/fb_lead_merge.xml',
    ],
    # 'js': ['static/src/js/resource.js'],
    # 'qweb': ['static/src/xml/resource.xml'],
    'application': True,
}
