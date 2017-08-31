# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbPages(models.Model):
    _name = 'fb.page'
    name = fields.Char('Page facebook', required=True)
    page_id = fields.Char('Page id facebook', required=True)
    camp = fields.One2many('fgcm.campaign.config', 'page', 'Campagne', readonly=True)
    leadgen_ids = fields.One2many('fb.leadgen', 'fb_page', string="Formulaire facebook", readonly=False)

    _sql_constraints = [
        ('fb_id_uniq', 'unique(page_id)', 'The id of the facebook page must be unique !'),
    ]
