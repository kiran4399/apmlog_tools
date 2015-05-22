try:
	import rospy
	import rosbag
	from apmlog_tools.msg import ATT
except ImportError:
	print "Can't load ROS dependencies"


class ATTHandler:
	'''ATT handler'''
	def __init__(self, name, logdata, bagfile):
		self.name = name
		self.logdata = logdata
		self.bag = bagfile

		self.msgid = 0
		self.topic = logdata.vehicleType+'/'+self.name

		self.channel = logdata.channels[self.name]
		self.timestamp_ms = self.channel["TimeMS"].listData

		self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
		self.msgs_len = len(self.timestamp_ms)

	def getTimestamp(self):
		if self.msgid < self.msgs_len:
			self.stamp = rospy.Time.from_sec(float(long(self.timestamp_ms[self.msgid][1])/1e6)) # TODO: check if conversion is correct 
			return self.stamp
		else:
			return None

	def convertData(self):

		if self.msgid < self.msgs_len:
			msg = ATT()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.DesRoll = self.channel["DesRoll"].listData[self.msgid][1]
			msg.DesYaw = self.channel["DesYaw"].listData[self.msgid][1]
			msg.ErrRP = self.channel["ErrRP"].listData[self.msgid][1]
			msg.ErrYaw = self.channel["ErrYaw"].listData[self.msgid][1]
			msg.Pitch = self.channel["Pitch"].listData[self.msgid][1]
			msg.Roll = self.channel["Roll"].listData[self.msgid][1]
			msg.Yaw = self.channel["Yaw"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1
