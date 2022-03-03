import mock
import pytest
from django.conf import settings
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import URLPattern, URLResolver


def _admin_list_urls():
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
        if url.startswith("admin/"):
            # urls to skip in admin
            if "jsi18n" in url:
                continue
            if "<" in url:
                continue
            urls.append(f"/{url}")
    return urls


def _admin_detail_urls():
    """ function to return details pages in admin if a factory is found for model
    the function will search for matching factory if factory found it will model factory
    and details URL
    """
    for model, _ in admin.site._registry.items():
        try:
            app_factories = __import__(
                f"tests.{model._meta.app_label}.factories",
                fromlist=[f"{model._meta.object_name}Factory",],
            )
            yield [
                getattr(app_factories, f"{model._meta.object_name}Factory"),
                f"admin:{model._meta.app_label}_{model._meta.model_name}_change",
            ]
        except ImportError:
            # Cannot locate factory under
            # tests/[app_label]/factories.py
            continue
        except AttributeError:
            # cannot allocate class factory
            # tests/[app_label]/factories.py::[object_name]Factory()
            continue


@pytest.mark.parametrize("admin_url", _admin_list_urls())
@pytest.mark.django_db
@mock.patch("requests.post")
def test_admin_pages_reach(client, super_user, admin_url):
    client.force_login(super_user)
    resp = client.get(admin_url, follow=True)
    if isinstance(resp, TemplateResponse):
        assert resp.status_code == 200
        assert "<!DOCTYPE html".encode() in resp.content
