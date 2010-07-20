"""
Registers a tag with the syntax:
{% twitter [<user>] [<messages>] %}

Requires python-twitter
"""
try:
	import twitter
except ImportError:
	pass
else:
	from pipettes.registry import pipettes
	from django.conf import settings


	class TwitterPipette(object):
		tag_name = 'twitter'
	
		def __init__(self):
			self.api = twitter.Api()
		
		def get_context(self, user=getattr(settings, 'PIPETTES_TWITTER_USER', None),
						messages='5'):
			messages = int(messages)
			return {'statuses': self.api.GetUserTimeline(user)[:messages]}
	
	
	pipettes.register(TwitterPipette())