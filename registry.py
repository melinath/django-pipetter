from inspect import ismethod


class NotRegistered(Exception):
	pass


class AlreadyRegistered(Exception):
	pass


class PipetteError(Exception):
	pass


class Pipettes(object):
	def __init__(self):
		self._registry = {}
	
	def register(self, pipette):
		# FIXME: could check to be sure that the required attributes and methods are in place.
		if not hasattr(pipette, 'get_context') or not ismethod(pipette.get_context):
			raise PipetteError('%s does not define a get_context method' % pipette)
		
		tag = getattr(pipette, 'tag_name', pipette.__module__.rsplit('.', 1)[-1])
		
		if tag in self._registry:
			raise AlreadyRegistered('Pipette tag %s was already registered.' % tag)
		
		# Set some defaults
		if not hasattr(pipette, 'template'):
			pipette.template = "pipettes/%s.html" % tag
		
		if not hasattr(pipette, 'takes_context'):
			pipette.takes_context = False
		
		if not hasattr(pipette, 'cache_for'):
			pipette.cache_for = 5
		
		self._registry[tag] = pipette
	
	def unregister(self, pipette):	
		tag = pipette.__module__.rsplit('.', 1)[-1]
		
		if tag not in self._registry:
			raise NotRegistered('Pipette tag %s is not registered' % tag)
		elif self._registry[tag] != pipette:
			raise NotRegistered('A different pipette is registered as tag %s' % tag)
		
		self._registry.remove(pipette)
	
	def __iter__(self):
		return self._registry.__iter__()
	
	def items(self):
		return self._registry.items()


pipettes = Pipettes()