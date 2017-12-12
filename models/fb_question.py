# -*- coding: utf-8 -*-
from openerp import models, fields


class FbQuestion(models.Model):
    _name = 'fb.question'
    _description = 'Facebook Survey Question'
    _rec_name = 'question'

    question = fields.Char('Question Name', required=True, translate=True)
    lead_child_ids = fields.One2many(
        comodel_name="fb.lead.child",
        inverse_name="question_id",
        string="Child")

    # user_input_line_ids = fields.One2many(
    #     'survey.user_input_line',
    #     'question_id',
    #     'Answers',
    #     domain=[('skipped', '=', False)])
