from app import config

from webapp2 import WSGIApplication, Route, uri_for
from app.base_view import RequestHandler, PageRequestHandler
from app.decorators import cached_property
from app.ical_sync import CalendarSync


class Daily(PageRequestHandler):
    """
    Cron Job

    * Deletes old revisions of pages
    """

    def wiki_pages(self):
        return [item.get_url() for item in config.menu_items]

    def get(self):
        keep_history = 10
        self.response.headers['Content-Type'] = 'text/plain'
        log = self.response.write
        for name in self.wiki_pages():
            log(name + '\n')
            pages = self.load_page_history(name, 100)
            log('History consists of {0} entries\n'.format(len(pages)))
            for page in pages[keep_history:]:
                self.response.write('deleting version from {0}\n'.format(page.date))
                page.key.delete()
            log('\n')





class IcalSyncer(RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        cal = CalendarSync()
        for remote in config.remote_calendars:
            cal.import_url(remote.series, remote.url, remote.activate)
        self.response.write(str(cal.events))










application = WSGIApplication([
    Route(r'/cron/daily', Daily, name='cron-daily'),
    Route(r'/cron/calendar', IcalSyncer, name='cron-calendar'),
], debug=True)

