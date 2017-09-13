# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class CampaignConfig(models.Model):
    _name = 'fb.campaign.config'
    _order = 'date_release desc, name'

    name = fields.Char('Nom de la campagne', required=True)

    page = fields.Many2one('fb.page', 'Page facebook', select=True)

    leadgen_form = fields.Many2one(comodel_name='fb.leadgen', string='Formulaire facebook')

    leadgen_form_id = fields.Char('leadgen form id', store=True)  # todo onchange + required=True)

    date_release = fields.Date('Release Date')
    # state : definir : todo demarer les pull lorsque actif
    state = fields.Selection([('configpage', 'ConfigurationPage'),
                              ('configform', 'ConfigurationFormulaire'),
                              ('configdone', 'Ready'),
                              ],
                             'State')

    # pour test
    lead_firstname = fields.Char(readonly=True, copy=False, string='Prenom')
    lead_lastname = fields.Char(readonly=True, copy=False, string='Nom')
    lead_email = fields.Char(readonly=True, copy=False, string='Courriel')
    test_result = fields.Char(readonly=True, copy=False, string='Result')

    @api.multi
    @api.onchange("leadgen_form")
    def _set_leadgen_form_id(self):
        for r in self:
            r.leadgen_form_id = r.leadgen_form.page_id

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
        page_id = self.leadgen_form.page_id
        leads = self.env.user.get_leads(page_id)
        if not leads:
            return

        firstleads = leads.next()
        leadid = firstleads['id']
        leadcreatedtime = firstleads['created_time']
        lead_field_data = firstleads['field_data']
        lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

        self.write({'test_result': str(firstleads), 'lead_firstname': lead_entry_dict['first_name'],
                    'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})


    @api.one
    def clear_lead(self):
        self.ensure_one()
        self.write({'test_result': '', 'lead_firstname': '', 'lead_lastname': '', 'lead_email': ''})


    @api.multi
    def get_leads(self):
        self.ensure_one()
        page_id = self.leadgen_form.page_id
        leads = self.env.user.get_leads(page_id)
        if not leads:
            return

        for lead in leads:
            lead_id = lead['id']
            leadcreatedtime = lead['created_time']
            lead_field_data = lead['field_data']

            self.env['fb.lead'].create(
                {'lead_id': lead_id,
                 'campaign_id':self.id,
                 'data': str(lead),
                 'created_time':leadcreatedtime})

            lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

            lead_base_id = self.env['fb.lead.base'].create(lead_entry_dict, self.id)

            self.env['fb.lead.ref'].create(
                {'lead_id': lead_id, 'campaign_id': self.id, 'lead_base_id': lead_base_id.id})
