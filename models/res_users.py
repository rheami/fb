from openerp import models, fields, api
from openerp.addons.base.res import res_users
import facebook

res_users.USER_PRIVATE_FIELDS.append('oauth_facebook_long_access_token')


class ResUsers(models.Model):
    _inherit = 'res.users'

    oauth_facebook_long_access_token = fields.Char('OAuth Long Access Token', copy=False)

    # todo : aller chercher page et les formlead de ces pages et les enregistrers (ajouter bouton mise a jour)
    # todo : utiliser pour initialiser les selections
    # todo : verifier ajouter seulement les form active
    # todo : log erreur si page plus active

    @api.multi
    def update_facebook_pages(self):
    #def get_fb_pages(self):
        data_list = []

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
                if result :
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
        recs = self.env["fgcm.campaign.config"].search([])
        for rec in recs:
            rec.leadgen_form = False

        self.env["fb.leadgen"].search([]).unlink()

    def get_leadgen_forms(self, page_id):
        if not page_id or not self.oauth_facebook_long_access_token:
            return []

        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version='2.10')

        endpoint = '{0}/leadgen_forms'.format(page_id)
        result = graph.get_object(id=endpoint, fields='id, name')
        data_list = result['data']
        return data_list

    def get_leads(self, leadgen_form_id):
        if not leadgen_form_id or not self.oauth_facebook_long_access_token:
            return []

        graph = facebook.GraphAPI(access_token=self.oauth_facebook_long_access_token, version='2.10')

        # leads = graph.get_connections(id=leadgen_form_id, connection_name='leads')

        # avec gestion des pages (utiliser une version recente de la library)
        leads = graph.get_all_connections(id=leadgen_form_id, connection_name='leads')
        return leads



