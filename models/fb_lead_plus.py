# -*- coding: utf-8 -*-
from openerp import models, fields


class FbLeadPlus(models.Model):
    _name = 'fb.lead.plus'

    lead_id = fields.Char()
    campaign_id = fields.Char()
    lead_base_id = fields.Char()
    name = fields.Char()
    value = fields.Char()

