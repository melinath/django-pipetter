default_pipettes = []


try:
	from pipettes.default_pipettes.noaa import WeatherPipette
except ImportError:
	pass
else:
	default_pipettes.append(WeatherPipette)

try:
	from pipettes.default_pipettes.twitter_pipette import TwitterPipette
except ImportError:
	pass
else:
	default_pipettes.append(TwitterPipette)