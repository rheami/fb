# -*- coding: utf-8 -*-

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class LeadCategory(models.Model):

    _name = "fb.lead.category"
    _description = "Facebook Lead Category"

    name = fields.Char(string="Lead Tag", required=True)
    color = fields.Integer(string='Color Index')

    #fb_lead_ref_ids = fields.Many2many('fb.lead.ref', 'fb_lead_category_rel', 'category_id', 'lead_id', string='Leads')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class FbLeadBase(models.Model):

    _name = "fb.lead.base"
    _order = 'last_name'

    signup_date = fields.Date('Signup Date')
    last_name = fields.Char('Last Name')
    first_name = fields.Char('First Name')

    street_address = fields.Char('Street')

    city = fields.Char('City')
    province = fields.Char('State')
    country = fields.Char('Country')
    post_code = fields.Char('Zip Code')
    phone_number = fields.Char('Phone')
    email = fields.Char('Email')

    # todo category_ids = fields.Many2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    state = fields.Char('state')  # LeadCategory  : duplicate , validate or qualified
    lead_ref_ids = fields.One2many(
        comodel_name='fb.lead.ref',
        inverse_name='lead_base_id',
        string='leads parents',
        readonly=True)

    @api.multi
    def create(self, values, ref_values_dict,  context=None):
        specific_fields = []
        keys = [k for k, v in values.items() if not self._fields.get(k)]
        for k in keys:
            child = {'name': k, 'value': values[k]}
            specific_fields.append((0, 0, child))
            del values[k]

        record = super(FbLeadBase, self).create(values)
        ref_values_dict['lead_child_ids'] = specific_fields
        ref_values_dict['lead_base_id'] = record.id
        self.env['fb.lead.ref'].create(ref_values_dict)
        return record