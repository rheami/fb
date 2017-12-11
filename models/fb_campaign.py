# -*- coding: utf-8 -*-
import logging
from datetime import date, datetime
import time

from openerp import models, fields, api, exceptions, _

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S' # facebook format
DATETIME_LENGTH = len(datetime.now().strftime(DATETIME_FORMAT))
_logger = logging.getLogger(__name__)


class FbCampaign(models.Model):
    _name = 'fb.campaign'
    _order = 'date_release desc, name'

    name = fields.Char('Campaign Name', required=True)
    leadgen_form = fields.Many2one(comodel_name='fb.leadgen_form', string='Facebook Leadgen Form')
    # todo add to leadgen_forms_id so we can other form to leadgen_form_ids

    #category = fields.Many2one(comodel_name='fb.campaign.category', string='Category', select=True)
    date_release = fields.Date('Release Date')

    lead_ref_ids = fields.One2many(
        comodel_name='fb.lead.ref',
        inverse_name='campaign_id',
        string='leads associate to the facebook campaign',
        readonly=True)

    # state : definir : todo demarer les pull lorsque actif
    # state = fields.Selection([('configpage', 'ConfigurationPage'),
    #                           ('configform', 'ConfigurationFormulaire'),
    #                           ('configdone', 'Ready'),
    #                           ],
    #                          'State')

    # pour test todo : placer dans un wizard
    lead_firstname = fields.Char(readonly=True, copy=False, string='Firstname')
    lead_lastname = fields.Char(readonly=True, copy=False, string='Name')
    lead_email = fields.Char(readonly=True, copy=False, string='Email')
    test_result = fields.Char(readonly=True, copy=False, string='Result')

    # @api.multi
    # @api.onchange("leadgen_form")
    # def _set_leadgen_form_id(self):
    #     for r in self:
    #         r.leadgen_form_id = r.leadgen_form.leadgen_form_id

    # todo : placer dans un wizard
    @api.one
    def update_facebook_pages(self):
        self.ensure_one()
        self.env.user.update_facebook_pages()

    # todo : placer dans un wizard
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

    # todo : placer dans un wizard
    @api.one
    def get_one_lead(self):
        self.ensure_one()
        leadgen_form_id = self.leadgen_form.leadgen_form_id

        try:
            leads = self.env.user.get_leads(leadgen_form_id)
            first_leads = leads.next()
            leadid = first_leads['id']
            leadcreatedtime = first_leads['created_time']
            lead_field_data = first_leads['field_data']
            lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

            self.write({'test_result': str(first_leads), 'lead_firstname': lead_entry_dict['first_name'],
                        'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})
        except exceptions.ValidationError, exceptions.ValidationError.message:
            error_msg = 'Oauth facebook setting are not set or no leadgen form access'
            self.write({'test_result': error_msg})
        except Exception, e:
            self.write({'test_result': "No Leads found"})

    # todo : placer dans un wizard
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

            fb_lead_ref = self.env['fb.lead.ref'].search([('lead_id', '=', lead_id)])
            if fb_lead_ref :
                _logger.warning("Lead already there")
                continue

            lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}
            ref_values_dict = {'lead_id': lead_id,
                               'campaign_id': self.id,
                               'leadgen_form_id': self.leadgen_form.id,
                               'data': str(lead),
                               'created_time': lead_created_time}
            lead_entry_dict['lead_ref_ids'] = ref_values_dict

            lead_base = self.env['fb.lead.base'].create(lead_entry_dict)

        # update lastLeadCreated
        if lastLeadCreated > self.leadgen_form.lastLeadCreated:
            self.leadgen_form.write({'lastLeadCreated': lastLeadCreated})
            _logger.warning("lastLeadCreated {}".format(lastLeadCreated))
