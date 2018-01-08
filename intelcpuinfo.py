#!/usr/bin/env python

try:
    from prettytable import PrettyTable
except ImportError:
    textout = True
import sys

patched = {
    '000406F1': '0xb000025',
    '000306C3': '0x23',
    '000306F2': '0x3b',
    '00040661': '0x18',
    '00040651': '0x21',
    '000506E3': '0xc2',
    '00050653': '0x100013e',
    '00050654': '0x200003a',
    '000406E3': '0xc2',
    '00040671': '0x1b',
    '000306D4': '0x28',
    '000506F1': '0x20',
    '000906EA': '0x7c',
    '000906EB': '0x7c',
    '000806EA': '0x7c',
    '000906E9': '0x7c',
    '000806E9': '0x7c',
    '000506C9': '0x2e',
    '000506CA': '0x8',
    '000306E4': '0x42a',
    '000306F4': '0x10',
    '000706A1': '0x20',
    '00050662': '0x13',
    '00050663': '0x7000010',
    '00060663': 'TBD',
    '000406C3': 'TBD',
    '000606E1': 'TBD',
    '000306E7': '0x70F',
    '000206D7': '0x712',
    '000406D8': '0x129',
    '00050664': '0xF00000E',
    '00050665': '0xE000006',
    '00050671': '0x1B2',
    '00080650': '0x14',
    '000206A7': '0x2b',
    '000506C2': 'TBD',
    '0007065A': 'TBD',
    '00070658': 'TBD',
    '000406C4': 'TBD',
    '00030678': 'TBD',
    '000506A0': 'TBD',
    '000206D6': '0x61b',
    '000406A8': 'TBD',
    '000106A5': 'TBD',
    '000306A9': 'TBD',
    '000206F2': 'TBD',
    '00020655': 'TBD',
    '00020652': 'TBD',
    '000106E5': 'TBD',
    '00030679': 'TBD',
    '000206C2': 'TBD',
    '000106A4': 'TBD',
    '000406A9': 'TBD',
    '000206E6': 'TBD',
    '00030673': 'TBD',
    '000506D1': 'TBD',
    '000506D1': 'TBD',
    '000106E4': 'TBD',
    '000506A1': 'TBD',
    '000106D1': 'TBD',
    '00010676': 'TBD',
    '0001067A': 'TBD',
    '00010676': 'TBD',
    '00010676': 'TBD',
    '0001067A': 'TBD',
    '00070676': 'TBD',
    '00010677': 'TBD'
}


cpudict = {}

with open('/proc/cpuinfo', 'r') as f:
   cpulist = f.read()
   cpuinfo = set(cpulist.splitlines())
   for line in cpuinfo:
       if ('family' in line or 'model' in line or 'stepping' in line or
           'microcode' in line):
           k,v = line.replace('\t', '').split(':')
           cpudict[k.strip()] = v.strip()

hexmodel = hex(int(cpudict['model']))[2:]
cpufamily = ("000{}0{}{}{}" .format(hexmodel[0], cpudict['cpu family'],
             hexmodel[1], cpudict['stepping'])).upper()

if textout:
    print "CPU Model Name:             {}" .format(cpudict['model name'])
    print "CPUID:                      {}" .format(cpufamily)
    print "Current Microcode Version:  {}" .format(cpudict['microcode'])
    print "Patched Microcode Version:  {}" .format(patched[cpufamily])
else:
    table = PrettyTable(["CPU Model Name", "CPUID", "Current Microcode Version", "Patched Microcode Version"])
    table.add_row([cpudict['model name'], cpufamily, cpudict['microcode'], patched[cpufamily]])

    print table

if cpudict['microcode'] == patched[cpufamily]:
    sys.exit(0)
else:
    sys.exit(1)
