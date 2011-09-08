from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from pipetter.utils import refresh_cache
import urllib2
from django.contrib.sites.models import Site


class Command(BaseCommand):
	args = '<pipette_name pipette_name ...>'
	help = 'Refreshes all current caches for the given pipettes.'
	
	def handle(self, *args, **options):
		url = 'http://%s%s' % (Site.objects.get_current().domain, reverse('pipetter.views.refresh_cache', kwargs={'pipette_names': ''.join(['%s/' % arg for arg in args])}))
		urllib2.urlopen(url)
		print 'Caches reset.\n\n'