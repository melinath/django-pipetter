#!/usr/bin/env python

from setuptools import setup, find_packages

version = __import__('pipetter').VERSION

setup(
		name='Pipetter',
		version='.'.join([str(v) for v in version]),
		description='Uniform registration and processing of inclusion tags for information pulled from other sources, such as websites.',
		packages = find_packages(),
		extras_require = {
			'twitter': ['pytwitter'],
			'noaa': ['BeautifulSoup']
		}
	)