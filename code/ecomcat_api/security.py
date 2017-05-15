

#install_pcm
#seed = "45 82 0A"
#real_key = "3B 15 E1"

#install_pcm_again
#seed = "36 F0 F7"
#real_key = "C9 4E C9"

#sjb
seed = "7A 6B 61"
real_key = "96 11 73"

print "Observed seed: "+seed
#
# This is the "secret" found in debugger for PCM
#
#s1 = 0x08
#s2 = 0x30
#s3 = 0x61
#s4 = 0xa4
#s5 = 0xc5

#
# for SJB
# 
s1 = 0x3f
s2 = 0x9e
s3 = 0x78
s4 = 0xc5
s5 = 0x96

seed_int = (int(seed[0:2],16)<<16) + (int(seed[3:5],16)<<8) + (int(seed[6:8],16)) 
#print "Seed: %x" % seed_int

or_ed_seed = ((seed_int & 0xFF0000) >> 16) | (seed_int & 0xFF00) | (s1 << 24) | (seed_int & 0xff) << 16
#print "or_ed_seed: %x\n" % or_ed_seed

mucked_value = 0xc541a9

for i in range(0,32):
	a_bit = ((or_ed_seed >> i) & 1 ^ mucked_value & 1) << 23
	v9 = v10 = v8 = a_bit | (mucked_value >> 1);
	mucked_value = v10 & 0xEF6FD7 | ((((v9 & 0x100000) >> 20) ^ ((v8 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v8 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v8 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v8 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v8 & 0x800000) >> 23));
#	print "mucked: %x" % (mucked_value)

for j in range(0,32):
	v11 = ((((s5 << 24) | (s4 << 16) | s2 | (s3 << 8)) >> j) & 1 ^ mucked_value & 1) << 23;
	v12 = v11 | (mucked_value >> 1);
	v13 = v11 | (mucked_value >> 1);
	v14 = v11 | (mucked_value >> 1);
	mucked_value = v14 & 0xEF6FD7 | ((((v13 & 0x100000) >> 20) ^ ((v12 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v12 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v12 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v12 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v12 & 0x800000) >> 23));

key = ((mucked_value & 0xF0000) >> 16) | 16 * (mucked_value & 0xF) | ((((mucked_value & 0xF00000) >> 20) | ((mucked_value & 0xF000) >> 8)) << 8) | ((mucked_value & 0xFF0) >> 4 << 16);

print "Computed key: %x" % key
print "observed key: " + real_key
