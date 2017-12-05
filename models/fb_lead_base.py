# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging
import re

_logger = logging.getLogger(__name__)


class LeadCategory(models.Model):

    _name = "fb.lead.category"
    _description = "Facebook Lead Category"

    name = fields.Char(string="Lead Tag", required=True)
    color = fields.Integer(string='Color Index')

    #  fb_lead_ref_ids = fields.Many2many('fb.lead.ref', 'fb_lead_category_rel', 'category_id', 'lead_id', string='Leads')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

def equal_dicts(a, b, ignore_keys):
    ka = set(a).difference(ignore_keys)
    return all(a[k] == b[k] for k in ka)

class FbLeadBase(models.Model):

    _name = "fb.lead.base"
    _order = 'last_name'
    name = fields.Char(compute='_compute_name')

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
    #created_time = fields.Date('LastModifiedDate') # todo _get_LastModifiedDate prend la date la + recente selon la liste lead_ref.created_time

    # todo state = fields.One2many('fb.lead.category', '_category_rel', '_id', 'category_id', string='Tags')
    state = fields.Char('state')  # LeadCategory  : duplicate , validate or qualified
    lead_ref_ids = fields.One2many(
        comodel_name='fb.lead.ref',
        inverse_name='lead_base_id',
        string='leads parents',
        readonly=True)
    lead_child_ids = fields.One2many(
        comodel_name='fb.lead.child', string=u"Lead Childs", compute='_compute_childs_ids')

    @api.depends('email', 'last_name', 'first_name')
    def _compute_name(self):
        for r in self:
            r.name = u'{} : {} {}, email: {}'.format(r.id, r.first_name, r.last_name, r.email)

    @api.multi
    @api.depends('lead_ref_ids')
    def _compute_childs_ids(self):
        for record in self:
            toto = self.lead_ref_ids.mapped('lead_child_ids')
            record.lead_child_ids = toto.ids

    @api.multi
    def create(self, values, ref_values_dict,  context=None):
        email = values.pop('email', None)

        # set pattern format to keep alphanumerics, dot, underscore, minus , trait long et court
        pattern = re.compile(ur'[^\.\_\w\s\u2014\u2013-]', re.U)

        base_fields = {k: re.sub(pattern, '', v) for k, v in values.items() if self._fields.get(k)}

        specific_fields = [(0, 0, {'name': k, 'value': values[k]}) for k, v in values.items()
                           if not self._fields.get(k)]

        # todo a tester rendu ici
        lead_dup_ids = self.env['fb.lead.base'].search([('email', '=', email)])
        merge = False
        if lead_dup_ids:
            state = 'duplicate'
            for record in lead_dup_ids:
                dup_fields={k: record._fields[k].convert_to_read(record[k], True) for k in base_fields.keys()}
                if dup_fields == base_fields:
                    merge = True
                    if len(lead_dup_ids) == 1:
                        state = 'validate'
                    break # only one merge is plausible
            lead_dup_ids.write({'state': state})
        else:
            state = 'validate'

        base_fields['state'] = state
        base_fields['email'] = email

        ref_values_dict['lead_child_ids'] = specific_fields

        if merge:
            ref_values_dict['lead_base_id'] = record.id
        else:
            record = super(FbLeadBase, self).create(base_fields)
            ref_values_dict['lead_base_id'] = record.id

            self.env['fb.lead.ref'].create(ref_values_dict)

        return record
