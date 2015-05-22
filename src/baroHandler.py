

try:
	import rospy
	import rosbag
	from apmlog_tools.msg import BARO
except ImportError:
	print "Can't load ROS dependencies"


class BAROHandler:
	'''BARO channel handler'''
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

			msg = BARO()

			msg.header.seq = self.timestamp_ms[self.msgid][0]
			msg.header.stamp = self.stamp

			msg.Alt = self.channel["Alt"].listData[self.msgid][1]
			msg.CRt = self.channel["CRt"].listData[self.msgid][1]
			msg.Press = self.channel["Press"].listData[self.msgid][1]
			msg.Temp = self.channel["Temp"].listData[self.msgid][1]

			self.bag.write(self.topic, msg, msg.header.stamp)
			self.msgid = self.msgid + 1

