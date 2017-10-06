# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbPages(models.Model):
    _name = 'fb.page'
    name = fields.Char('Facebook Page', required=True)
    page_id = fields.Char('Facebook Page Id', required=True)
    leadgen_ids = fields.One2many('fb.leadgen', 'fb_page', string="Facebook Form", readonly=False)

    _sql_constraints = [
        ('fb_id_uniq', 'unique(page_id)', 'The id of the Facebook page must be unique !'),
    ]
