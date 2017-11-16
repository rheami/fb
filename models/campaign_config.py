# -*- coding: utf-8 -*-
import logging
from datetime import date, datetime
import time

from openerp import models, fields, api

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S' # facebook format
DATETIME_LENGTH = len(datetime.now().strftime(DATETIME_FORMAT))
_logger = logging.getLogger(__name__)


class CampaignConfig(models.Model):
    _name = 'fb.campaign.config'
    _order = 'date_release desc, name'

    name = fields.Char('Campaign Name', required=True)

    page = fields.Many2one('fb.page', 'Facebook Page', select=True)

    leadgen_form = fields.Many2one(comodel_name='fb.leadgen_form', string='Facebook Leadgen Form')
    #category = fields.Many2one(comodel_name='fb.campaign.category', string='Category', select=True)

    leadgen_form_id = fields.Char('leadgen form id', store=True)  # todo onchange + required=True)

    date_release = fields.Date('Release Date')
    # state : definir : todo demarer les pull lorsque actif
    # state = fields.Selection([('configpage', 'ConfigurationPage'),
    #                           ('configform', 'ConfigurationFormulaire'),
    #                           ('configdone', 'Ready'),
    #                           ],
    #                          'State')

    # pour test
    lead_firstname = fields.Char(readonly=True, copy=False, string='Firstname')
    lead_lastname = fields.Char(readonly=True, copy=False, string='Name')
    lead_email = fields.Char(readonly=True, copy=False, string='Email')
    test_result = fields.Char(readonly=True, copy=False, string='Result')

    @api.multi
    @api.onchange("leadgen_form")
    def _set_leadgen_form_id(self):
        for r in self:
            r.leadgen_form_id = r.leadgen_form.leadgen_form_id

    @api.one
    def update_facebook_pages(self):
        self.ensure_one()
        self.env.user.update_facebook_pages()

    @api.one
    def delete_facebook_pages(self):
        self.ensure_one()
        self.env.user.delete_facebook_pages()

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('configpage', 'configform'),
                   ('configform', 'configdone'),
                   ('configdone', 'configform'),
                   ('configdone', 'configpage'),
                   ('configform', 'configpage'),
                   ]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for rec in self:
            if rec.is_allowed_transition(rec.state,
                                         new_state):
                rec.state = new_state
            else:
                continue

    @api.one
    def get_one_lead(self):
        self.ensure_one()
        leadgen_form_id = self.leadgen_form.leadgen_form_id
        leads = self.env.user.get_leads(leadgen_form_id)

        try:
            first_leads = leads.next()
            leadid = first_leads['id']
            leadcreatedtime = first_leads['created_time']
            lead_field_data = first_leads['field_data']
            lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

            self.write({'test_result': str(first_leads), 'lead_firstname': lead_entry_dict['first_name'],
                        'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})
        except:
            self.write({'test_result': "No Leads found"})

    @api.one
    def clear_lead(self):
        self.ensure_one()
        self.write({'test_result': '', 'lead_firstname': '', 'lead_lastname': '', 'lead_email': ''})

    @api.multi
    def get_leads(self):
        self.ensure_one()
        leadgen_form_id = self.leadgen_form.leadgen_form_id
        lastLeadCreated = self.leadgen_form.lastLeadCreated
        leads = self.env.user.get_leads(leadgen_form_id, lastLeadCreated)

        for lead in leads:
            lead_id = lead['id']
            lead_created_time = lead['created_time'][:DATETIME_LENGTH]
            lead_created_epoch = int(time.mktime(time.strptime(lead_created_time, DATETIME_FORMAT)))
            if lead_created_epoch > lastLeadCreated:
                lastLeadCreated = lead_created_epoch
            lead_field_data = lead['field_data']

            fb_lead = self.env['fb.lead'].search([('lead_id', '=', lead_id)])
            if fb_lead :
                _logger.warning("Lead deja present")
                continue

            self.env['fb.lead'].create(
                {'lead_id': lead_id,
                 'campaign_id':self.id,
                 'data': str(lead),
                 'created_time':lead_created_time})

            lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}
            email = lead_entry_dict['email']
            lead_base = self.env['fb.lead.base'].search([('email', '=', email)])
            if lead_base :
                lead_base.write({'state': 'duplicate'})
                lead_entry_dict['state'] = 'duplicate'
            else:
                lead_entry_dict['state'] = 'validate'

            lead_base = self.env['fb.lead.base'].create(lead_entry_dict, self.id)

            self.env['fb.lead.ref'].create(
                {'lead_id': lead_id, 'campaign_id': self.id, 'lead_base_id': lead_base.id})

        # update lastLeadCreated
        if lastLeadCreated > self.leadgen_form.lastLeadCreated:
            self.leadgen_form.write({'lastLeadCreated': lastLeadCreated})
            _logger.warning("lastLeadCreated {}".format(lastLeadCreated))