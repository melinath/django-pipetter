from pipettes.default_pipettes import default_pipettes
from inspect import ismethod
import re


class NotRegistered(Exception):
	pass


class AlreadyRegistered(Exception):
	pass


class PipetteError(Exception):
	pass


PIPETTE_TAG_NAME_RE = re.compile("^[a-zA-Z0-9]\w*$")


class PipetteRegistry(object):
	def __init__(self):
		self._registry = {}
	
	def register(self, pipette, tag_name=None):
		if not hasattr(pipette, 'get_context') or not ismethod(pipette.get_context):
			raise PipetteError('%s does not define a get_context method' % pipette)
		
		if tag_name is None:
			tag_name = getattr(pipette, 'tag_name', pipette.__module__.rsplit('.', 1)[-1])
		
		if not PIPETTE_TAG_NAME_RE.match(tag_name):
			raise PipetteError("%s is not a valid tag name." % tag_name)
		
		if tag_name in self._registry:
			raise AlreadyRegistered('Pipette tag %s was already registered.' % tag_name)
		
		# Set some defaults
		if not hasattr(pipette, 'template'):
			pipette.template = "pipettes/%s.html" % tag_name
		
		if not hasattr(pipette, 'takes_context'):
			pipette.takes_context = False
		
		if not hasattr(pipette, 'cache_for'):
			pipette.cache_for = 5
		
		self._registry[tag_name] = pipette
	
	def unregister(self, pipette, tag_name=None):
		if tag_name is None:
			tag_name = getattr(pipette, 'tag_name', pipette.__module__.rsplit('.', 1)[-1])
		
		if tag_name not in self._registry:
			raise NotRegistered('Pipette tag %s is not registered' % tag_name)
		elif self._registry[tag_name] != pipette:
			raise NotRegistered('A different pipette is registered as tag %s' % tag_name)
		
		self._registry.remove(pipette)
	
	def __iter__(self):
		return self._registry.__iter__()
	
	def items(self):
		return self._registry.items()
	
	def __getitem__(self, key):
		return self._registry[key]


pipettes = PipetteRegistry()
for pipette in default_pipettes:
	pipettes.register(pipette)


def autodiscover():
	"""
	Auto-discover INSTALLED_APPS pipettes.py files and force an import
	on them. This function should be called from a module which is
	known to run, such as a models.py or urls.py file. Modeled off of
	django.contrib.admin.autodiscover().
	"""
	import copy
	from django.conf import settings
	from django.utils.importlib import import_module
	from django.utils.module_loading import module_has_submodule
	
	for app in settings.INSTALLED_APPS:
		if app == __package__:
			# Don't try to import from the package we're in, i.e. pipettes.
			continue
		
		mod = import_module(app)
		try:
			before_import_registry = copy.copy(pipettes._registry)
			import_module('%s.pipettes' % app)
		except:
			# Reset the registry to the state before last import.
			pipettes._registry = before_import_registry
			# Decide whether to bubble up this error. If there is no
			# submodule, we can ignore the error as a misguided import
			# attempt. Otherwise, we want it to bubble up.
			if module_has_submodule(mod, 'pipettes'):
				raise