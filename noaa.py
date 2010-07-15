"""Registers a pipette to be used with the syntax: {% noaa <stationkey> %}"""

# Relies on python-weather, which pulls from NOAA.


import Weather


class pipette(Weather.Station):
	template = 'pipettes/noaa.html'
	takes_context = False
	
	@classmethod
	def get_context(self, var):
		instance = self(var)
		return instance.context
	
	@property
	def context(self, vars=['temp_f', 'temp_c', 'link', 'weather']):
		return dict([(k, v) for k,v in self.items()])