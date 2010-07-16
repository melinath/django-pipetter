from pipettes.registry import pipettes as registry
from pipettes.default_pipettes import *


def autodiscover():
	"""
	Auto-discover INSTALLED_APPS pipettes.py modules and fail silently
	when not present. Force an import on them to register any pipettes
	provided.
	"""
	
	import copy
	from django.conf import settings
	from django.utils.importlib import import_module
	from django.utils.module_loading import module_has_submodule
	
	for app in settings.INSTALLED_APPS:
		if __package__ == app:
			continue
		
		mod = import_module(app)
		
		# try importing the app's pipettes module
		try:
			before_import_registry = copy.copy(registry._registry)
			import_module('%s.pipettes' % app)
		except:
			registry._registry = before_import_registry
			if module_has_submodule(mod, 'pipettes'):
				raise