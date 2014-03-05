#!/usr/bin/env python
'''
Online Digitizer and Analyzer for
Project8: Towards measuring the mass of neutrino.
Author:Prajwal Mohanmurthy
       prajwal@mohanmurthy.com
       LNS MIT
'''

import corr,time,numpy,struct,sys,logging,pylab,matplotlib

bitstream = 'proj83.bof'
katcp_port=7147
roach = '198.125.161.179'
timeout = 10
fpga = corr.katcp_wrapper.FpgaClient(roach,katcp_port, timeout)

print 'Roach: Loading bof file\n'
fpga.progdev(bitstream)

print 'Roach: Seting{Accumulation Length:acc_len, Gain:gain}\n'
fpga.write_int('acc_len',2*(2**28)/2048) #record length
fpga.write_int('gain',0xffffffff) #1

print 'Roach: Resetting{Counter:cnt_rst}\n'
fpga.write_int('cnt_rst',1)
fpga.write_int('cnt_rst',0)

print 'Roach: Reading interleaved record'
acc_n = fpga.read_uint('acc_cnt')
a_0=struct.unpack('>1024l',fpga.read('one',1024*4,0))
a_1=struct.unpack('>1024l',fpga.read('two',1024*4,0))
a_2=struct.unpack('>1024l',fpga.read('three',1024*4,0))
a_3=struct.unpack('>1024l',fpga.read('four',1024*4,0))
interleave_a=[]
for i in range(1024):
	interleave_a.append(a_0[i])
	interleave_a.append(a_1[i])
	interleave_a.append(a_2[i])
	interleave_a.append(a_3[i])

print interleave_a

print 'Roach: Slow plotting using pylab'
pylab.figure(num=1,figsize=(10,10))
pylab.plot(interleave_a)
pylab.title('Integration number %i.'%acc_n)
pylab.ylabel('Power (arbitrary units)')
pylab.grid()
pylab.xlabel('Channel')
pylab.xlim(0,2048)
pylab.show()
