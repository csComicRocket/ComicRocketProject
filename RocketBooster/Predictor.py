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

			# weedingStart - seconds since the epoch when weeding started
			tgm = time.gmtime()
			self.__data['weedingStartSec'] = time.mktime(time.strptime(str(tgm.tm_year) +' '+ str(tgm.tm_mon) +' '+ str(tgm.tm_mday) +' '+ str(tgm.tm_hour), '%Y %m %d %H'))
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
		""" Add dayHour to the updateRange which spans it """
		for i, uRange in enumerate(self.__data['updateRange']):
			if (Predictor.inURange(dayHour, uRange)):				
				self.addDayHourToURange(dayHour, i)
				return True
		return False

	def addDayHourToURange(self, dayHour, index):
		""" Add dayHour to the updateRange with the given index """
		ur_hist_len = len(self.__data['updateRange'][index]['updateHistory']) - Predictor.rangeHistorySize
		if (ur_hist_len > 0):
			for i in ur_hist_len:
				self.__data['updateRange'][i]['updateHistory'].pop(0)
		self.__data['updateRange'][index]['updateHistory'].append(dayHour)

	def addUpdateRange(self, uRange):
		self.__data['updateRange'].append(uRange)	

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



class Predictor:
	""" Contains the methods for predicting updates from predictorData and storing predicorData """

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
		""" Checks whether or not dayHour is in updateRange """
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
		""" Generate blank schedule """
		return [[0 for i in range(24)] for j in range(7)]

	@staticmethod
	def blankUpdateRange(dayHour):
		""" Generate blank updateRange with position dayHour """
		return { 'position': dayHour, 'updateHistory': [dayHour], 'width': Predictor.rangeWidth }

	@staticmethod
	def dayHourToHours(dayHour):
		""" Convert from dayHour to hours """
		return dayHour[0] * 24 + dayHour[1]

	@staticmethod
	def hoursToDayHour(hours):
		""" Convert from hours to dayHour """
		day = hours%(7*24)/24
		hour = hours%(7*24) - day*24
		return day, hour

	def incDayHour(self, dayHour, step):
		""" Increment a dayHour by step """
		hours = dayHour[0] * 24 + dayHour[1]
		hours += step
		return self.hoursToDayHour(hours)

	def calculateURPositions(self, updateRanges):
		""" Calculates average position of each updateRange from the updateHistory of the updateRange """
		ranges = []
		prevRange = updateRanges[-1]
		positions = []

		for uRange in updateRanges:
			hend = len(uRange['updateHistory'])
			hstart = 0 if hend - self.rangeHistN < 0 else hend - self.rangeHistN
			hPos = [0, 0, 0]
			
			for i in range(hstart, hend):
				hPos[1] = self.dayHourToHours(uRange['updateHistory'][i])
				hPos[0] = hPos[1] - 7*24
				hPos[2] = hPos[1] + 7*24

				if (len(positions) == 0):
					positions.append(hPos[1])
				else:
					hDist = {}

					for p in hPos:
						if (positions[0] <= p <= positions[-1]):
							hDist[0] = p
							break
						else:
							hDist[min(abs(positions[0] - p), abs(positions[-1] - p))] = p					

					positions.append(hDist[min(hDist.keys())])
					positions.sort()

			uRange['position'] = self.hoursToDayHour(int(round(float(sum(positions)) / len(positions))))
			ranges.append(uRange)
			positions = []

		return ranges	

	def calculateScheduleUR(self, updateRanges):
		""" Calculates schedule from updateRanges """
		schedule = self.blankSchedule()
		for uRange in updateRanges:
			urMin = (uRange['position'][0] * 24 + uRange['position'][1] - uRange['width'])
			urMax = (uRange['position'][0] * 24 + uRange['position'][1] + uRange['width'])
			for i in range(urMin, urMax + 1):
				day = i%(7*24)/24
				hour = i%(7*24) - day*24
				schedule[day][hour] = 1
		return schedule

	def calculateScheduleDHL(self, dayHourList):
		""" Calculate schedule from list of dayHours """
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
		#TODO test
		""" Called whenever a comic has been updated """
		self.load(comicId)

		for i in range(1):
			# Stop weeding?
			if (self.__predictorData.weeding()):
				tgm = time.gmtime()
				sec = time.mktime(time.strptime(str(tgm.tm_year) +' '+ str(tgm.tm_mon) +' '+ str(tgm.tm_mday) +' '+ str(dayHour[1]), '%Y %m %d %H'))
				if (sec >= self.__predictorData.getWeedingStart() + 7*24*60*60):
					self.__predictorData.stopWeeding()

			if (self.__predictorData.weeding()):
				# Weeding
				uRanges = self.__predictorData.getUpdateRanges()
				if (len(uRanges) > 0):
					if (self.__predictorData.addDayHour(dayHour)):
						break
					if (inURange(incDayHour(dayHour, -self.rangeWidth), uRanges[-1])):
						uRangeLast = incDayHour(uRanges[-1]['position'], uRanges[-1]['width'])
						self.__predictorData.addUpdateRange(self.addUpdateRange(incDayHour(uRangeLast, Predictor.rangeWidth + 1)))
						break	
				self.__predictorData.addUpdateRange(self.blankUpdateRange(dayHour))
			else:
				# Regular update
				if (not self.__predictorData.addDayHour(dayHour)):
					# Add dayHour to nearest range
					updateRanges = self.__predictorData.getUpdateRanges()
					dist = {}
					dh = self.dayHourToHours(dayHour)
					for i, uRange in enumerate(updateRanges):
						ur_pos_hours = self.dayHourToHours(uRange['position'])
						ur_width = uRange['width']
						hours = self.dayHourToHours(dayHour)
						dist[min(abs(ur_pos_dh - ur_width - hours), abs(ur_pos_dh + ur_width - hours))] = i
					self.__predictorData.addDayHourToURangeange(dayHour, dist[min(dist.keys())])

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
		return [[[] for i in range(24)] for j in range(7)]

	def scanDirectory(self, comicId):
		#TODO test
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
		return self.load()


	def load(self):
		try:
			os.makedirs(self.__pdir)
		except OSError:
			pass
		try:
			with open(self.__pdir + self.__pfile, 'r') as f:
				self.__predictorData = PredictorData(f.readline())
			f.close()
		except IOError:
			return
		return True

	def save(self, comicId):
		self.__pdir = self.directory + str(comicId) + "/"
		return self.save()


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

	def runTests(self):
		t = []


		# Predictor.inUrange()

		t_fname = 'PredictorData.addDayHourToURange'

		# 0
		updateRange = { 'position': (0,0), 'width': 2 }
		t_num = 0
		dh = (6,21)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		dh = (6,22)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		dh = (0,2)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 3
		t_num = 3
		dh = (0,3)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 4
		updateRange = { 'position': (6,23), 'width': 3 }
		t_num = 4
		dh = (6,19)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 5
		t_num = 5
		dh = (6,21)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 6
		t_num = 6
		dh = (0,1)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 7
		t_num = 7
		dh = (0,3)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 8
		updateRange = { 'position': (1,23), 'width': 2 } 
		t_num = 8
		dh = (1,20)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 9
		t_num = 9
		dh = (1,21)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 10
		t_num = 10
		dh = (2,1)
		t_res = self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))

		# 11
		t_num = 11
		dh = (2,2)
		t_res = not self.inURange(dh, updateRange)
		t.append(( t_fname, t_num, t_res ))


		# Predictor.generatePredictorDataTemplate()

		t_fname = 'Predictor.generatePredictorDataTemplate'

		def test_gpdt_weedingrate(weedingRate):
			temp_weedingRate = Predictor.weedingRate
			Predictor.weedingRate = weedingRate
			self.generatePredictorDataTemplate()
			self.__pdir = Predictor.directory
			self.load()
			schedule = self.__predictorData.getSchedule()
			for d, day in enumerate(schedule):
				for h, hour in enumerate(day):
					i = d*24+h
					if (hour != 1 and i%Predictor.weedingRate == 0):
						return False
					elif (hour == 0 and i%Predictor.weedingRate == 0):
						return False
			Predictor.weedingRate = temp_weedingRate
			return True

		# 0
		t_num = 0 
		t_res = True
		try:
			self.generatePredictorDataTemplate()
		except IOError, OSError:
			t_res = False
		if (not os.path.isdir(self.directory)):
			t_res = False	
		try:
   			with open(self.directory + "/" + self.__pfile) as f: pass
		except IOError as e:
			t_res = False
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		t_res = test_gpdt_weedingrate(1)
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		t_res = test_gpdt_weedingrate(3)
		t.append(( t_fname, t_num, t_res ))

		# 3
		t_num = 3
		t_res = test_gpdt_weedingrate(5)
		t.append(( t_fname, t_num, t_res ))

		# cleanup
		self.generatePredictorDataTemplate()


		# Predictor.calculateScheduleUR()

		t_fname = 'Predictor.calculateScheduleUR'
		updateRanges = []
		updateRanges.append({ 'position': (0,0), 'width': 2 })
		updateRanges.append({ 'position': (4,23), 'width': 4 })
		updateRanges.append({ 'position': (2,10), 'width': 2 })
		schedule = self.calculateScheduleUR(updateRanges)

		# 0
		t_num = 0
		t_res = schedule[6][22] == 1
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		t_res = schedule[6][21] == 0
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		t_res = schedule[0][0] == 1
		t.append(( t_fname, t_num, t_res ))

		# 3
		t_num = 3
		t_res = schedule[0][2] == 1
		t.append(( t_fname, t_num, t_res ))

		# 4
		t_num = 4
		t_res = schedule[0][3] == 0
		t.append(( t_fname, t_num, t_res ))

		# 5
		t_num = 5
		t_res = schedule[4][19] == 1
		t.append(( t_fname, t_num, t_res ))

		# 6
		t_num = 6
		t_res = schedule[4][18] == 0
		t.append(( t_fname, t_num, t_res ))

		# 7
		t_num = 7
		t_res = schedule[5][3] == 1
		t.append(( t_fname, t_num, t_res ))

		# 8
		t_num = 8
		t_res = schedule[5][4] == 0
		t.append(( t_fname, t_num, t_res ))

		# 9
		t_num = 9
		t_res = schedule[2][10] == 1
		t.append(( t_fname, t_num, t_res ))

		# 10
		t_num = 10
		t_res = schedule[2][13] == 0
		t.append(( t_fname, t_num, t_res ))


		# Predictor.calculateScheduleDHL()

		t_fname = 'Predictor.calculateScheduleDHL'
		schedule = self.blankSchedule()
		dayHourList = []

		# 0
		t_num = 0
		schedule = self.calculateScheduleDHL(dayHourList)
		for day in schedule:
			for hour in day:
				if (hour != 0):
					t_res = False
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		dayHourList.append((6,20))
		schedule = self.calculateScheduleDHL(dayHourList)
		t_res = schedule[6][20] == 1
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		dayHourList.append((0,0))
		schedule = self.calculateScheduleDHL(dayHourList)
		t_res = schedule[0][0] == 1
		t.append(( t_fname, t_num, t_res ))
		
		# 3
		t_num = 3
		dayHourList.append((3,23))
		schedule = self.calculateScheduleDHL(dayHourList)
		t_res = schedule[3][23] == 1
		t.append(( t_fname, t_num, t_res ))


		# Predictor.calculateURPositions()

		t_fname = 'Predictor.calculateURPositions'
		updateRanges = []
		updateRanges.append({ 'position': (0,0), 'updateHistory': [(0,1), (0,3), (0,1), (0,3)], 'width': 2 })
		updateRanges.append({ 'position': (0,0), 'updateHistory': [(6,23), (0,0), (0,1), (0,0)], 'width': 2 })
		updateRanges.append({ 'position': (0,0), 'updateHistory': [(0,0), (3,11), (6,23)], 'width': 2 })
		updateRanges.append({ 'position': (0,0), 'updateHistory': [(3,13), (0,0), (6,23)], 'width': 2 })
		updateRanges = self.calculateURPositions(updateRanges)

		# 0
		t_num = 0
		t_res = updateRanges[0]['position'] == (0,2)
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		t_res = updateRanges[1]['position'] == (0,0)
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		t_res = 25 < self.dayHourToHours(updateRanges[2]['position']) < 30
		t.append(( t_fname, t_num, t_res ))
		
		# 3
		t_num = 3
		t_res = 139 < self.dayHourToHours(updateRanges[3]['position']) < 143
		t.append(( t_fname, t_num, t_res ))


		# PredictorData.addDayHourToURange()
		
		t_fname = 'PredictorData.addDayHourToURange'
		self.__predictorData = PredictorData(None)
		self.__predictorData.addUpdateRange(self.blankUpdateRange((0, 0)))

		# 0
		t_num = 3
		dh = (3, 3)
		index = 0
		self.__predictorData.addDayHourToURange(dh, index)
		t_res = self.__predictorData.getUpdateRanges()[index]['updateHistory'][1] == dh
		t.append(( t_fname, t_num, t_res ))

		# cleanup
		self.__predictorData = None

		# PredictorData.addDayHour()
	
		t_fname = 'PredictorData.addDayHour'
		self.__predictorData = PredictorData(None)
		self.__predictorData.addUpdateRange(self.blankUpdateRange((0, 0)))
		self.__predictorData.addUpdateRange(self.blankUpdateRange((1, 5)))

		# 0
		t_num = 0
		t_res = True
		ur_width = self.__predictorData.getUpdateRanges()[0]['width']
		dh = self.incDayHour((0,0), -ur_width)
		if (not self.__predictorData.addDayHour(dh)):
			t_res = False
		if (self.__predictorData.getUpdateRanges()[0]['updateHistory'][-1] != dh):
			t_res = False
		t.append(( t_fname, t_num, t_res ))

		# 1
		t_num = 1
		t_res = True
		ur_width = self.__predictorData.getUpdateRanges()[0]['width']
		dh = self.incDayHour((0,0), -ur_width-1)
		if (self.__predictorData.addDayHour(dh)):
			t_res = False
		if (self.__predictorData.getUpdateRanges()[0]['updateHistory'][-1] == dh):
			t_res = False
		t.append(( t_fname, t_num, t_res ))

		# 2
		t_num = 2
		ur_width = self.__predictorData.getUpdateRanges()[1]['width']
		t_res = self.__predictorData.addDayHour((1,5))
		t.append(( t_fname, t_num, t_res ))

		return t


if __name__ == "__main__":
	p = Predictor()
	tests = p.runTests()

	print '\nTests:'
	for test in tests:
		print test
	print '\nErrors:'
	for test in tests:
		if (not test[2]):
			print test[0], test[1]
	