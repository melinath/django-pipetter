from pipettes import noaa


class NotRegistered(Exception):
	pass


class AlreadyRegistered(Exception):
	pass


class Pipettes(object):
	def __init__(self):
		self._registry = {}
	
	def register(self, pipette):
		# FIXME: could check to be sure that the required attributes and methods are in place.
		tag = pipette.__module__.rsplit('.', 1)[-1]
		
		if tag in self._registry:
			raise AlreadyRegistered('Pipette tag %s was already registered.' % tag)
		
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
pipettes.register(noaa.pipette)