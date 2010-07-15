"""
This module implements a generic interface for pipettes. A pipette must have two attributes:
1. template (string)
2. takes_context (True/False)

It should also have a method called get_context which will be called with all variables for the tag.

Pipette results are stored for five minutes unless specified otherwise in the pipette itself (pipette.cache_for - minutes)
"""

from django import template
from ..registry import pipettes


register = template.Library()


def pipette_context(name, pipette):
	"""Sets the pipette's name so that the tag name will be the module's name instead of get_context."""
	# FIXME: return either the actual function or a function that just pulls from the cache?
	# FIXME: find a way to set the vars do_pipette takes to the vars pipette.get_context takes
	
	def do_pipette(var):
		return pipette.get_context(var)
	do_pipette.__name__ = name
	return do_pipette


for name, pipette in pipettes.items():
	register.inclusion_tag(
		pipette.template,
		takes_context=pipette.takes_context
	)(pipette_context(name, pipette))