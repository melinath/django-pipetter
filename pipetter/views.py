from django.http import HttpResponse, Http404
import django.utils.simplejson as json
from pipetter.utils import refresh_cache as refresh, create_cache as create, get_cache_or_new
from pipetter import registry, NotRegistered


def refresh_cache(request, pipette_names):
	"""Perform a hard refresh of the cache for any of the named pipettes."""
	refresh(pipette_names.strip('/').split('/'))
	return HttpResponse('')


def create_cache(request, pipette_name, argstr):
	try:
		create(pipette_name, tuple(argstr.strip('/').split('/')))
	except NotRegistered:
		raise Http404('The specified pipette "%s" does not exist or is not registered.' % pipette_name)

	return HttpResponse('')
	
def json_response(request, pipette_name, argstr=None):
	"""Return the results of a pipette as a JSON response.
	Expects arguments as a '/' separated string."""
	
	if argstr:
		args = tuple(argstr.strip('/').split('/'))
	else:
		args = ()
	
	try:
		response_data = get_cache_or_new(pipette_name, args)
	except NotRegistered:
		raise Http404('The specified pipette "%s" does not exist or is not registered.' % pipette_name)
	
	response = json.dumps(response_data)	
	return HttpResponse(response, mimetype='application/json')