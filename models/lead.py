# -*- coding: utf-8 -*-
from openerp import models, fields


class Lead(models.Model):
    _name = 'fgcm.lead'
    _inherit = 'fgcm.campaign.config'
    datajson = fields.Text()

