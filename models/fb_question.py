# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbQuestion(models.Model):
    _name = 'fb.question'
    _description = 'Facebook Question'
    _rec_name = 'label'

    campaign_id = fields.Many2one(related='leadgen_form_id.campaign_id', string='Survey Campaign')
    leadgen_form_id = fields.Many2one(comodel_name='fb.leadgen_form', string='Leadgen Form', required=True)
    key = fields.Char(required=1)
    label = fields.Char(required=1, translate=True)
    description = fields.Html('Description', help="Use this field to add \
            additional explanations about your question", translate=True)
    type = fields.Char()
    # options =

    lead_child_ids = fields.One2many(
        comodel_name="fb.lead.child",
        inverse_name="question_id",
        string="Answers")

    @api.model
    def create(self, vals):
        vals['question_id'] = vals.pop('id')
        return super(FbQuestion, self).create(vals)

    @api.model
    def write(self, vals):
        return super(FbQuestion, self).write(vals)
