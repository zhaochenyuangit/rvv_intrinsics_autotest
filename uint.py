import re

#match = re.search('(?P<basetype>(u?int\d+)|(float\d+))(?P<lmul>mf?\d)','vuint16m1_t')
#print(match.group('basetype'),match.group('lmul'))
basesize = re.search('(?P<size>\d+)','int16')
