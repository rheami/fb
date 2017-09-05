# -*- coding: utf-8 -*-
from openerp import models, fields


class FbLeadRef(models.Model):
    _name = 'fb.lead.ref'
    lead_id = fields.Char()
    campaign_id = fields.Char()
    lead_base_id = fields.Char()

