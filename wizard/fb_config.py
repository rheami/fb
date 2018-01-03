# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp import exceptions
import logging

_logger = logging.getLogger(__name__)


class FacebookConfig(models.TransientModel):
    _name = 'fb.config'
    new_user_id = fields.Many2one('res.users', string='Responsable of facebook pages')
    leadgen_forms_ids=fields.Many2one('fb.leadgen_form', string='Leadgen Forms')

    @api.one
    def update_facebook_pages(self):
        self.ensure_one()
        self.env.user.update_facebook_pages()

    @api.one
    def delete_facebook_pages(self):
        self.ensure_one()
        self.env.user.delete_facebook_pages()
