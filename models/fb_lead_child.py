# -*- coding: utf-8 -*-
from openerp import models, fields


class FbLeadChild(models.Model):
    _name = 'fb.lead.child'

    campaign_id = fields.Char()
    name = fields.Char()
    value = fields.Char()
    parent_id = fields.Many2one('fb.lead.base', 'Related Lead')
    lead_id = fields.Char(related='parent_id.email')
