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

    street_address = fields.Char('Street')

    city = fields.Char('City')
    province = fields.Char('State')
    country = fields.Char('Country')
    post_code = fields.Char('Zip Code')
    phone_number = fields.Char('Phone')
    email = fields.Char('Email')

    lead_child_ids = fields.One2many(
        comodel_name="fb.lead.child",
        inverse_name="parent_id",
        string="Specific fields",
        #required=True,
        help="Fields used in a specific campains")

    # todo category_ids = fields.Many2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    state = fields.Char('state')  # LeadCategory  : duplicate , validate or qualified # rendu ici
    # color = fields.Integer('Color Index', default=0)

    # _sql_constraints = [
    #     ('email_uniq', 'unique (email)', "email already exists !"),
    # ]
    #
    # @api.multi
    # def create(self, values, campaign_id, context=None):
    #     specific_fields = []
    #     for key, val in values.iteritems():
    #         field = self._fields.get(key)
    #         if not field:
    #             child = {'campaign_id': campaign_id,
    #                      'name': key,
    #                      'value': val}
    #             specific_fields.append((0,0,child))
    #
    #     values['lead_child_ids'] = specific_fields
    #     record = super(FbLeadBase, self).create(values)
    #
    #     return record

    @api.multi
    def create(self, values, campaign_id, context=None):
        specific_fields = []
        keys = [k for k, v in values.items() if not self._fields.get(k)]
        for k in keys:
            child = {'campaign_id': campaign_id, 'name': k, 'value': values[k]}
            specific_fields.append((0, 0, child))
            del values[k]

        values['lead_child_ids'] = specific_fields
        record = super(FbLeadBase, self).create(values)
        return record