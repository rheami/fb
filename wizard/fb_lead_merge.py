from openerp import models, fields, api, _
from openerp import exceptions
import logging
_logger = logging.getLogger(__name__)


class FbLeadMerge(models.TransientModel):
    _name = "fb.lead.merge"

    lead = fields.Many2one(comodel_name='fb.lead.base', string='select lead',
                           domain="[('state', 'ilike', 'dup')]")
    email = fields.Char(related="lead.email")
    lead_dup_ids1 = fields.Many2many(comodel_name='fb.lead.base', string='lead chosen for merge',
                                     default=lambda self: self.env['fb.lead.base'].search([('id', '=', self.lead.id)]))
    lead_dup_ids2 = fields.Many2many(comodel_name='fb.lead.base', string='dup leads',
    default = lambda self: self.env['fb.lead.base'].search([('email', '=', self.email), ('id', '!=', self.lead.id)]))

    @api.multi
    @api.onchange('lead')
    def on_change_lead(self):
        self.lead_dup_ids1 = {}
        self.lead_dup_ids1 += self.lead
        self.lead_dup_ids2 = self.env['fb.lead.base'].search([('email', '=', self.email), ('id', '!=', self.lead.id)])


    @api.multi
    def create_request(self):
        return True

    # todo afficher count of dup : si 10 total qui se regroupe en trois : afficher 7 doublons

    @api.multi
    def do_merge(self):
        self.ensure_one()

        _logger.debug('merging leads')
        # pour joindre deux(ou +) lead_base:
        # 1 copier touts les lead_ref_ids dans le lead_base que l'on garde:
        for dup in self.lead_dup_ids2:
            self.lead.lead_ref_ids |= dup.lead_ref_ids  # append to lead_ref_ids

        # 2 effacer le(s) leadbase
        self.lead_dup_ids2.unlink()

        # 3 set state to validate if no other dupplicate of this lead
        self.lead.state = 'validate'

        # 4 check if more dupplicate
        res = self.env['fb.lead.base'].search([('state', 'ilike', 'dup')])

        if not res:
            return True # no more exit

        # else stay on the wizard

        self.lead = res[0]
        #self.on_change_lead()  # force change
        self.lead_dup_ids1 = {}
        self.lead_dup_ids1 += self.lead
        self.lead_dup_ids2 = self.env['fb.lead.base'].search([('email', '=', self.email), ('id', '!=', self.lead.id)])

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'fb.lead.merge',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'context': self._context,
            'target': 'new',
        }