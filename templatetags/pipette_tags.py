from django import template
from pipettes import pipettes
from django.core.cache import cache
import datetime


register = template.Library()


def pipette_context(name, pipette):
	"""
	Wraps the pipette's get_context method to cache it and correctly set the
	function's name for tag creation.
	"""
	cache_key = 'pipette_%s' % name
	
	def do_pipette(*args):
		cached = cache.get(cache_key, None)
		
		if cached is None:
			cached = {}
		
		# Check if the pipette hasn't been called with these args before or if the cache time has expired.
		if (
			args not in cached or
			(datetime.datetime.now() - cached[args]['time']) > datetime.timedelta(0, 0, 0, 0, pipette.cache_for)
			):
			new_context = pipette.get_context(*args);
			if new_context or args not in cached:
				cached[args] = 	{
					'time': datetime.datetime.now(),
					'context': new_context
				}
				cache.set(cache_key, cached)
			else:
				# If a cached version exists and there's no current information, poke the cache time.
				cached[args]['time'] = datetime.datetime.now()
		
		return cached[args]['context']
	do_pipette.__name__ = name
	return do_pipette


for name, pipette in pipettes.items():
	register.inclusion_tag(
		pipette.template,
		takes_context=pipette.takes_context
	)(pipette_context(name, pipette))