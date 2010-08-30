from django.core.cache import cache
from pipettes import pipettes as registry
import datetime


def refresh_cache(pipette_names):
	"""Perform a hard refresh of all caches associated with the given pipettes."""
	pipettes = [(name, registry[name]) for name in pipette_names if name in registry]
	for name, pipette in pipettes:
		cache_key = 'pipette_%s' % name
		cached = cache.get(cache_key)
		
		if cached is None:
			continue
		
		for args in cached:
			try:
				new_context = pipette.get_context(*args)
			except:
				new_context = {}
			
			if new_context:
				cached[args] = {
					'time': datetime.datetime.now(),
					'context': new_context
				}
			else:
				cached[args]['time'] = datetime.datetime.now()
			
			cache.set(cache_key, cached, (pipette.cache_for+5)*60)


def create_cache(pipette_name, args):
	"""Force creation of a cache for a pipette with a certain set of args.
	If the cache for those args already exists, it will be updated."""
	if pipette_name not in registry:
		return
	
	cache_key = 'pipette_%s' % pipette_name
	pipette = registry[pipette_name]
	cached = cache.get(cache_key)
	
	if cached is None:
		cached = {}
	
	try:
		new_context = pipette.get_context(*args)
	except:
		new_context = {}
	
	if new_context or args not in cached:
		cached[args] = {
			'time': datetime.datetime.now(),
			'context': new_context
		}
	else:
		# If a cached version exists and there's no current information, poke the cache time.
		cached[args]['time'] = datetime.datetime.now()
	
	cache.set(cache_key, cached, (pipette.cache_for+5)*60)