from django import template
from ..registry import pipettes
from django.core.cache import cache
import datetime


register = template.Library()


def pipette_context(name, pipette):
	"""
	Wraps the pipette's get_context method to cache it and correctly set the
	function's name for tag creation.
	"""
	# FIXME: find a way to set the vars do_pipette takes to the vars pipette.get_context takes
	cache_key = 'pipette_%s' % name
	
	def do_pipette(*args):
		cached = cache.get(cache_key, None)
		
		if cached is None:
			cached = {}
		
		if (
			args not in cached or
			(datetime.datetime.now() - cached[args]['time']) > datetime.timedelta(0, 0, 0, 0, pipette.cache_for)
			):
			cached[args] = {
				'time': datetime.datetime.now(),
				'context': pipette.get_context(*args)
			}
			cache.set(cache_key, cached)
		
		return cached[args]['context']
	do_pipette.__name__ = name
	return do_pipette


for name, pipette in pipettes.items():
	register.inclusion_tag(
		pipette.template,
		takes_context=pipette.takes_context
	)(pipette_context(name, pipette))