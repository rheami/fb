# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadData(models.Model):
    _name = 'fb.lead.data'
    data = fields.Char()
    created_time = fields.Char()
