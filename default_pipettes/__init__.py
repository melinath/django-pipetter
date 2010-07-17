from pipettes.default_pipettes import noaa, twitter_pipette
from pipettes.registry import pipettes


__all__ = (
	'noaa',
	'twitter_pipette',
)


pipettes.register(noaa.pipette)
pipettes.register(twitter_pipette.pipette)