from openerp.addons.base.res import res_users
from openerp import models, fields, api, exceptions, _
import facebook
from fb_config import FACEBOOK_VERSION
import logging

_logger = logging.getLogger(__name__)
# todo should be accessible to user in group facebook admin
res_users.USER_PRIVATE_FIELDS.append('oauth_facebook_long_access_token')
res_users.USER_PRIVATE_FIELDS.append('oauth_facebook_short_access_token')
res_users.USER_PRIVATE_FIELDS.append('facebook_username')
res_users.USER_PRIVATE_FIELDS.append('facebook_app_id')
res_users.USER_PRIVATE_FIELDS.append('facebook_app_secret')

class ResUsers(models.Model):
    _inherit = 'res.users'

    oauth_facebook_long_access_token = fields.Char('OAuth Facebook Long Term Access Token', copy=False)
    oauth_facebook_short_access_token = fields.Char('OAuth Facebook Short Term Access Token', copy=False)
    facebook_username = fields.Char('Facebook user name', copy=False)
    facebook_app_id = fields.Char('App id', copy=False)
    facebook_app_secret = fields.Char('App secret', copy=False)

    @api.multi
    def get_facebook_long_access_token(self):

        if self.oauth_facebook_short_access_token:
            graph = facebook.GraphAPI(access_token=self.oauth_facebook_short_access_token, version=FACEBOOK_VERSION)

            try:
                res = graph.extend_access_token(self.facebook_app_id, self.facebook_app_secret)
                tok = res['access_token']
                self.oauth_facebook_long_access_token = tok
            except facebook.GraphAPIError as e:
                raise Warning(e)

        return

    @api.multi
    def update_facebook_pages(self):

        # GET https://graph.facebook.com/v2.9/me/accounts?fields=leadgen_forms{name,status,leads_count,question_page_custom_headline,questions,qualifiers},name

        if self.oauth_facebook_long_access_token:
            graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version=FACEBOOK_VERSION)
            endpoint = 'me/accounts'
            # result = graph.get_object(id=endpoint, fields='leadgen_forms{name,status,leads_count,questions},name')
            result = graph.get_object(id=endpoint, fields='leadgen_forms{name,status,leads_count},name')
            page_list = result['data']

            for page in page_list:
                fb_page_id = page['id']
                page['page_id'] = page.pop('id')
                fb_page = self.env['fb.page'].search([('page_id', '=', fb_page_id)])
                fb_page.write(page) if fb_page else self.env['fb.page'].create(page)

                # then create fb.leadgen_form
                leadgen_forms = page['leadgen_forms']['data'] # todo prendre en compte le paging (si plus de 25 leadgen_form)
                for leadgen_form in leadgen_forms:
                    leadgen_form_id = leadgen_form['id']
                    leadgen_form['leadgen_form_id'] = leadgen_form.pop('id')
                    leadgen_form['fb_page'] = fb_page.id
                    fb_form = self.env['fb.leadgen_form'].search([('leadgen_form_id', '=', leadgen_form_id)])
                    fb_form.write(leadgen_form) if fb_form else self.env['fb.leadgen_form'].create(leadgen_form)
        return

    @api.multi
    def delete_facebook_pages(self):
        self.env["fb.page"].search([]).unlink()
        recs = self.env["fb.campaign"].search([])
        for rec in recs:
            rec.leadgen_form = False

        self.env["fb.leadgen_form"].search([]).unlink()

    def get_leadgen_forms(self, page_id):
        if not page_id or not self.oauth_facebook_long_access_token:
            error_msg='Oauth facebook setting are not set or no page access'
            _logger.error(error_msg)
            raise exceptions.ValidationError(_(error_msg))

        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version=FACEBOOK_VERSION)

        endpoint = '{0}/leadgen_forms'.format(page_id)
        result = graph.get_object(id=endpoint, fields='id, name, status')
        data_list = result['data']
        return data_list

    def get_leads(self, leadgen_form_id, last_get=0):
        if not leadgen_form_id or not self.oauth_facebook_long_access_token:
            error_msg='Oauth facebook setting are not set or no leadgen form access'
            _logger.error(error_msg)
            raise exceptions.ValidationError(_(error_msg))

        # using facebook_sdk version 3 : ( work with facebook version 2.9 et +)
        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version=FACEBOOK_VERSION)

        filtering = 'filtering=[{{"field": "time_created", "operator": "GREATER_THAN", "value":{0}}}]'.format(last_get)
        connection_name = '{0}/?{1}'.format('leads', filtering)
        leads = graph.get_all_connections(id=leadgen_form_id, connection_name=connection_name)
        return leads
