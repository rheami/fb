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

Dépendances : facebook-sdk version 3 : 
pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk

        """,
    'website': '',
    'author': 'Michel Rheault, Osha',
    'license': 'AGPL-3',
    'depends' : ['auth_oauth'],
    #'external_dependencies': {'python': ['facebook']},
    'data' : [
        'views/fb_views.xml',
        'views/res_users.xml',
        'wizard/fb_lead_merge.xml',
    ],
    # 'js': ['static/src/js/resource.js'],
    # 'qweb': ['static/src/xml/resource.xml'],
    'application': True,
}
