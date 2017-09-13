# -*- coding: utf-8 -*-

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class LeadCategory(models.Model):

    _name = "fb.lead.category"
    _description = "Facebook Lead Category"

    name = fields.Char(string="Lead Tag", required=True)
    color = fields.Integer(string='Color Index')

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

    address1 = fields.Char()  # ex 123
    address2 = fields.Char()  # ex vendome
    address3 = fields.Char()  # app
    city = fields.Char()
    state = fields.Char()
    country = fields.Char()
    zip_code = fields.Char(change_default=True)
    phone_number = fields.Char('Phone')
    email = fields.Char()
    lead_child_ids = fields.One2many('fb.lead.child', 'parent_id',
                                'Specific fields')


    #category_ids = fields.Many2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    color = fields.Integer('Color Index', default=0)

    # look for lead, or create one if none is found
    # env['fb.lead'].find_or_create(email_address)

    _sql_constraints = [
        ('email_uniq', 'unique (email)', "email already exists !"),
    ]

    @api.multi
    def create(self, values, campaign_id, context=None):
        specific_fields = []
        for key, val in values.iteritems():
            field = self._fields.get(key)
            if not field:
                child = {'campaign_id': campaign_id,
                         'name': key,
                         'value': val}
                specific_fields.append((0,0,child))
                values.pop(field, None)

        values['lead_child_ids'] = specific_fields
        record = super(FbLeadBase, self).create(values)

        # for (key, val) in other_field:
        #     self.env['fb.lead.plus'].create({
        #         'lead_base_id': record.id,
        #         'campaign_id': campaign_id,
        #         'name': key,
        #         'value': val})

        return record
