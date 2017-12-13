# -*- coding: utf-8 -*-
from openerp import models, fields


class FbQuestion(models.Model):
    _name = 'fb.question'
    _description = 'Facebook Question'
    _rec_name = 'question'

    # Question metadata
    leadgen_form_id = fields.Many2one('fb.leadgen_form', 'Survey page (facebook leadgen form)',
            ondelete='restrict', required=True)
    campaign_id = fields.Many2one(related='leadgen_form_id.campaign_id', string='Survey Campaign')
    # Question
    question = fields.Char('Question Name', required=1, translate=True)
    description = fields.html('Description', help="Use this field to add \
            additional explanations about your question", translate=True)

    lead_child_ids = fields.One2many(
        comodel_name="fb.lead.child",
        inverse_name="question_id",
        string="Answers")

    _sql_constraints = [
        ('question_uniq', 'unique (question)', "Question already exists !"),
    ]
