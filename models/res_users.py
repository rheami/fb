from openerp import models, fields, api
from openerp.addons.base.res import res_users
import facebook

res_users.USER_PRIVATE_FIELDS.append('oauth_facebook_long_access_token')


class ResUsers(models.Model):
    _inherit = 'res.users'

    oauth_facebook_long_access_token = fields.Char('OAuth Facebook Long Term Access Token', copy=False)

    # todo : log erreur si page plus active ou si hors de la periode
    # todo : set long term token as short term : login facebook : in a config facebook page

    @api.multi
    def update_facebook_pages(self):

        if self.oauth_facebook_long_access_token:
            graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version='2.10')
            endpoint = 'me/accounts'
            result = graph.get_object(id=endpoint, fields='id,name')
            page_list = result['data']

            # remove all
            self.delete_facebook_pages()

            for page in page_list:
                fb_page_id = page['id']

                page['page_id'] = page.pop('id')

                endpoint = '{0}/leadgen_forms'.format(fb_page_id)
                result = graph.get_object(id=endpoint, fields='id, name')

                # if having form then create fb.page
                if result:
                    fb_page = self.env['fb.page'].create(page)

                    # then create fb.leadgen
                    leadgen_list = result['data']
                    for leadgen in leadgen_list:
                        leadgen['page_id'] = leadgen.pop('id')
                        leadgen['fb_page'] = fb_page.id
                        self.env['fb.leadgen'].create(leadgen)
        return

    @api.multi
    def delete_facebook_pages(self):
        self.env["fb.page"].search([]).unlink()
        recs = self.env["fb.campaign.config"].search([])
        for rec in recs:
            rec.leadgen_form = False

        self.env["fb.leadgen"].search([]).unlink()

    def get_leadgen_forms(self, page_id):
        if not page_id or not self.oauth_facebook_long_access_token:
            return []

        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version='2.10')

        endpoint = '{0}/leadgen_forms'.format(page_id)
        result = graph.get_object(id=endpoint, fields='id, name, status')
        data_list = result['data']
        return data_list

    def get_leads(self, leadgen_form_id):
        if not leadgen_form_id or not self.oauth_facebook_long_access_token:
            return []

        # using new library : ( work with facebook version 2.10)
        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version='2.10')

        # 1-Download by Date Range  : 1857791184537261/leads?since=2017-08-28
        # 2-using from_date and to_date in a POSIX or UNIX time format, expressing the number of seconds since epoch
        # 3-Download New Leads (since last download) : how to ?

        leads = graph.get_all_connections(id=leadgen_form_id, connection_name='leads')

        # using old library
        # graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version=2.7)
        # leads = graph.get_connections(id=leadgen_form_id, connection_name='leads')

        return leads
