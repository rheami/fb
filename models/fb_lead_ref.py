# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadRef(models.Model):
    _name = 'fb.lead.ref'

    _inherits = {'fb.lead.data': 'lead_data_id'}
    lead_id = fields.Char(required=True)
    campaign_id = fields.Many2one(comodel_name='fb.campaign', string='Campaign', required=True)
    leadgen_form_id = fields.Many2one(comodel_name='fb.leadgen_form', string='Leadgen Form', required=True)
    lead_data_id = fields.Many2one(comodel_name='fb.lead.data', string='Lead data', ondelete="cascade", required=True)
    lead_base_id = fields.Many2one(comodel_name='fb.lead.base', string='Lead base', required=True)
    lead_child_ids = fields.One2many(
        comodel_name="fb.lead.child",
        inverse_name="lead_ref_id",
        string="Specific fields",
        help="Fields related to a specific Facebook Leadgen Form")

    # pour joindre deux leadbases :
    #  1 changer le lead_base_id pour celui que l'on garde
    #  2 changer le parent_id des childs pour lead_base_id que l'on garde

    _sql_constraints = [
        ('lead_id_uniq', 'unique (lead_id)', "Lead id already exists !"),
    ]

    @api.multi
    def create(self, values,  context=None):
        lead_data = self.env['fb.lead.data'].create(values)
        values['lead_data_id']=lead_data.id
        record = super(FbLeadRef, self).create(values)
        return record