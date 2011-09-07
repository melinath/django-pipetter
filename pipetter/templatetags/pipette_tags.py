from django import template
from django.conf import settings
from pipetter import pipettes, NotRegistered
from pipetter.utils import get_cache_or_new
import datetime


register = template.Library()


class ConstantPipetteNode(template.Node):
	def __init__(self, tag_name, args, template_path=None):
		self.tag_name = tag_name
		self.pipette = pipettes[tag_name]
		self.args = args
		
		try:
			t = template.loader.get_template(template_path or self.pipette.template)
		except:
			if settings.TEMPLATE_DEBUG:
				raise
			t = None
		self.template = t
	
	def render(self, context):
		if self.template is None:
			return settings.TEMPLATE_STRING_IF_INVALID
		args = tuple([arg.resolve(context) for arg in self.args])
		c = template.Context(get_cache_or_new(self.tag_name, args))
		return self.template.render(c)


class PipetteNode(template.Node):
	def __init__(self, tag_name, args, template_path):
		self.tag_name = tag_name
		self.pipette = pipettes[tag_name]
		self.args = args
		self.template_path = template_path
	
	def render(self, context):
		try:
			template_path = self.template_path.resolve(context)
			t = template.loader.get_template(template_path)
		except:
			if settings.TEMPLATE_DEBUG:
				raise
			return settings.TEMPLATE_STRING_IF_INVALID
		
		args = tuple([arg.resolve(context) for arg in self.args])
		c = template.Context(get_cache_or_new(self.tag_name, args))
		return t.render(c)

def do_pipette(parser, token):
	"""
	Syntax:
	{% <pipette_name> [<arg1> <arg2> ...] [with <template_path>] %}
	"""
	bits = token.split_contents()
	pipette_name = bits[0]
	path = None
	
	if len(bits) > 2 and bits[-2] == 'with':
		path = bits[-1]
		bits = bits[:-2]
		
	args = [parser.compile_filter(arg) for arg in bits[1:]]
	
	
	if path:
		if path[0] not in ('"', "'") or path[0] != path[-1]:
			path = parser.compile_filter(path)
			return PipetteNode(pipette_name, args, path)
		else:
			path = path[1:-1]
	return ConstantPipetteNode(pipette_name, args, path)


for name, pipette in pipettes.items():
	register.tag(name, do_pipette)