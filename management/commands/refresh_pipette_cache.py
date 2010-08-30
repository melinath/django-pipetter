from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from pipettes.utils import refresh_cache
import urllib2


class Command(BaseCommand):
	args = '<pipette_name pipette_name ...>'
	help = 'Refreshes all current caches for the given pipettes.'
	
	def handle(self, *args, **options):
		url = 'http://%s%s/' % (Site.objects.get_current().domain, reverse('pipettes.views.refresh_cache', kwargs={'pipette_names': '/'.join(args)}))
		urllib2.urlopen(url)
		self.stdout.write('Caches reset.')