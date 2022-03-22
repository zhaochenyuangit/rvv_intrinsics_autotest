import os 
import re
import datetime
from random import randint, random
import readline
from time import sleep

DOC_PATH = os.path.join('..','rvv-intrinsic-doc-master','intrinsic_funcs')
VLEN = 128

def random_line():
    md_files = os.listdir(DOC_PATH)
    filename = [f for f in md_files if f.startswith("05")][0]
    filename = os.path.join(DOC_PATH,filename)
    filesize = os.stat(filename).st_size
    with open(filename,'r') as f:
        ret = ""
        while not re.findall(';\s+$',ret):
            file_pointer = randint(0,filesize)
            f.seek(file_pointer)
            f.readline()
            ret =  f.readline()
        return ret
    
def parse_declaration(line):
    ret, func, rest_of_line = line.split(" ", 2)
    match = re.search('(?P<ops>(?<=\().+(?=\)))',rest_of_line)
    op_pairs = match.group('ops').split(',')
    op_pairs = [op.split() for op in op_pairs]
    operands = {arg:dtype for dtype,arg in op_pairs}
    return {'ret':ret,'func':func,'ops':operands}    

def parse_vector_type(vec_t:str):
    size_dict = {'mf8':1/8,'mf4':1/4,'mf2':1/2,'m1':1,'m2':2,'m4':4,'m8':8,}
    if 'bool' in vec_t:
        return vec_t
    match = re.search('(?P<basetype>(u?int\d+)|(float\d+))(?P<lmul>mf?\d)',vec_t)
    reg_size = size_dict.get(match.group('lmul'))*VLEN
    basetype = match.group('basetype')
    basesize = re.search('(?P<size>\d+)',basetype).group('size')
    vlmax = int(reg_size)//int(basesize)
    return (match.group('basetype')+'_t',vlmax)

def main():
   line = random_line()
   print(line)
   #line = 'vint16m2_t vmin_vv_i16m1_tu (vint16mf8_t dest, vint16m1_t op1, vint16m1_t op2, size_t vl);'
   ret, func, rest_of_line = line.split(" ", 2)
   operands = re.findall('\w+_t',rest_of_line)
   v_operands = set([op for op in operands if op.startswith('v')])
   v_parse_rules = map(parse_vector_type,v_operands)
   v_parse_dict = dict(zip(v_operands,v_parse_rules))
   print(v_parse_dict)

        

if __name__=='__main__':
    main()