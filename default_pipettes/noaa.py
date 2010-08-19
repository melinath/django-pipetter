"""
Registers a pipette to be used with the syntax:
{% noaa <stationkey> [<datakeys>]%}

Depends on BeautifulSoup.
"""
try:
	from BeautifulSoup import BeautifulSoup
except:
	pass
else:
	import urllib2
	
	
	class NoaaPipette(object):
		cache_for = 30
		
		def get_context(self, station, datakeys=['temp_f', 'temp_c', 'link', 'weather']):
			page = urllib2.urlopen('http://www.weather.gov/xml/current_obs/%s.xml' % station)
			soup = BeautifulSoup(page)
			context = {}
			for key in datakeys:
				try:
					context[key] = getattr(soup, key).string
				except:
					pass
			return context