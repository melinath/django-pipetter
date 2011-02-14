from django import template
from pipettes import pipettes
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
		
		cache_key = 'pipette_%s' % self.tag_name
		cached = cache.get(cache_key)		
		if cached is None:
			cached = {}
		
		
		# Check if the pipette hasn't been called with these args before or if the cache time has expired.
		if (
			self.args not in cached or
			(datetime.datetime.now() - cached[self.args]['time']) > datetime.timedelta(0, 0, 0, 0, self.pipette.cache_for)
			):
			try:
				if args:
					new_context = self.pipette.get_context(*args)
				else:
					new_context = self.pipette.get_context()
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
			
			cache.set(cache_key, cached, (self.pipette.cache_for+5)*60)
		
		c = template.Context(cached[args]['context'])
		t = get_template() if template_path is None else get_template(template_path)
		
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