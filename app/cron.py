

from app import config

from datetime import datetime, timedelta
from webapp2 import WSGIApplication, Route, uri_for

from app.base_view import RequestHandler, PageRequestHandler
from app.decorators import cached_property
from app.ical_sync import CalendarSync
from app.event_model import Event


class Daily(PageRequestHandler):
    """
    Cron Job

    * Deletes old revisions of pages
    """

    def wiki_pages(self):
        return [item.get_url() for item in config.menu_items]

    def expire_old_pages(self):
        keep_history = 10
        log = self.response.write
        for name in self.wiki_pages():
            log(name + '\n')
            pages = self.load_page_history(name, 100)
            log('History consists of {0} entries\n'.format(len(pages)))
            for page in pages[keep_history:]:
                log('deleting version from {0}\n'.format(page.date))
                page.key.delete()
            log('\n')


    def expire_deleted_events(self):
        max_unseen = timedelta(days=2)
        now = datetime.utcnow()
        query = Event.query(Event.start_date > now)
        events = query.fetch(1000)
        log = self.response.write
        log('=' * 80)
        log(u'Total: {} events\n'.format(len(events)))
        for ev in events:
            if ev.seen is None:
                log(u'{}: seen is None, deleting\n'.format(ev.speaker))
                ev.key.delete()
                continue
            age = now - ev.seen
            if age > max_unseen: 
                log(u'{}: age = {} > {}, deleting.\n'.format(ev.speaker, age, max_unseen))
                ev.key.delete()
                continue
            log(u'{}: is current, keeping.\n'.format(ev.speaker))

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.expire_old_pages()
        self.expire_deleted_events()
        



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

