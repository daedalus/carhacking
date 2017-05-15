#!/usr/bin/python

class SFFMessage:
	def __init__(self, line):

		self.wid = 0x0000
		self.line = line
		#break out the pieces
		pieces = line.split(',')

		if(len(pieces) > 3):
			self.idh = pieces[0].split(':')[1].strip()
			self.idl = pieces[1].split(':')[1].strip()
			self.wid = self.idh + self.idl
			self.len = int(pieces[2].split(':')[1].strip(),16)
			self.data = pieces[3].split(':')[1].strip()

			self.data_pieces = self.data.split(' ')
			if len(self.data_pieces) != self.len:
				print "ERROR - COULDN'T SPLIT DATA"
				print line
				print self.data


def	check_for_msg(msg, print_repeats, verbosity):
	global lines
	if msg.wid in lines.keys():
#		print "existing..."
		entry = lines[msg.wid]
		if entry['len'] != msg.len:
			print "Packet with unexpected length found!"
			print msg.line
			if not print_repeats:
				add_msg_to_data(msg)
		for x in range(msg.len):
			#seen this byte before
			if msg.data_pieces[x] not in entry[x].keys():
				if verbosity > 0:
					print "FOUND DIFFERING BYTE, SLOT %d" % x
					print entry[x].keys()
					print msg.data_pieces[x]
					print msg.line
				if verbosity == 0:
					print msg.wid
				if not print_repeats:
					add_msg_to_data(msg)
	else:
		print "NEW MSG TYPE " + msg.wid


def add_msg_to_data(msg):
	global lines
	if msg.wid in lines.keys():
#		print "existing, add to it"
		entry = lines[msg.wid]
		if entry['len'] != msg.len:
			print "Packet with lengths that don't match found!"
		for x in range(msg.len):
			#seen this byte before
			if msg.data_pieces[x] in entry[x].keys():
				entry[x][msg.data_pieces[x]] = entry[x][msg.data_pieces[x]] + 1
			# its a new byte
			else:
				entry[x][msg.data_pieces[x]] = 1
	else:
#		print "new one, add it"
		entry = {'len':msg.len}
		for x in range(msg.len):
			entry[x] = {msg.data_pieces[x]:1}
	lines[msg.wid] = entry


def get_data(filename):
	fp = open(filename, "r")
	for line in fp:
		msg = SFFMessage(line)
		if(msg.wid != 0):
			add_msg_to_data(msg)
		
def look_for_different_data(filename, print_repeats, verbosity):
	fp = open(filename, "r")
	for line in fp:
		msg = SFFMessage(line)
		if(msg.wid != 0):
			check_for_msg(msg, print_repeats, verbosity)
		
lines = {}		
#get_data("idle.dat")
get_data("idle_s.dat")
look_for_different_data("unlock_nofob_s.dat", False, 1)
#print lines
