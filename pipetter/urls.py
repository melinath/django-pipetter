from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('pipetter.views',
	url(r'^refresh/(?P<pipette_names>(?:[\w-]+/)+)$', 'refresh_cache'),
	url(r'^create/(?P<pipette_name>[\w-]+)/(?P<argstr>(?:[^/]+/)*)$', 'create_cache'),
	url(r'^json/(?P<pipette_name>[\w-]+)/(?P<argstr>(?:[^/]+/)*)$', 'json_response')
)