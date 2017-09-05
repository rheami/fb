# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class LeadCategory(models.Model):

    _name = "fb.lead.category"
    _description = "Facebook Lead Category"

    name = fields.Char(string="Lead Tag", required=True)
    color = fields.Integer(string='Color Index')

    # class odoo.fields.Many2many(comodel_name=<object object>, relation=<object object>, column1=<object object>, column2=<object object>, string=<object object>, **kwargs)
    fb_lead_ids = fields.Many2many('fb.lead', 'fb_lead_category_rel', 'category_id', 'lead_id', string='Leads')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class FbLeadBase(models.Model):

    _name = "fb.lead.base"
    _description = "Personne"
    _order = 'last_name'

    signup_date = fields.Date('Signup Date')
    last_name = fields.Char()
    first_name = fields.Char()

    address1 = fields.Char() # ex 123
    address2 = fields.Char()  # ex vendome
    address3 = fields.Char() # app
    city = fields.Char()
    state = fields.Char() # default = quebec
    # state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country = fields.Char() # default = canada
    # country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    zip_code = fields.Char(change_default=True)
    phone_number = fields.Char('Phone')
    email = fields.Char() # get facebook email : already validated

    #category_ids = fields.Many2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    color = fields.Integer('Color Index', default=0)

    # look for lead, or create one if none is found
    # env['fb.lead'].find_or_create(email_address)

    @api.multi
    def create(self, values, campaign_id, context=None):
        unknown = []
        for key, val in values.iteritems():
            field = self._fields.get(key)
            if not field:
                # self.env['fb.lead.plus'].create({'campaign_id': campaign_id, 'name':key, 'value':val})
                unknown.append(key)
                values.pop(field, None)

        if unknown:
            _logger.warning("%s.write() with unknown fields: %s", self._name, ', '.join(sorted(unknown)))



    # @api.multi
    # def get_leads(self):
    #     model = self.env['fgcm.leadgen.config']
    #     domain = [('name', '=', 'test_form-copy')] # todo get name from config
    #     leadgen_info = model.search(domain)
    #     if not leadgen_info:
    #         return
    #
    #     leadgen = leadgen_info[0]
    #
    #     page_id = leadgen.leadgen_form_id
    #     leadsgenerator = self.env.user.get_leads(page_id)
    #     for lead in leadsgenerator:
    #         leadid = lead['id']
    #         #print (leadid)
    #         leadcreatedtime = lead['created_time']
    #         #print (leadcreatedtime)
    #         lead_field_data = lead['field_data']
    #         # lead_field_data['created_time'] = lead['created_time']
    #         lead_entry_dict = {fd['name']: fd['values'][0] for fd in lead_field_data}
    #
    #     self.write(lead_entry_dict)
