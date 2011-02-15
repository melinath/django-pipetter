from django import template
from pipettes import pipettes, NotRegistered
from pipettes.utils import get_cache_or_new
from django.core.cache import cache
from django.template.loader import get_template, render_to_string
import datetime


register = template.Library()

class PipetteNode(template.Node):
	def __init__(self, pipette, args, template=None):
		self.tag_name = pipette
		self.pipette = pipettes[pipette]
		self.args = args
		self.template = template
	
	def render(self, context):
		args = tuple([bit.resolve(context) for bit in self.args])
		
		if self.template is not None:
			template_path = self.template.resolve(context)
		else:
			template_path = self.pipette.template
		
		c = template.Context(get_cache_or_new(self.tag_name, args))
		t = get_template(template_path)
		
		s = t.render(c)
		return s

def do_pipette(parser, token):
	"""
	Syntax:
	{% <pipette_name> [<arg1> <arg2> ...] [with <template>] %}
	"""
	bits = token.split_contents()
	pipette_name = bits[0]
	template = None
	
	if len(bits) > 3 and bits[-2] == 'with':
		template = bits[-1]
		bits = bits[:-2]
		
	args = tuple([parser.compile_filter(arg) for arg in bits[1:]])
	
	if template:
		template = parser.compile_filter(template)
	
	return PipetteNode(pipette_name, args, template)


for name, pipette in pipettes.items():
	register.tag(name, do_pipette)