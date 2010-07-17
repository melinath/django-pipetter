"""
Registers a pipette to be used with the syntax:
{% noaa <stationkey> [<datakeys>]%}

Requires python-weather, which pulls from NOAA.
"""


import Weather


class pipette(Weather.Station):
	@classmethod
	def get_context(self, station, datakeys=['temp_f', 'temp_c', 'link', 'weather']):
		instance = self(station)
		instance.datakeys = datakeys
		return instance.context
	
	@property
	def context(self, vars):
		return dict([(k, v) for k,v in self.items() if k in self.datakeys])