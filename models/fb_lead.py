# -*- coding: utf-8 -*-
from openerp import models, fields


class FbLead(models.Model):
    _name = 'fb.lead'
    lead_id = fields.Char()
    campaign_id = fields.Char()
    data = fields.Char()
    created_time = fields.Char()

    _sql_constraints = [
        ('lead_id_uniq', 'unique (lead_id)', "Lead id already exists !"),
    ]