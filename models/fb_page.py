# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbPages(models.Model):
    _name = 'fb.page'
    name = fields.Char('Facebook Page', required=True)
    page_id = fields.Char('Facebook Page Id', required=True)

    leadgen_ids = fields.One2many(
        comodel_name="fb.leadgen_form",
        inverse_name="fb_page",
        string="Facebook Form",
        # required=True,
        readonly=False,
        help="Leadgen_Forms of the Facebook Page")

    def create(self, vals):
        return super(FbPages, self).create(vals)

    def write(self, vals):
        return super(FbPages, self).write(vals)

    _sql_constraints = [
        ('fb_id_uniq', 'unique(page_id)', 'The id of the Facebook page must be unique !'),
    ]
