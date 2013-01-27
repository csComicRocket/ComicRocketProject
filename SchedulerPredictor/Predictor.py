import time
import json
import os

class PredictorData:
	""" Datatype for the prediction of a given comic """

	def __init__(self, dataString):
		if (not dataString):
			self.__data = {}

			# schedule - Hourslots for when to check for updates
			# 1 - check, 0 - don't check
			self.__data['schedule'] = [[1 if (i+24*j)%Predictor.weedingRate == 0 else 0 for i in range(24)] for j in range(7)]
			
			# updateRange - List of ranges for anticipated updates
			# Range format	{	
			#					'midPoint': (int, int) - dayhour tuple for midpoint of the range
			#					'updateHistory': [ (int, int), .. ] - List of dayhour of previous updates
			#					'width': int - Width of range. Predictor.rangeWidth
			# 				}
			self.__data['updateRange'] = []

			# locked - Avoid recalculating schedule whenever updateRanges are updated
			self.__data['locked'] = True

			# weeding - Initial state where schedule with frequent checks are used to determine initial updateRanges
			self.__data['weeding'] = True

			# weedingStartDate - (weekday, hour) when weeding started
			self.__data['weedingStart'] = time.gmtime().tm_wday, time.gmtime().tm_hour
		else:
			self.__data = json.loads(dataString)

	def addDayHour(self, dayHour):
		#TODO: Pop any number of excess elements, not just 1.
		for uRange in self.__data['updateRange']:
			if (Predictor.isInUpdateRange(dayHour, uRange)):				
				if (len(uRange['updateHistory']) >= Predictor.rangeHistorySize):
					uRange['updateHistory'].pop(0)
				uRange['updateHistory'].append(dayHour)
				return

	def Lock(self):
		self.__data['locked'] = True

	def Unlock(self):
		self.__data['locked'] = False

	def toString(self):
		return json.dumps(self.__data)


	#
	# Testing
	#

	def testSetUR(self):
		self.__data['updateRange'].append({ 'midPoint': (1,5), 'updateHistory': [(1,2), (1,5), (1,6), (1,3)], 'width': 2 })
		self.__data['updateRange'].append({ 'midPoint': (2,10), 'updateHistory': [(2,10), (2,11), (2,7), (2,9)], 'width': 2 })

	def testGetData(self):
		return self.__data


class Predictor:
	""" Contains the methods for predicting updates and storing predicorData """

	def __init__(self):
		self.__predictorData = None
		self.__pdir = None
		self.__pfile = "predictorData.txt"


	#
	# Settings
	#

	# directory - the directory of all predictor data
	directory = "predictorInfo/"

	# rangeWidth - The width in hours of the updateRanges
	rangeWidth = 2

	# rangeHistorySize - how many dayhours will be stored in the update history of each range
	rangeHistorySize = 4

	# weedingRate - The rate the comic is checked for updates during weeding
	# 1 - every hour, 2 - every second hour, etc.
	weedingRate = 2 * 2 + 1


	#
	# Static Methods
	#

	@staticmethod
	def isInUpdateRange(dayHour, updateRange):
		urm = updateRange['midPoint']
		urw = updateRange['width']

		#TODO: handle condition for ranges that span the time when the week changes
		if (urm[0] * 24 + urm[1] - urw <= dayHour[0] * 24 + dayHour[1] <= urm[0] * 24 + urm[1] + urw):
			return True
		return False


	#
	# Prediction
	#

	def generatePredictorDataTemplate(self):
		""" Stores default predictorData in 'predictorInfo/predictorData.txt' """
		self.__pdir = Predictor.directory
		self.__predictorData = PredictorData(None)
		self.save()


	def update(self, comicId):
		""" Called whenever a comic has been updated """
		self.load(comicId)
		# TODO: updatelogic
		self.save(comicId)
		return


	#
	# Save/Load
	#

	def load(self, comicId):
		self.__pdir = self.directory + str(comicId) + "/"
		self.load()


	def load(self):
		try:
			os.makedirs(self.__pdir)
		except OSError:
			pass
		try:
			with open(self.__pdir + self.__pfile, 'r') as f:
				__predictorData = PredictorData(f.readline())
			f.close()
		except IOError:
			return
		return True

	def save(self, comicId):
		self.__pdir = self.directory + str(comicId) + "/"
		self.save()


	def save(self):
		try:
			os.makedirs(self.__pdir)
		except OSError:
			pass
		try:
			with open(self.__pdir + self.__pfile, 'w') as f:
				f.write(self.__predictorData.toString())
			f.close()
		except IOError:
			return

		self.__predictorData = None
		return True


	#
	# Tests	
	#

	def testGenTemplate(self):
		self.generatePredictorDataTemplate()

		if (not os.path.isdir(self.directory)):
			return False 

		try:
   			with open(self.directory + "/" + self.__pfile) as f: pass
		except IOError as e:
			return False

		return True

	def testPDfunc(self):
		pd = PredictorData(None)
		print(pd.testGetData())
		pd.testSetUR()
		print(pd.testGetData())
		pd.addDayHour((1,3))
		pd.addDayHour((1,7))
		pd.addDayHour((2,10))
		pd.addDayHour((2,12))
		pd.addDayHour((2,8))
		print(pd.testGetData())

