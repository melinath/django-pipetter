from django.http import HttpResponse
from pipettes.utils import refresh_cache as refresh, create_cache as create


def refresh_cache(request, pipette_names):
	"""Perform a hard refresh of the cache for any of the named pipettes."""
	refresh(pipette_names.strip('/').split('/'))
	return HttpResponse('')


def create_cache(request, pipette_name, argstr):
	create(pipette_name, tuple(argstr.strip('/').split('/')))
	return HttpResponse('')