import time

class PredictorData:
	def __init__(self):
		self.data = {}

		""" schedule - Hourslots for when to check for updates. 1 - check, 0 - don't check"""
		self.data['schedule'] = [[1 if (i+24*j)%Predictor.weedRate == 0 else 0 for i in range(24)] for j in range(7)]
		
		""" updateRanges - """
		self.data['updateRanges'] = []

		""" locked - Avoid recalculating schedule whenever updateRanges are updated """
		self.data['locked'] = True

		""" weeding - Initial state where schedule with frequent checks are used to determine
		initial updateRanges """
		self.data['weeding'] = True

		""" weedingStartDate - (weekday, hour) when weeding started """
		self.data['weedingStart'] = time.gmtime().tm_wday, time.gmtime().tm_hour


class Predictor:
	""" Contains the methods for predicting updates and storing predicotData """

	""" weedingRate - The rate the comic is checked for updates during weeding:
	1 - every hour, 2 - every second hour, etc. """
	weedingRate = 2;


	def __init__(self):


	def updatePredictorData(self, comicId, url):


	def initializePredictorData(self, comicId):


