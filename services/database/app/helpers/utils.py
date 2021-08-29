class Utils(object):
	@staticmethod
	def create_guild_settings(settings):
		settingsTemplate = {
			"addons": {
				"satellites": {
					"enabled": False
				},
				"marketAlerts": {
					"enabled": False
				},
				"commandPresets": {
					"enabled": False
				},
				"flow": {
					"enabled": False
				},
				"statistics": {
					"enabled": False
				}
			},
			"settings": {
				"assistant": {
					"enabled": True
				},
				"channels": {
					"public": None,
					"private": None
				},
				"cope": {
					"holding": [],
					"voting": []
				},
				"messageProcessing": {
					"bias": "traditional",
					"autodelete": False,
					"sentiment": True
				},
				"setup": {
					"completed": False,
					"connection": None,
					"tos": 1.0
				}
			}
		}

		if settings is None: settings = {}
		Utils.__recursive_fill(settings, settingsTemplate)

		return settings

	@staticmethod
	def __recursive_fill(settings, template):
		for e in template:
			if type(template[e]) is dict:
				if e not in settings:
					settings[e] = template[e].copy()
				else:
					Utils.__recursive_fill(settings[e], template[e])
			elif e not in settings:
				settings[e] = template[e]