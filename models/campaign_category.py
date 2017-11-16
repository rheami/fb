# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class CampaignConfig(models.Model):
    _name = 'fb.campaign.category'

    name = fields.Char('Category Name', required=True)

    # leadgen_form = fields.One2many('fb.campaign.config', 'leadgen_form', 'Form associate to the campaign', readonly=True)
