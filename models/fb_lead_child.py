# -*- coding: utf-8 -*-
from openerp import models, fields


class FbLeadChild(models.Model):
    _name = 'fb.lead.child'

    name = fields.Char()
    value = fields.Char()
    lead_ref_id = fields.Many2one('fb.lead.ref', 'Related Lead', ondelete='cascade', required=True)
