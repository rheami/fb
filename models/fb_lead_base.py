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


class FbLeadBase(models.Model):

    _name = "fb.lead.base"
    _order = 'last_name'
    name = fields.Char(compute='_compute_name')

    last_name = fields.Char('Last Name')
    first_name = fields.Char('First Name')

    street_address = fields.Char('Street')

    city = fields.Char('City')
    province = fields.Char('State')
    country = fields.Char('Country')
    post_code = fields.Char('Zip Code')
    phone_number = fields.Char('Phone')
    email = fields.Char('Email')

    state = fields.Selection([
        ('validate', 'Validate'),
        ('duplicate', 'Duplicate'),
        ('qualified', 'Qualified'),
        ('rejected', 'Rejected'),
    ], default='validate', string='Status', readonly=True, copy=False, help="Gives the status of the leads." , select=True)

    lead_ref_ids = fields.One2many(
        comodel_name='fb.lead.ref',
        inverse_name='lead_base_id',
        string='Lead_ref',
        readonly=True, required=True)

    lead_child_ids = fields.One2many(
        comodel_name='fb.lead.child', string=u"Lead Childs", compute='_compute_childs_ids')

    @api.one
    def validate_progressbar(self):
        self.write({
            'state': 'validate',
        })

    @api.one
    def duplicate_progressbar(self):
        self.write({
            'state': 'duplicate'
        })

    @api.one
    def qualified_progressbar(self):
        self.write({
            'state': 'qualified'
        })

    @api.one
    def rejected_progressbar(self):
        self.write({
            'state': 'rejected',
        })

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

    @api.model
    def create(self, vals):
        email = vals.pop('email', None)
        ref_values_dict = vals.pop('lead_ref_ids', None)

        # set pattern format to keep alphanumerics, dot, underscore, minus , trait long et court
        pattern = re.compile(ur'[^\.\_\w\s\u2014\u2013-]', re.U)

        base_fields = {k: re.sub(pattern, '', v) for k, v in vals.items() if self._fields.get(k)}

        specific_fields = [(0, 0, {'name': k, 'value': vals[k]}) for k, v in vals.items()
                           if not self._fields.get(k)]

        lead_dup_ids = self.env['fb.lead.base'].search([('email', '=', email)])
        merge = False
        if lead_dup_ids:
            state = 'duplicate'
            for record in lead_dup_ids:
                dup_fields = {k: record._fields[k].convert_to_read(record[k], True) for k in base_fields.keys()}
                if dup_fields == base_fields:
                    merge = True
                    break # only one merge is plausible
                if state == 'duplicate':
                        lead_dup_ids.write({'state': state})   # todo gestion des states : si reject do not change
        else:
            state = 'validate'

        if ref_values_dict:
            ref_values_dict['lead_child_ids'] = specific_fields
            base_fields['lead_ref_ids'] = [(0, 0, ref_values_dict)]
            if merge:
                ref_values_dict['lead_base_id'] = record.id
                self.env['fb.lead.ref'].create(ref_values_dict)
                # update state
                if len(lead_dup_ids) > 1:
                    record.write({'state': 'duplicate'})
            else:
                base_fields['state'] = state
                base_fields['email'] = email
                record = super(FbLeadBase, self).create(base_fields)
        else: # import from csv
            if not merge:
                base_fields['state'] = state
                base_fields['email'] = email
                record = super(FbLeadBase, self).create(base_fields)
            # else: #  rien a faire le external id sera associé a ce record

        return record

    @api.multi
    def write(self, vals):
        return super(FbLeadBase, self).write(vals)


