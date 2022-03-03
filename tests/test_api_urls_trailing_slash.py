import pytest
from django.conf import settings
from django.urls import URLPattern, URLResolver


def _api_list_urls():
    """ function to return all admin urls from urlconf.urlpatterns
    """
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])

    def list_urls(lis, acc=None):
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        if isinstance(l, URLPattern):
            yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from list_urls(lis[1:], acc)

    urls = []
    for p in list_urls(urlconf.urlpatterns):
        url = "".join(p)
        if url.startswith("apis") or url.startswith("admin-apis"):
            # urls to skip in admin
            if "jsi18n" in url:
                continue
            if "<" in url:
                continue
            urls.append(f"/{url}")
    return urls


@pytest.mark.parametrize("api_url", _api_list_urls())
@pytest.mark.django_db
def test_admin_pages_reach(client, super_user, api_url):
    assert not api_url.endswith("/")
    assert not api_url.endswith("/^$")
    assert not api_url.endswith("/$")
