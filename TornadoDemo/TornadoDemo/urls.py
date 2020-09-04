from tornado.web import url
from tornado.web import StaticFileHandler
from apps.user import urls as user_urls
from TornadoDemo import settings


class MyFileHandler(StaticFileHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.redirect('http://example.com')  # Fetching a default resource


urlpatterns = [
    (url("/media/(.*)", StaticFileHandler, {'path': settings.MEDIA_URL})),
]
urlpatterns += user_urls.urlpatterns
