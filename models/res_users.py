from openerp import models, fields

from openerp.addons.base.res import res_users
res_users.USER_PRIVATE_FIELDS.append('oauth_facebook_long_access_token')
import facebook

class res_users(models.Model):
    _inherit = 'res.users'

    oauth_facebook_long_access_token = fields.Char('OAuth Long Access Token', copy=False)

    def get_fb_pages(self):
        data_list = []
        if self.oauth_facebook_long_access_token:
            graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version=2.7)
            endpoint = 'me/accounts'
            result = graph.get_object(id=endpoint, fields='id,name')
            data_list = result['data']
        # data_dict = {d['name']: d['id'] for d in data_list}
        # data_sel = [(i['id'],i['name']) for i in data_list]
        return data_list

    def get_leadgen_forms(self, page_id):
        if not page_id:
            return []

        access_token = self.oauth_facebook_long_access_token
        graph = facebook.GraphAPI(access_token=access_token, version='2.10')

        endpoint = '{0}/leadgen_forms'.format(page_id)
        result = graph.get_object(id=endpoint, fields='id, name')
        data_list = result['data']
        return data_list

    def get_leads(self, leadgen_form_id):
        if not leadgen_form_id:
            return []
        access_token = self.oauth_facebook_long_access_token
        graph = facebook.GraphAPI(access_token=access_token, version='2.10')

        # leads = graph.get_connections(id=leadgen_form_id, connection_name='leads')

        # avec gestion des pages (utiliser une version recente de la library)
        leads = graph.get_all_connections(id=leadgen_form_id, connection_name='leads')
        return leads
