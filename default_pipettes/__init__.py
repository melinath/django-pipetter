from pipettes.default_pipettes import noaa
from pipettes.registry import pipettes


__all__ = (
	'noaa',
)


pipettes.register(noaa.pipette)