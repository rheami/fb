# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class CampaignConfig(models.Model):
    _name = 'fgcm.campaign.config'
    _order = 'date_release desc, name'

    name = fields.Char('Nom de la campagne', required=True)

    page = fields.Many2one('fb.page', 'Page facebook', select=True)
    page_id = fields.Char('page id')

    leadgen_form = fields.Many2one(comodel_name='fb.leadgen', string='Formulaire facebook')

    leadgen_form_id = fields.Char('leadgen form id')  # todo onchange + required=True)

    # leadgen_form_ids = fields.One2many('fgcm.leadgen.config', 'campaign_id', string="Formulaire", readonly=False)

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
    @api.onchange("page")
    def _set_page_id(self):
        for r in self:
            r.page_id = r.page.page_id

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
    def get_leads(self):
        self.ensure_one()
        page_id = self.leadgen_form_id
        leads = self.env.user.get_leads(page_id)
        firstleads = leads.next()

        leadid = firstleads['id']
        print (leadid)
        leadcreatedtime = firstleads['created_time']
        print (leadcreatedtime)
        lead_field_data = firstleads['field_data']
        lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

        self.write({'test_result': str(firstleads), 'lead_firstname': lead_entry_dict['first_name'],
                    'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})


    @api.one
    def clear_record_data(self):
        self.ensure_one()
        self.write({'test_result': '', 'lead_firstname': '', 'lead_lastname': '', 'lead_email': ''})


# todo : plus besoin de ce model
class LeadGeneratorConfig(models.Model):
    _name = 'fgcm.leadgen.config'
    name = fields.Char('Nom du formulaire', required=True)  # todo readonly=True car set a la creation
    leadgen_form_id = fields.Char('leadgen form id', copy=False)  # todo readonly=True car set a la creation

    campaign_id = fields.Many2one('fgcm.campaign.config', readonly=True, required=True)  # ne pas permettre de changer

    # camp_page = fields.Selection(related='campaign_id.page', readonly=True, store=True, string='Facebook Page')
    camp_page_id = fields.Char(related='campaign_id.page_id', readonly=True, copy=False, string='Facebook Page id')

    lead_firstname = fields.Char(readonly=True, copy=False, string='Prenom')
    lead_lastname = fields.Char(readonly=True, copy=False, string='Nom')
    lead_email = fields.Char(readonly=True, copy=False, string='Courriel')
    test_result = fields.Char(readonly=True, copy=False, string='Result')

    @api.one
    def get_leads(self):
        self.ensure_one()
        page_id = self.leadgen_form_id
        leads = self.env.user.get_leads(page_id)
        firstleads = leads.next()

        leadid = firstleads['id']
        print (leadid)
        leadcreatedtime = firstleads['created_time']
        print (leadcreatedtime)
        lead_field_data = firstleads['field_data']
        lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}

        self.write({'test_result': str(firstleads), 'lead_firstname': lead_entry_dict['first_name'],
                    'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})

    #        inv_line = self.env['fb.lead'].create(entry)

    @api.one
    def clear_record_data(self):
        self.ensure_one()
        self.write({'test_result': '', 'lead_firstname': '', 'lead_lastname': '', 'lead_email': ''})
