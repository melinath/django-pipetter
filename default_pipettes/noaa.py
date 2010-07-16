"""
Registers a pipette to be used with the syntax: {% noaa <stationkey> %}

Requires python-weather, which pulls from NOAA.
"""


import Weather


class pipette(Weather.Station):
	@classmethod
	def get_context(self, station):
		instance = self(station)
		return instance.context
	
	@property
	def context(self, vars=['temp_f', 'temp_c', 'link', 'weather']):
		return dict([(k, v) for k,v in self.items()])