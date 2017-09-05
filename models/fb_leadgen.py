# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadgen(models.Model):
    _name = 'fb.leadgen'
    name = fields.Char('Formulaire facebook', required=True)
    page_id = fields.Char('Page id du formulaire facebook', required=True)
    fb_page = fields.Many2one('fb.page', readonly=True)
    fb_page_name = fields.Char(related='fb_page.name', store = True, readonly=True, copy=False, string='Facebook Page')
    leadgen_form = fields.One2many('fgcm.campaign.config', 'leadgen_form', 'Formulaire de la Campagne', readonly=True)
    status = fields.Char(string="Status")

    _sql_constraints = [
        ('fb_id_uniq', 'unique(page_id)', 'The id of the facebook leadgen page must be unique !'),
    ]

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.name
            fbpage = record.fb_page_name
            if name and fbpage:
                name = "%s <%s>" % (name, fbpage)
            result.append((record.id, name))
        return result