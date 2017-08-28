# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import facebook

class CampaignConfig(models.Model):
    _name = 'fgcm.campaign.config'
    _order = 'date_release desc, name'

    name = fields.Char('Nom de la campagne', required=True)
    leadgen_form_ids = fields.One2many('fgcm.leadgen.config', 'campaign_id', string="Formulaire", readonly=False)

    date_release = fields.Date('Release Date')
    # state : definir : todo demarer les pull lorsque actif
    state = fields.Selection([('configpage', 'ConfigurationPage'),
                              ('configform', 'ConfigurationFormulaire'),
                              ('configdone', 'Ready'),
                             ],
                             'State')

    page = fields.Selection(selection='_get_fb_pages', store=True)
    pages = fields.Char('pages', compute='_get_pages', required=True)
    page_id = fields.Char('page id', required=True)
    data_sel = fields.Char('pages', compute='_get_fb_pages', required=True)

    @api.multi
    def create(self):
        # Todo code
        print("toto")
        super(CampaignConfig, self).create()

    @api.multi
    def write(self):
        # Todo code
        print("totoa")
        super(CampaignConfig, self).write()

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

    def _get_fb_pages(self):
        data_list = self.env.user.get_fb_pages()
        data_sel = [(i['id'], i['name']) for i in data_list]
        print(data_sel) # todo verifier
        return data_sel

    # solution temporaire pour developement
    def _get_pages(self):
        for record in self:
            record.pages = str(self._get_fb_pages())

    def create_leadgen_form_record_data(self):
        # check state ?
        self.ensure_one()
        data_list = self.env.user.get_leadgen_forms(self.page_id)
        # todo create a LeadGeneratorConfig record for each  write name , leadgen_form_id

    # todo at save change state
    #
    #         # create the new invoice
    #         invoice_line_data = invoice_data['invoice_line']
    #         del invoice_data['invoice_line']
    #         newinvoice = self.with_context(is_merge=True).create(invoice_data)
    #         invoice_lines_info[newinvoice.id] = {}
    #         for entry in invoice_line_data.values():
    #             o_line_ids = entry['o_line_ids']
    #             del entry['o_line_ids']
    #             entry['invoice_id'] = newinvoice.id
    #             inv_line = self.env['account.invoice.line'].create(entry)



class LeadGeneratorConfig(models.Model):
    _name = 'fgcm.leadgen.config'
    name = fields.Char('Nom du formulaire', required=True) # todo readonly=True car set a la creation
    leadgen_form_id = fields.Char('leadgen form id', copy=False) # todo readonly=True car set a la creation

    campaign_id = fields.Many2one('fgcm.campaign.config', readonly=True, required=True) # ne pas permettre de changer

    camp_page = fields.Selection(related='campaign_id.page', readonly=True, store=True, string='Facebook Page')
    camp_page_id = fields.Char(related='campaign_id.page_id', readonly=True, copy=False, string='Facebook Page id')

    lead_firstname = fields.Char(readonly=True, copy=False, string='Prenom')
    lead_lastname = fields.Char(readonly=True, copy=False, string='Nom')
    lead_email = fields.Char(readonly=True, copy=False, string='Courriel')
    test_result = fields.Char(readonly=True, copy=False, string='Result')

    # @api.multi
    # def create(self, vals):
    #     # Todo code
    #     super(LeadGeneratorConfig, self).create(vals)
    #
    # @api.multi
    # def write(self, vals):
    #     # Todo code
    #     super(LeadGeneratorConfig, self).write(vals)

    # def _get_fb_pages(self):
    #     data_list = self.env.user.get_fb_pages()
    #     data_sel = [(i['id'], i['name']) for i in data_list]
    #     return data_sel

    @api.one
    def get_leads(self):
        self.ensure_one()
        page_id = self.leadgen_form_id
        leads = self.env.user.get_leads(page_id)
        data = leads['data']
        if data:
            #for lead in data:
            lead = data[0]
            leadid = lead['id']
            print (leadid)
            leadcreatedtime = lead['created_time']
            print (leadcreatedtime)
            lead_field_data = lead['field_data']
            lead_entry_dict = { fd['name']: fd['values'][0] for fd in lead_field_data }

        self.write({'test_result': str(leads), 'lead_firstname': lead_entry_dict['first_name'], 'lead_lastname': lead_entry_dict['last_name'], 'lead_email': lead_entry_dict['email']})
#        inv_line = self.env['fb.lead'].create(entry)

    @api.one
    def clear_record_data(self):
        self.ensure_one()
        self.write({'test_result': '', 'lead_firstname': '', 'lead_lastname': '', 'lead_email': ''})
