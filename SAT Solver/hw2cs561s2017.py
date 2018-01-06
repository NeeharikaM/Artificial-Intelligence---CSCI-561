import copy as cp
import random
import sys

f = open('input.txt','r')
p=f.readline().strip()
#print p
guests1=p.split(' ')[0]
tables1=p.split(' ')[1]
guests=int(guests1)
tables=int(tables1)
conditions = []
conditions =  f.read().strip()
conditions = list(conditions)
conditions = [x for x in conditions if x != ' ' and x != '\n' and x != '\r']

relations = [[0 for i in range(guests)] for j in range(guests)]
i=2
while i <= len(conditions)-1:
	if conditions[i]=='F':
		relations[int(conditions[i-1])-1][int(conditions[i-2])-1]=1
	if conditions[i]=='E':
		relations[int(conditions[i-1])-1][int(conditions[i-2])-1]=-1
	i=i+3
f.close()
#print relations

def CNF(guests,tables,relations):
	CNF = []
	for i in range (0,len(relations)):
		for j in range(0,len(relations)):
			if relations[i][j]==-1: #2,1
				for k in range(0,tables):
					CNF.append([['~x',str(i+1),str(k+1)],['~x',str(j+1),str(k+1)]])
			elif relations[i][j]==1: #1,0
				for r in range(0,tables): #0
					for s in range(0,tables): #0
						if r!=s:
							CNF.append([['~x',str(j+1),str(r+1)],['~x',str(i+1),str(s+1)]])
			else:
				pass
	if tables!=1:
		for h in range(0,guests):  #0,1,2,3,4 #implementation of first rule
			onetab = []
			for t in range(0,tables): #0
				onetab.append(['~x',str(h+1),str(t+1)]) #(~x,1,1),(~x,1,2)
			CNF.append(onetab)
		for b in range(0,guests): #implementation of second rule
			twotab = []
			for c in range(0,tables):
				twotab.append(['x',str(b+1),str(c+1)])
			CNF.append(twotab)
	return CNF

def CNFString(guests,tables,relations):
	CNF = []
	for i in range (0,len(relations)):
		for j in range(0,len(relations)):
			if relations[i][j]==-1: #2,1
				for k in range(0,tables):
					CNF.append(['~x'+str(i+1)+','+str(k+1),'~x'+str(j+1)+','+str(k+1)])
			elif relations[i][j]==1: #1,0
				if tables>1:
					for r in range(0,tables): #0
						for s in range(0,tables): #0
							if r!=s:
								CNF.append(['~x'+str(j+1)+','+str(r+1),'~x'+str(i+1)+','+str(s+1)])
				else:
					pass
	for h in range(0,guests):  #0,1,2,3 #implementation of first rule
		onetab = []
		if tables>1:
			for t in range(0,tables): #0
				onetab.append('~x'+str(h+1)+','+str(t+1)) #(~x,1,1),(~x,1,2)
			CNF.append(onetab)
	for b in range(0,guests): #implementation of second rule
		twotab = []
		for c in range(0,tables):
			twotab.append('x'+str(b+1)+','+str(c+1))
		CNF.append(twotab)
	return CNF
		
CNFlist = CNFString(guests,tables,relations)
	

def DPLL_SATISFIABLE(CNFlist):
	#print CNFlist
	if tables==0 or guests==0:
		return False
	symbols = []
	for i in range(0,len(CNFlist)):
		for x in CNFlist[i]:
			if x not in symbols and x[0]!='~':
				symbols.append(x)
	#print CNFlist
	#print symbols
	return DPLL(CNFlist,symbols,{})
	#return DPLL(CNFlist,symbols,{})
	

def DPLL(clauses,symbols,model):
	#print "model"
	#print model
	#print "symbols"
	#print symbols
	unknown_clause= []
	for c in clauses:
		b=CheckBooleanValue(c,model)
		if b==False:
			return False
		elif b!=True:
			unknown_clause.append(c)
	#print "unknown clause"
	#print unknown_clause
	if unknown_clause==[]:
		return True
	PS,value=FindPureSymbol(symbols,unknown_clause)
	#print PS,value
	if PS:
		return DPLL(clauses,remove_sym(symbols,PS),adddict(model,PS,value))
	UC,UCValue=FindUnitClause(unknown_clause,model)
	#print UC,UCValue
	if UC:
		return DPLL(clauses,remove_sym(symbols,UC),adddict(model,UC,UCValue))
	R=symbols.pop()
	#print "popped symbol"
	#print R
	return (DPLL(clauses,symbols,adddict(model,R,True)) or
			DPLL(clauses,symbols,adddict(model,R,False)))
	
