# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadChild(models.Model):
    _name = 'fb.lead.child'
    _rec_name = 'question_id'

    question_id = fields.Many2one('fb.question', 'Question', ondelete='restrict', required=True)
    value = fields.Char('Answers')
    lead_ref_id = fields.Many2one('fb.lead.ref', 'Related Lead', ondelete='cascade', required=True)

    @api.model
    def create(self, vals):
        name = vals.pop('name')
        leadgen_form_id= self.env.context.get('leadgen_form_id')
        domain = [('key', '=', name)]
        domain += [('leadgen_form_id', '=', leadgen_form_id)]
        question_id = self.env['fb.question'].search(domain) # domain question in leadgen_form
        # todo : ensure one

        vals['question_id'] = question_id.id
        return super(FbLeadChild, self).create(vals)

    @api.multi
    def write(self, vals):
        return super(FbLeadChild, self).write(vals)

