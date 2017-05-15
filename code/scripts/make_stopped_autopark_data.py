#!/usr/bin/python

def print_81_line(pos, ts):
	out = 'IDH: 00, IDL: 81, Len: 08, Data: '
	out += '%02X' % (pos >> 8) 
	out += ' '
	out += '%02X' % (pos & 0xff)
	out += ' 12 00 00 00 00 00 ,TS: '
	out += '%d' % ts
	out += ',BAUD: 1'
	print out

num_times = 120 # 60
diffs=[-10,-16,-24,-30,-40,-46,-54,-60,-70,-76,-84,-94,-100,-108,-114,-122,-130,-138,-146,-152,-160,-168,-176,-184,-192,-194]
end_diff = -194
start = 0x4E6B 
ts_diff = 312

newposition = start
timestamp = 0
for diff in diffs:
	print_81_line(newposition,timestamp)
	newposition += diff
	timestamp += ts_diff
for x in range(num_times):
	print_81_line(newposition,timestamp)
	newposition += end_diff
	timestamp += ts_diff

