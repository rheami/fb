# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadgenForm(models.Model):
    _name = 'fb.leadgen_form'
    name = fields.Char('Facebook leadgen form', required=True)
    leadgen_form_id = fields.Char('Facebook leadgen form id ', required=True)
    fb_page = fields.Many2one('fb.page', readonly=True)
    fb_page_name = fields.Char(related='fb_page.name', store = True, readonly=True, copy=False, string='Facebook Page')
    leadgen_form = fields.One2many('fb.campaign.config', 'leadgen_form', 'Form associate to the campaign', readonly=True)
    status = fields.Char(string="Status")
    leads_count = fields.Char(string="Leads Counts", help='Actual Leads in the facebook leadsgen form')
    lastLeadCreated = fields.Integer(default=0, help='Created Time of last downloaded lead (epoch format)')

    _sql_constraints = [
        ('leadgen_form_id_uniq', 'unique(leadgen_form_id)', 'The id of the facebook leadgen form must be unique !'),
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