def FindUnitClause(clauses,model):
	for c in clauses:
		counter=0
		for x in c:
			if x[0]=='~':
				position=x.index(',')
				a=x[2:position]
				b=x[position+1:]
				temp=x[1]+a+','+b
				value1=temp
				bool1=False
			else:
				value1=x
				bool1=True
			if value1 not in model:
				value,bool=value1,bool1
				counter=counter+1
		if counter==1:
			#print "hi"
			#print value,bool
			return value,bool
	return None,None

def remove_sym(symbols,lit):
	temp = []
	for i in range(0,len(symbols)):
		if symbols[i]!=lit:
			temp.append(symbols[i])
	return temp
	
def adddict(model,PS,value):
	tempdict=cp.deepcopy(model)
	tempdict[PS]=value
	return tempdict

def CheckBooleanValue(clause,model={}): #x11V~x21
	#print clause
	#print model
	falsecounter=0
	for i in range(0,len(clause)):
		if model.get(clause[i])==True:
			return True
		elif model.get(clause[i])==False:
			falsecounter=falsecounter+1
		elif clause[i][0]=='~':
			position=clause[i].index(',')
			a=clause[i][2:position]
			b=clause[i][position+1:]
			temp='x'+a+','+b
			if temp in model:
				if model.get(temp)==False:
					return True
				elif model.get(temp)==True:
					falsecounter=falsecounter+1	
	if falsecounter==len(clause):
		return False
	else:
		return None
	
def FindPureSymbol(symbols,unknown_clause):
	found_negative=0
	found_positive=0
	for s in symbols:
		for c in unknown_clause:
			if '~'+s in c:
				found_negative=found_negative+1
			if s in c:
				found_positive=found_positive+1
		if found_negative>0 and found_positive>0:
			return None,None
		elif found_negative==0 and found_positive>0:
			return s,True
		elif found_negative>0 and found_positive==0:
			return s,False
		else:
			return None,None

CNFlist1 = CNF(guests,tables,relations)
CNFlist2 = CNF(guests,tables,relations)

def WalkSAT(clauses,p,max_flips):
	count=0
	#print CNFlist1
	onetabarr = []
	if len(clauses)==0 and tables==1:
		for i in range(1,guests+1):
			onetabarr.append(str(i)+' '+'1')
		return onetabarr
	else:
		model=RandomAssignment(clauses)
		#print model
		for i in range(1,max_flips):
			falseindexes=satisfy(model)
			#print falseindexes
			if falseindexes== []:
				count=count+1
				return finalarrangement(model,count)
				#print CNFlist2
			else:
				flipped=flip(model,falseindexes)
			#print flipped

def finalarrangement(model,count):
	if count==1:
		truecases = []
		output = []
		final = [] 
		temp = []
		finalarrange = []
		for i in range(0,len(model)):
			for j in range(0,len(model[i])):
				if model[i][j]=='True' and model[i][j] not in truecases:
					truecases.append(CNFlist1[i][j])
				else:
					pass
		#print truecases
		for i in range(0,len(truecases)):
			if truecases[i][0]=='x':
				output.append(truecases[i])
		output.sort(key=lambda x: x[1])
		#print output
		for i in range(0,guests):
			temp= [] #0,1,2...12
			for j in range(0,len(output)):
				if int(output[j][1])==i+1: 
					temp.append(output[j])
					#print temp
					randarr=temp[0]
			final.append(randarr)
		for i in range(0,len(final)):
			finalarrange.append(final[i][1]+' '+final[i][2])
		return finalarrange
	else:
		pass
	

def flip(model,falseindexes):
	modelexp=cp.deepcopy(model)
	indx=random.choice(falseindexes)
	#print indx
	indices = []
	for i in range(0,len(model[indx])):
		if model[indx][i]=='False':
			indices.append(i)
	#print indices
	if random.uniform(0,1)<p:
		#print "hi"
		randlit=random.choice(indices)
		variable=CNFlist2[indx][randlit][0]
		person=CNFlist2[indx][randlit][1]
		table=CNFlist2[indx][randlit][2]
		model[indx][randlit]='True'
		for i in range(0,len(CNFlist2)): #0,1,2...12
			for j in range(0,len(CNFlist2[i])):#0,1
				if CNFlist2[i][j][1]==person:
					if CNFlist2[i][j][2]==table:
						if CNFlist2[i][j][0]==variable:
							#print model[i][j]
							#print model[indx][randlit]
							model[i][j]=model[indx][randlit]
						else:
							if model[indx][randlit]=='True':
								model[i][j]='False'
							else:
								model[i][j]='True'
					else:
						pass
				else:
					pass
		return model
	else:
		#print "hey"
		index=FindMaximumSatisfiabilityIndex(indx,indices,model)
		#print index
		variable=CNFlist2[indx][index][0]
		person=CNFlist2[indx][index][1]
		table=CNFlist2[indx][index][2]
		model[indx][index]='True'
		for i in range(0,len(CNFlist2)): #0,1,2...12
			for j in range(0,len(CNFlist2[i])):#0,1
				if CNFlist2[i][j][1]==person:
					if CNFlist2[i][j][2]==table:
						if CNFlist2[i][j][0]==variable:
							#print model[i][j]
							#print model[indx][randlit]
							model[i][j]=model[indx][index]
						else:
							if model[indx][index]=='True':
								model[i][j]='False'
							else:
								model[i][j]='True'
					else:
						pass
				else:
					pass
		return model
		
			
