# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FbLeadgenForm(models.Model):
    _name = 'fb.leadgen_form'
    name = fields.Char('Facebook leadgen form', required=True)
    leadgen_form_id = fields.Char('Facebook leadgen form id ', required=True)

    fb_page = fields.Many2one('fb.page', readonly=True)
    fb_page_name = fields.Char(related='fb_page.name', store = True, readonly=True, copy=False, string='Facebook Page')
    status = fields.Char(string='Status')
    leads_count = fields.Char(string='Leads Counts', help='Actual Leads in the facebook leadsgen form')
    lastLeadCreated = fields.Integer(default=0, help='Created Time of last downloaded lead (epoch format)')
    campaign_id = fields.Many2one('fb.campaign', readonly=True)
    lead_ref_ids = fields.One2many(
        comodel_name='fb.lead.ref',
        inverse_name='leadgen_form_id',
        string='leads associate to the facebook form',
        readonly=True)

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
                name = '%s <%s>' % (name, fbpage)
            result.append((record.id, name))
        return result