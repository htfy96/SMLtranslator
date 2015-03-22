#!/usr/bin/python3
#! -*- coding:utf8 -*-
# Author: L******
# StudentNumber: 514*******
# Class: F14*****
# Time: 2014/10/25 21:30:23
# Prog: Simple translator of assembly language designed 

from sys import argv

def tran(filename,targetname):

	global var
	global lab
	global base,entry
	global legalop
	legalop={"lm":"1","lb":"2","j":"B","and":"8","or":"7","xor":"9","rot":"A","halt":"C","addc":"5","addf":"6","mov":""}
	
	var,lab={},{}
	base,entry=0,0
	
	def legalreg(w):
		return 0<=w<8
		
	def legalmem(w):
		return 0<=w<256

	def delcomment(s):
		if s.find(";")!=-1:
			return s[:s.find(";")]
		return s
	
	def genelegal(s):
		for c in s:
			if not ("0"<=c<="9") and not ("a"<=c<="z") and not ("A"<=c<="Z") and not (c=='_'):
				raise ValueError("'{0}' is illegal".format(s))
		if s=="":
			return False
		return True
				
	def getlabel(s):
		if s.find(":")!=-1:
			w=delprespace(s[:s.find(":")])
			for c in w:
				if not ("0"<=c<="9") and not ("a"<=c<="z") and not ("A"<=c<="Z"):
					raise ValueError("in '{0}' , Label is illegal".format(w))
			return w
		return ""
	
	def delprespace(s):
		for i in range(len(s)):
			if s[i]!=" ":
				return s[i:]
		return ""
		
	def delpostspace(s):
		for i in range(len(s)-1,-1,-1):
			if s[i]!=" ":
				return s[:i+1]
		return ""
		
	def deledgespace(s):
		ss=delprespace(delpostspace(s))
		return ss
		
	def part(s):
		s2=delprespace(s)
		if s2.find(" ")==-1:
			return s2
		else:
			return(s2[:s2.find(" ")])
			
	def nextpart(s):
		if s.find(" ")==-1:
			return ""
		else:
			return part(s[s.find(" "):])
			
	def getbody(s):
		if s.find(":")==-1:
			return s
		else:
			return(delprespace(s[s.find(":")+1:]))
			
	def check(para,num,*typ):
		global var,lab
		if len(para)!=num:
			return False
		for i in range(num):
			if typ[i]=="reg":
				if not legalreg(int(para[i])) or len(para[i])!=1:
					return False
			elif typ[i]=="val":
				if  (para[i].lower() not in var) and (not legalmem(int(para[i],16)) or len(para[i])!=2) :
					return False
			elif typ[i]=="addr":
				if (para[i].lower() not in lab) and ( not legalmem(int(para[i],16)) or len(para[i])!=2):
					return False
		return True
			
	def checkpara(h,para):
		checkpara=True
		if h in ("lm","lb"):
			checkpara=checkpara and check(para,2,"reg","val")
		if h=="mov":
			checkpara=checkpara and (check(para,2,"reg","val") or check(para,2,"reg","reg"))
		if h in ("addc","addf","or","and","xor"):
			checkpara=checkpara and ((check(para,3,"reg","reg","reg") or check(para,2,"reg","reg")))
		if h=="rot":
			checkpara=checkpara and check(para,2,"reg","reg")
		if h=="j":
			checkpara=checkpara and (check(para,2,"reg","addr") or check(para,1,"addr"))
		if h=="halt":
			checkpara=checkpara and check(para,0)
				
	def var2num(s):
		global var
		if s in var:
			return var[s]
		else:
			return int(s,16)
			
	def lab2num(s):
		global lab
		if s in lab:
			return lab[s]
		else:
			return int(s,16)
	
	def process(ff,h,para):
		global legalop
		global var
		global label
		checkpara(h,para)
		if h!="mov":
			ff.write(legalop[h])
		else:
			if check(para,2,"reg","val"):
				ff.write("3")
			else:
				ff.write("4")

		if h in ("lm","lb"):
			ff.write("{0}{1:0>2x}".format(para[0],var2num(para[1])))
		if h=="mov":
			if check(para,2,"reg","val"):
				ff.write("{0}{1:0>2x}".format(para[0],var2num(para[1])))
			else:
				ff.write("{0}{1}".format(para[0],para[1]))
		if h in ("addc","addf","or","and","xor"):
			if check(para,2,"reg","reg"):
				ff.write("{0}{1}{2}".format(para[0],para[0],para[1]))
			else:
				ff.write("{0}{1}{2}".format(para[0],para[1],para[2]))
		if h=="rot":
			ff.write("{0}0{1}".format(para[0],para[1]))
		if h=="j":
			if check(para,1,"addr"):
				ff.write("0{0:0>2x}".format(lab2num(para[0])))
			else:
				ff.write("{0}{1:0>2x}".format(para[0],lab2num(para[1])))
		if h=="halt":
			ff.write("000")
		ff.write("\n")
	
	def scan1():
		global var
		global lab
		global base,entry
		f=open(filename,"r")
		raw=" ";
		datap=False
		codep=False
		while len(raw):
			raw=f.readline()
			s=delprespace(delcomment(raw)).replace("\n","")
			if s!="":
			#	print("'"+part(s).lower()+"'")
			#	print(len(nextpart(s)))
				if codep and s!="":
					now+=2
				if deledgespace(s).lower()==".data":
					if datap or codep or len(nextpart(s)):
						raise ValueError(".DATA Declaration Error in {0}".format(s))
					else:
						datap=True
				if deledgespace(s).lower()==".code":
					
					if codep or len(nextpart(s)):
						raise ValueError(".CODE Declaration Error in {0}".format(s))
					else:
						codep=True
						datap=False
						now=0
						print("ok")

				if part(deledgespace(s).lower())==".entry":
					if not codep:
						raise ValueError(".ENTRY Declaration Error in {0}".format(s))
					else:
						entry=int(nextpart(s),16)
						if not legalmem(entry):
							raise ValueError("illegal Entry {0} in {1}".format(entry,s))
			
				if part(deledgespace(s).lower())==".base":
					if not codep or base or now!=2:
						raise ValueError(".BASE Declaration Error in {0}".format(s))
					else:
						base=int(nextpart(s),16)		
						entry=base
						if not legalmem(base):
							raise ValueError("illegal base {0} in {1}".format(base,s))
						now=base-2
					
			
				if datap and deledgespace(s).lower()!=".data":
					if s.find(" ")==-1:
						return ValueError("Illegal data declaration in {}".format(s))
					first=part(s)
					if first in var or not genelegal(first) or first.isdigit():
						raise ValueError("{0} is declared twice or illegal in {1}".format(first,s))
					second=int(nextpart(s),16)
					if not legalmem(second):
						raise ValueError("Illegal address {0} in {1}".format(second,s))
					else:
						var[first.lower()]=second
					
				if codep and deledgespace(s).lower()!=".code" and deledgespace(s).lower()!=".entry" and deledgespace(s).lower()!=".base" and deledgespace(s).lower()!=".code":
				#	print(":::",s)
					if genelegal(getlabel(s).lower()):
						lab[getlabel(s).lower()]=now
				
		f.close()
	
	def scan2():
		global var
		global lab
		global base,entry
		global legalop
		f=open(filename,"r")
		raw=" ";
		ff=open(targetname,"w")
		codep=False
		while len(raw):
			raw=f.readline()
			s=delprespace(delcomment(raw)).replace("\n","")
			if s!="":
			#	print("'"+part(s).lower()+"'")
			#	print(len(nextpart(s)))
				if codep and s!="":
					now+=2
				if part(s).lower()==".code":
					if codep  or len(nextpart(s)):
						raise ValueError(".CODE Declaration Error in {0}".format(s))
					else:
						codep=True
						datap=False
						now=0
						print("ok")
				if part(s).lower()==".base":
				#	if not codep or base or now!=2:
				#		raise ValueError(".BASE Declaration Error in {0}".format(s))
				#	else:
				#		base=int(nextpart(s))		
				#		if not legalmem(base):
				#			raise ValueError("illegal base {0} in {1}".format(base,s))
						now=base-2
				
				if codep and part(s).lower()!=".code" and part(s).lower()!=".base" and part(s).lower()!=".entry":
					ss=getbody(s)
					h=part(ss).lower()
					if  h not in legalop:
						raise ValueError("Illegal operator {0} in {1}".format(part(ss),s))
					print("{0:<3x}".format(now),"|",ss)
					para=ss[ss.find(" ")+1:].split(",")
					for i in range(len(para)):
						para[i]=deledgespace(para[i]).lower()
					process(ff,h,para)
		ff.close()
		f.close()
		
	scan1() 
	print(lab)
	print(base)
	scan2()
	
	
def main():
	helps="Translator from SimpleBasic to machine language\n\
	Version 0.1	2014/10/25	L** *****\n\
---------------------------------------------------\n\
Usage:\n\
	translator inputfile outputfile"
	print(argv)
	if len(argv)==1:
		print(helps)
		
	if len(argv)!=3:
		print("there must be two parameters!")
		s1=input("Input source assembly file：")
		s2=input("Input output machine language file：")
		tran(s1,s2)
	else:
		tran(argv[1],argv[2])
		
if __name__=="__main__":
	main()
	
				
			
			