def FindMaximumSatisfiabilityIndex(indx,indices,modelexp):
	counter=1000000000
	index=0
	for i in range(0,len(indices)):
		#print 'i='+str(i)
		selectedindx=indices[i]
		variable=CNFlist2[indx][selectedindx][0]
		person=CNFlist2[indx][selectedindx][1]
		table=CNFlist2[indx][selectedindx][2]
		modelexp[indx][selectedindx]='True'
		for i in range(0,len(CNFlist2)): #0,1,2...12
			for j in range(0,len(CNFlist2[i])):#0,1
				if CNFlist2[i][j][1]==person:
					if CNFlist2[i][j][2]==table:
						if CNFlist2[i][j][0]==variable:
							#print modelexp[i][j]
							#print modelexp[indx][randlit]
							modelexp[i][j]=modelexp[indx][selectedindx]
						else:
							if modelexp[indx][selectedindx]=='True':
								modelexp[i][j]='False'
							else:
								modelexp[i][j]='True'
					else:
						pass
				else:
					pass
		#print modelexp
		#print i
		count=0
		notsatisfiedcounter=0
		for g in range(0,len(modelexp)): #0,1,2,3,4...11
			count=0
			for h in range(0,len(modelexp[g])): #0,1
				if modelexp[g][h]=='False':
					count=count+1
					#print count
					if count==len(modelexp[g]):
						notsatisfiedcounter=notsatisfiedcounter+1
				else:
					pass
		#print notsatisfiedcounter
		#print i
		#print "hjh"
		if notsatisfiedcounter<counter:
			counter=notsatisfiedcounter
			#print "counter="+str(counter)
			index=selectedindx
			#print "index="+str(index)
		else:
			pass
	return index		
			
			
	
def RandomAssignment(CNFlist):
	symbols= []
	CNFlist1=cp.deepcopy(CNFlist)
	for i in range(0,len(CNFlist)):
		for x in CNFlist[i]:
			if x not in symbols:
				symbols.append(x)
	#print symbols
	booleansym=cp.deepcopy(symbols)
	for x in range(0,len(booleansym)):
		booleansym[x]=random.choice(['True','False'])
	
	for h in range(0,len(symbols)): #0
		for j in range(h+1,len(symbols)):
			if symbols[h][1]==symbols[j][1]:
				if symbols[h][2]==symbols[j][2]:
					if symbols[h][0]!=symbols[j][0]:
						if booleansym[h]=='True':
							booleansym[j]='False'
						else:
							booleansym[j]='True'
					else:
						pass
				else:
					pass
			else:
				pass
	#print booleansym
	for y in range(0,len(symbols)):
		for z in range(0,len(CNFlist1)):
			for d in range(0,len(CNFlist[z])):
				if symbols[y]==CNFlist1[z][d]:
					CNFlist1[z][d]=booleansym[y]
				else:
					pass
	return CNFlist1		

def satisfy(model):
	falseindexes = []
	count=0
	for i in range(0,len(model)): #0,1,2,3,4...11
		count=0
		for j in range(0,len(model[i])): #0,1
			if model[i][j]=='False':
				count=count+1
				#print count
				if count==len(model[i]):
					falseindexes.append(i)
			else:
				pass
	return falseindexes

g = open("output.txt", 'w')
sys.stdout = g
if DPLL_SATISFIABLE(CNFlist)==True:
	print "yes"
	p=0.5
	max_flips=10000
	arrangement =[]
	arrangement=WalkSAT(CNFlist1,p,max_flips)
	for i in range(0,len(arrangement)):
		print arrangement[i]
else:
	print "no"
g.close()
#res=PL_Resolution()					
#if __name__ == "__main__": main()
		
	
