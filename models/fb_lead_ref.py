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

    _sql_constraints = [
        ('lead_id_uniq', 'unique (lead_id)', "Lead id already exists !"),
    ]

    @api.multi
    def unlink(self):

        ref_ids = set(self.ids)
        data_ids = self.mapped('lead_data_id')
        base_ids = self.mapped('lead_base_id')
        base_to_del = []

        for b in base_ids:
            if b.lead_ref_ids:
                if set(b.lead_ref_ids.ids).issubset(ref_ids):
                    base_to_del.append(b.id)
            else:
                base_to_del.append(b.id)

        rec_base_ids = self.env['fb.lead.base'].browse(base_to_del)
        result = data_ids.unlink()
        if result:
            result = rec_base_ids.unlink()
        return result

    @api.model
    def create(self, vals):
        # self.env.context['leadgen_form_id'] = vals['leadgen_form_id']
        leadgen_form_id = vals['leadgen_form_id']
        self = self.with_context(leadgen_form_id=leadgen_form_id)
        return super(FbLeadRef, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(FbLeadRef, self).write(vals)


