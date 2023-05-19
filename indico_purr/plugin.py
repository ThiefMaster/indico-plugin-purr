from flask import session

from indico.core import signals
from indico.core.plugins import IndicoPlugin, url_for_plugin
from indico.modules.events.management.views import WPEventManagement
from indico.web.menu import SideMenuItem

from indico_purr import _
from indico_purr.blueprint import blueprint


class PurrPlugin(IndicoPlugin):
    """ PURR """

    configurable = False
    default_event_settings = {
        'connected': False,
        'api_url': '',
        'api_key': '',
        'pdf_page_width': 595.0,
        'pdf_page_height': 792.0,
        'custom_fields': [],
        'ab_session_h1': '{code} - {title}',
        'ab_session_h2': '{start} / {end}',
        'ab_contribution_h1': '| {code} | / | {start} |',
        'ab_contribution_h2': '| {code} | / | {start} |',
        'isbn': '',
        'issn': '',
        'booktitle_short': '',
        'booktitle_long': '',
        'series': '',
        'series_number': '',
        'location': '',
        'host_info': '',
        'editorial_board': '',
        'doi_base_url': 'doi:10.18429',
        'organization_segment': 'JACoW',
        'conference_segment': '',
        'doi_user': '',
        'doi_password': '',
        'date': '',
        
        'primary_color': '#F39433',
        'site_base_url': '//accelconf.web.cern.ch'
    }

    def init(self):
        super(PurrPlugin, self).init()
        self.register_assets()
        self.connect(signals.menu.items, self.purr_sidemenu_items, sender='event-management-sidemenu')

    def purr_sidemenu_items(self, sender, event, **kwargs):
        if event.can_manage(session.user):
            yield SideMenuItem('purr', _('PURR'), url_for_plugin('purr.purr_home', event),
                               0, section='workflows', icon='pdf')

    def get_blueprints(self):
        return blueprint

    def register_assets(self):
        self.inject_bundle('script.js', WPEventManagement)
        self.inject_bundle('style.css', WPEventManagement)

