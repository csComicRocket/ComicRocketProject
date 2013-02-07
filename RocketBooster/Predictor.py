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
			return True
		return False

	def getSchedule(self):
		return self.__data['schedule']

	def addDayHour(self, dayHour):
		#TODO: Pop any number of excess elements, not just 1.
		for uRange in self.__data['updateRange']:
			if (Predictor.inURange(dayHour, uRange)):				
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
		self.__predictorList = self.blankPredictorList()


	#
	# Settings
	#

	# directory - The directory of all predictor data
	directory = "Cache/predictorInfo/"

	# rangeWidth - The width in hours of the updateRanges
	rangeWidth = 2

	# rangeHistorySize - How many dayhours will be stored in the update history of each range
	rangeHistorySize = 64

	# rangeHistN - How many dayhours will be used to recalculate the range position
	rangeHistN = 5

	# weedingRate - The rate the comic is checked for updates during weeding
	# 1 - every hour, 2 - every second hour, etc.
	weedingRate = 1


	#
	# Prediction
	#

	@staticmethod
	def inURange(dayHour, updateRange):
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
	def dayHourToHours(dayHour):
		#TODO test
		return dayHour[0] * 24 + dayHour[1]

	@staticmethod
	def hoursToDayHour(hours):
		#TODO test
		day = hours%(7*24)/24
		hour = hours%(7*24) - day*24
		return day, hour

	def moveDayHour(self, dayHour, step):
		#TODO test
		hours = dayHour[0] * 24 + dayHour[1]
		hours += step
		return self.hoursToDayHour(hours)

	def calculateURPositions(self, updateRanges):
		''' Calculates position of each updateRange from the updateHistory of each updateRange '''
		#TODO test
		ranges = []
		prevRange = updateRanges[-1]
		positions = []
		for uRange in updateRanges:
			hend = len(uRange['updateHistory']) - 1
			hstart = 0 if hend - rangeHistN < 0 else hend - rangeHistN
			hPos = [0, 0, 0]
			hDist = {}
			for i in range(hstart, hend):
				hPos[1] = self.dayHourToHours(uRange['updateHistory'][i])
				hPos[0] = hPos[1] - 7*24
				hPos[2] = hPos[1] + 7*24

				for p in hPos:
					if (positions[0] < p < positions[-1]):
						positions.append(p)
						positions.sort()
						break
					else:
						hDist[min(abs(position[0] - p), abs(position[-1] - p))] = p
					if (p == hPos[2]):
						positions.append(hDist[min(hDist.values())])

			uRange['position'] = round(float(sum(positions)) / len(positions))
			ranges.append(uRange)
		return ranges	

	def calculateScheduleUR(self, updateRanges):
		''' Calculates schedule from updateRanges '''
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
		#TODO test
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
		#TODO fix if no range for dayHour
		#TODO test
		""" Called whenever a comic has been updated """
		self.load(comicId)

		for x in [0]:
			if (self.__predictorData.weeding()):
				# Weeding phase
				uRanges = self.__predictorData.getUpdateRanges()
				if (len(uRanges) > 0):
					if (self.__predictorData.addDayHour(dayHour)):
						break
					if (inURange(moveDayHour(dayHour, -self.rangeWidth), uRanges[-1])):
						uRangeLast = moveDayHour(uRanges[-1]['position'], uRanges[-1]['width'])
						self.__predictorData.addUpdateRange(self.addUpdateRange(moveDayHour(uRangeLast, Predictor.rangeWidth + 1)))
						break	
				self.__predictorData.addUpdateRange(self.blankUpdateRange(dayHour))
			else:
				if (not self.__predictorData.addDayHour(dayHour)):
					pass
					# If no range for dayHour, add dayHour to nearest range
					# updateRanges = self.__predictorData.getUpdateRanges()
					# dist = {}
					# dh = self.dayHourToHours(dayHour)
					# for i, uRange in enumerate(updateRanges):
					# 	updh = self.dayHourToHours(uRange['position'])
					# 	uw = uRange['width']
					# 	dist[i] = min(abs(self.dayHoursToHour(uRange['position']) - uRange['width'] - self.dayHoursToHour(dayHour)))

				self.calculateURPositions(self.__predictorData.getUpdateRanges())
				self.__predictorData.setSchedule(self.calculateScheduleUR(self.__predictorData.getUpdateRanges()))
		
		self.updatePredictorList(self.__predictorData.getSchedule(), comicId)
		self.save(comicId)

	def setSchedule(self, dayHourList, comicId):
		#TODO test
		self.load(comicId)
		__predictorData.setSchedule(calculateScheduleDHL(dayHourList))
		self.save(comicId)


	#
	# PredictorList
	#

	def updatePredictorList(schedule, comicId):
		#TODO test
		for day in range(7):
			for hour in range(24):
				if (schedule[day][hour] == 1 and not comicId in self.__predictorList[day][hour]):
					self.__predictorList[day][hour].append(comicId)
				elif (schedule[day][hour] == 0):
					while (comicId in self.__predictorList[day][hour]):
						self.__predictorList[day][hour].remove(comicId)


	def getHourList(self, dayHour):
		#TODO test
		return self.__predictorList[dayHour[0]][dayHour[1]]

	def blankPredictorList(self):
		#TODO test
		return [[[] for i in range(24)] for j in range(7)]

	def scanDirectory(self, comicId):
		self.load(comicId)
		updatePredictorList(self.__predictorData.getSchedule(), comicId)

	def scanDirectories(self):
		#TODO test
		self.__predictorList = self.blankPredictorList()
		for root, dirs, files in os.walk(d):
			for comicId in dirs:
				comicId = int(comicId)
				self.load(comicId)
				updatePredictorList(self.__predictorData.getSchedule(), comicId)
			break


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
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (6,22)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (0,2)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (0,3)
		print(dh, updateRange, self.inURange(dh, updateRange))
		
		print('bordercase1')
		updateRange = { 'position': (6,23), 'width': 2 }
		dh = (6,20)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (6,21)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (0,1)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (0,2)
		print(dh, updateRange, self.inURange(dh, updateRange))

		print('normalcase0')
		updateRange = { 'position': (1,23), 'width': 2 }
		dh = (1,20)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (1,21)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (2,1)
		print(dh, updateRange, self.inURange(dh, updateRange))
		dh = (2,2)
		print(dh, updateRange, self.inURange(dh, updateRange))

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
	