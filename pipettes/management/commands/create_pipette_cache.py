from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from pipettes.utils import create_cache
import urllib2


class Command(BaseCommand):
	args = '<pipette_name> <arg1 arg2 ...>'
	help = 'Creates a cache for the given pipette with the given args.'
	
	def handle(self, *args, **options):
		url = 'http://%s%s/' % (Site.objects.get_current().domain, reverse('pipettes.views.create_cache', kwargs={'pipette_name': args[0], 'argstr': '/'.join(args[1:])}))
		import pdb
		pdb.set_trace()
		urllib2.urlopen(url)
		self.stdout.write('Cache created.')