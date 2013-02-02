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
			#					'position': (int, int) - dayhour tuple for position of the range
			#					'updateHistory': [ (int, int), .. ] - List of dayhour of previous updates
			#					'width': int - Width of range. Predictor.rangeWidth
			# 				}
			self.__data['updateRange'] = []

			# locked - Avoid recalculating schedule whenever updateRanges are updated
			self.__data['locked'] = True

			# weeding - Initial state where schedule with frequent checks are used to determine initial updateRanges
			self.__data['weeding'] = True

			# weedingStartDate - (weekday, hour) when weeding started
			self.__data['weedingStart'] = time.gmtime().tm_mday, time.gmtime().tm_wday, time.gmtime().tm_hour
		else:
			self.__data = json.loads(dataString)

	def setSchedule(self, schedule):
		if (not self.__data['locked']):
			self.__data['schedule'] = schedule

	def addDayHour(self, dayHour):
		#TODO: Pop any number of excess elements, not just 1.
		for uRange in self.__data['updateRange']:
			if (Predictor.isInUpdateRange(dayHour, uRange)):				
				if (len(uRange['updateHistory']) >= Predictor.rangeHistorySize):
					uRange['updateHistory'].pop(0)
				uRange['updateHistory'].append(dayHour)
				return True
		return False

	def addUpdateRange(self, uRange):
		self.__data['updateRanges'].append(uRange)	

	def getUpdateRanges(self):
		return self.__data['updateRange']

	def isWeeding(self):
		return self.__data['weeding']

	def stopWeeding(self):
		self.__data['locked'] = False
		self.__data['weeding'] = False

	def getWeedingStart():
		return self.__data['weedingStart']

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
		self.__data['updateRange'].append({ 'position': (1,5), 'updateHistory': [(1,2), (1,5), (1,6), (1,3)], 'width': 2 })
		self.__data['updateRange'].append({ 'position': (2,10), 'updateHistory': [(2,10), (2,11), (2,7), (2,9)], 'width': 2 })

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
	directory = "Cache/predictorInfo/"

	# rangeWidth - The width in hours of the updateRanges
	rangeWidth = 2

	# rangeHistorySize - how many dayhours will be stored in the update history of each range
	rangeHistorySize = 64

	# weedingRate - The rate the comic is checked for updates during weeding
	# 1 - every hour, 2 - every second hour, etc.
	weedingRate = 1


	#
	# Prediction
	#

	@staticmethod
	def isInUpdateRange(dayHour, updateRange):
		urm = updateRange['position'][0] * 24 + updateRange['position'][1]
		urw = updateRange['width']
		dh = (dayHour[0] * 24 + dayHour[1])%(7*24)

		if (urm - urw <= 0 or urm + urw >= 7*24):
			if ((urm - urw)%(7*24) <= dh or dh <= (urm + urw)%(7*24)):
				return True 
		elif ((urm - urw)%(7*24) <= dh <= (urm + urw)%(7*24)):
			return True
		return False

	@staticmethod
	def blankSchedule():
		return [[0 for i in range(24)] for j in range(7)]

	@staticmethod
	def blankUpdateRange(dayHour):
		return { 'position': dayHour, 'updateHistory': dayHour, 'width': Predictor.rangeWidth }

	@staticmethod
	def moveDayHour(dayHour, step):
		dayHour = dayHour[0] * 24 + dayHour[1]
		dayHour += step
		day = dayHour%(7*24)/24
		hour = dayHour%(7*24) - day*24
		return day, hour

	def calculateScheduleUR(self, updateRanges):
		schedule = self.blankSchedule()
		for uRange in updateRanges:
			urMin = (uRange['position'][0] * 24 + uRange['position'][1] - uRange['width'])
			urMax = (uRange['position'][0] * 24 + uRange['position'][1] + uRange['width'])
			for i in range(urMin, urMax + 1):
				day = i%(7*24)/24
				hour = i%(7*24) - day*24
				print(day,hour)
				schedule[day][hour] = 1
		return schedule

	def calculateScheduleDHL(self, dayHourList):
		schedule = self.blankSchedule()
		for dayHour in dayHourList:
			schedule[dayHour[0]][dayHour[1]] = 1
		return schedule

	def generatePredictorDataTemplate(self):
		""" Stores default predictorData in 'Predictor.directory/predictorData.txt' """
		self.__pdir = Predictor.directory
		self.__predictorData = PredictorData(None)
		self.save()

	def update(self, dayHour, comicId):
		""" Called whenever a comic has been updated """
		self.load(comicId)

		if (self.__predictorData.weeding()):
			uRanges = self.__predictorData.getUpdateRanges()
			if (len(uRanges) > 0):
				if (self.__predictorData.addDayHour(dayHour)):
					return
				if (isInUpdateRange(moveDayHour(dayHour, -self.rangeWidth), uRange[-1])):
					uRangeLast = moveDayHour(uRange[-1]['position'], uRange[-1]['width'])
					self.__predictorData.addUpdateRange(self.addUpdateRange(moveDayHour(uRangeLast, Predictor.rangeWidth + 1)))
				else:		
					self.__predictorData.addUpdateRange(self.blankUpdateRange(dayHour))

		else:
			self.__predictorData.addDayHour(dayHour)
			self.__predictorData.setSchedule(self.calculateScheduleUR(self.__predictorData.getUpdateRanges()))
		self.save(comicId)

	def setSchedule(self, dayHourList, comicId):
		self.load(comicId)
		__predictorData.setSchedule(calculateScheduleDHL(dayHourList))
		self.save(comicId)


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

	def testInUR(self):
		print('bordercase0' )
		updateRange = { 'position': (0,0), 'width': 2 }
		dh = (6,21)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (6,22)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (0,2)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (0,3)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		
		print('bordercase1')
		updateRange = { 'position': (6,23), 'width': 2 }
		dh = (6,20)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (6,21)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (0,1)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (0,2)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))

		print('normalcase0')
		updateRange = { 'position': (1,23), 'width': 2 }
		dh = (1,20)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (1,21)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (2,1)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))
		dh = (2,2)
		print(dh, updateRange, self.isInUpdateRange(dh, updateRange))

	def testCalcSched(self):
		updateRanges = []
		updateRanges.append({ 'position': (0,0), 'width': 2 })
		updateRanges.append({ 'position': (4,23), 'width': 2 })
		updateRanges.append({ 'position': (2,10), 'width': 2 })
		schedule = self.calculateScheduleUR(updateRanges)
		print(schedule)
		print(schedule[6][22] == True)
		print(schedule[0][2] == True)
		print(schedule[4][21] == True)
		print(schedule[5][1] == True)
		print(schedule[2][8] == True)
		print(schedule[2][12] == True)

	def testMoveDayHour(self):
		dh = (6,23)
		print(dh, self.moveDayHour(dh, 1))


if __name__ == "__main__":
	p = Predictor()
	p.testMoveDayHour()
	