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
    _order = 'last_name'

    signup_date = fields.Date('Signup Date')
    last_name = fields.Char('Last Name')
    first_name = fields.Char('First Name')

    address_number = fields.Char()
    address_street = fields.Char('Street')
    address_app_number = fields.Char()

    city = fields.Char('City')
    state = fields.Char('State')
    country = fields.Char('Country')
    zip_code = fields.Char('Zip Code')
    phone_number = fields.Char('Phone')
    email = fields.Char('Email')
    lead_child_ids = fields.One2many('fb.lead.child', 'parent_id',
                                'Specific fields')

    # todo category_ids = fields.Many2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    color = fields.Integer('Color Index', default=0)

    # todo look for lead, or create one if none is found
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
                values.pop(field, None) # doesn't work !

        values['lead_child_ids'] = specific_fields
        record = super(FbLeadBase, self).create(values)

        return record
