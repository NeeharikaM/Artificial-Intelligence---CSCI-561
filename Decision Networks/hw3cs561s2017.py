import copy as cp
import re
import collections
import itertools
from operator import itemgetter
import sys
	
f = open("input.txt", "r")
g = open("output.txt", 'w')
sys.stdout = g
question = []
queries = []
utility = []
utilitydict = {}
decisionnodes = []
dectables = {}
tables = {}
r = []
finaloutput = []
firstindex=0
for line in f:
		question.append(line.strip())
question1=cp.deepcopy(question)
#making query list
for i in range(len(question)):
	question1.remove(question[i])
	if question[i]=='******':
		firstindex=i
		break
	else:
		queries.append(question[i])
#print queries
#making utility
for i in range(firstindex+1,len(question)):
	if question[i]!='******':
		continue
	elif question[i]=='******':
		question1.remove(question[i])
		for j in range(i+1,len(question)):
			utility.append(question[j])
			question1.remove(question[j])
#making utility dictionary
#utilitydict[utility[0].split('|')[0].replace(" ","")]=utility[0].split('|')[1].replace(" ","")
#for i in range(1,len(utility)):
	#utilitydict[utility[i][utility[i].index(' ')+1:]]=utility[i][:utility[i].index(' ')]
for j in range(1,len(utility)):
	str=tuple(utility[j][utility[j].index(' ')+1:].replace(" ",""))
	str=tuple(True if x=='+' else False for x in str)
	utilitydict[str]=utility[j][:utility[j].index(' ')]
#print 'utildict'
#print utilitydict
#print 'utildict'
#print utilitydict['+ -']
	
	
#making a list of decision nodes
for u in range(len(question1)):
	if question1[u]=='decision':
		decisionnodes.append(question1[u-1])
#print 'vvvvvvvv'
#print decisionnodes
		
#making bayesnet for decision networks
for i in range(len(question1)):
	if len(question1[i])==1 and question1[i+1]=='decision':
		continue
	elif len(question1[i])==1 and question1[i][0]!='0':
		dectables[question1[i]]={}
		dectables[question1[i]]['parents']=[]
		dectables[question1[i]]['children']=[]
		dectables[question1[i]]['prob']=float(question1[i+1])
		dectables[question1[i]]['condprobs']={}
	elif len(question1[i])>1 and question1[i][0]!='0' and question1[i][0]!='1' and question1[i]!='***' and question1[i]!='decision' and question1[i]!='utility' :
		strlnind=question1[i].index('|')
		dectables[question1[i][:strlnind].replace(" ","")]={}
		dectables[question1[i][:strlnind].replace(" ","")]['parents']=question1[i][strlnind+2:].replace(" ",",").split(",")
		dectables[question1[i][:strlnind].replace(" ","")]['children']=[]
		parents = question1[i][strlnind+2:].replace(" ",",").split(",")
		for p in range(len(parents)):
			if parents[p] in decisionnodes:
				continue
			else:
				dectables[parents[p]]['children'].append(question1[i][:strlnind].replace(" ",""))
		dectables[question1[i][:strlnind].replace(" ","")]['prob']= -1
		dectables[question1[i][:strlnind].replace(" ","")]['condprobs']={}
		for j in range(i+1,len(question1)):
			if question1[j]!='***':
				str=question1[j].replace(" ",",")[4:]
				str=tuple(str.replace(",",""))
				str=tuple(True if x=='+' else False for x in str)
				if question1[j].replace(" ",",")[3]==',':
					dectables[question1[i][:strlnind].replace(" ","")]['condprobs'][str]=float(question1[j].replace(" ",",")[:3])
				elif question1[j].replace(" ",",")[3]!=',':
					dectables[question1[i][:strlnind].replace(" ","")]['condprobs'][str]=float(question1[j].replace(" ",",")[:4])
			elif question1[j]=='***':
				break

#making bayesnet for probabilities
for i in range(len(question1)):
	#print "question"
	#print question1
	if len(question1[i])==1 and question1[i+1]=='decision':
		#print "dec node present"
		tables[question1[i]]={}
		tables[question1[i]]['parents']=[]
		tables[question1[i]]['children']=[]
		tables[question1[i]]['prob']= -2
		tables[question1[i]]['condprobs']={}
	elif len(question1[i])==1 and question1[i][0]!='0':
		tables[question1[i]]={}
		tables[question1[i]]['parents']=[]
		tables[question1[i]]['children']=[]
		tables[question1[i]]['prob']=float(question1[i+1])
		tables[question1[i]]['condprobs']={}
	elif len(question1[i])>1 and question1[i][0]!='0' and question1[i][0]!='1' and question1[i]!='***' and question1[i]!='decision' and question1[i]!='utility' :
		#print question1[i]
		strlnind=question1[i].index('|')
		#print strlnind
		tables[question1[i][:strlnind].replace(" ","")]={}
		tables[question1[i][:strlnind].replace(" ","")]['parents']=question1[i][strlnind+2:].replace(" ",",").split(",")
		tables[question1[i][:strlnind].replace(" ","")]['children']=[]
		parents = question1[i][strlnind+2:].replace(" ",",").split(",")
		for p in range(len(parents)):
			tables[parents[p]]['children'].append(question1[i][:strlnind].replace(" ",""))
		tables[question1[i][:strlnind].replace(" ","")]['prob']= -1
		tables[question1[i][:strlnind].replace(" ","")]['condprobs']={}
		for j in range(i+1,len(question1)):
			if question1[j]!='***':
				str=question1[j].replace(" ",",")[4:]
				str=tuple(str.replace(",",""))
				str=tuple(True if x=='+' else False for x in str)
				if question1[j].replace(" ",",")[3]==',':
					tables[question1[i][:strlnind].replace(" ","")]['condprobs'][str]=float(question1[j].replace(" ",",")[:3])
				elif question1[j].replace(" ",",")[3]!=',':
					tables[question1[i][:strlnind].replace(" ","")]['condprobs'][str]=float(question1[j].replace(" ",",")[:4])
			elif question1[j]=='***':
				break
	#print tables
#print queries
#print question1			
#print question1[3][:1]		
#print utility
#print dectables
#print "heeeee"
#print tables
#print utility

def makee(queries):
	#print type(queries)
	e = collections.OrderedDict()
	str2=''
	if '|' in queries:
		r = list(queries[queries.find("|")+1:queries.find(")")].replace(" ","").replace("=","").replace(",",""))
		for j in range(len(r)):
			str2=str2+r[j]
		for i in range(len(str2)):
			if bool(re.match(r'[A-Z]+$', str2[i])):
				if str2[i+1]=='+':
					e[str2[i]]=True
				else:
					e[str2[i]]=False
			else:
				continue
		return e
	else:
		return e

def makex(queries):
	g=list(queries[queries.find("(")+1:queries.find("|")].replace(" ","").replace("=","").replace(",",""))
	#print g
	str1=''
	X = collections.OrderedDict()
	for j in range(len(g)):
		str1=str1+g[j]
	#print str1
	for i in range(len(str1)):
		if bool(re.match(r'[A-Z]+$', str1[i])):
			if str1[i+1]=='+':
				X[str1[i]]=True
			else:
				X[str1[i]]=False
		else:
			continue
	return X

def mergedicts(queries): #for merging queries and evidence
	e = collections.OrderedDict()
	str2=''
	g=list(queries[queries.find("(")+1:queries.find("|")].replace(" ","").replace("=","").replace(",",""))
	#print g
	str1=''
	for j in range(len(g)):
		str1=str1+g[j]
	#print str1
	for i in range(len(str1)):
		if bool(re.match(r'[A-Z]+$', str1[i])):
			if str1[i+1]=='+':
				e[str1[i]]=True
			else:
				e[str1[i]]=False
		else:
			continue
	if '|' in queries:
		r = list(queries[queries.find("|")+1:queries.find(")")].replace(" ","").replace("=","").replace(",",""))
		for j in range(len(r)):
			str2=str2+r[j]
		for i in range(len(str2)):
			if bool(re.match(r'[A-Z]+$', str2[i])):
				if str2[i+1]=='+':
					e[str2[i]]=True
				else:
					e[str2[i]]=False
			else:
				continue
	return e

def topologicalsort(tables): #sorting bayes net nodes so that parent comes before child
	#print tables
	keyslist = list(tables.keys())
	#print keyslist
	keyslist.sort()
	#print keyslist
	s=set()
	#print s
	sortedlist = []
	while len(s)<len(keyslist):
		for x in keyslist:
			if x not in s and all(y in s for y in tables[x]['parents']):
				#print "hi"
				s.add(x)
				#print s
				sortedlist.append(x)
	return sortedlist

toposorted = topologicalsort(tables)
#print toposorted

def calcgivenprobs(Y,e): # A , {'A': False, 'C': 'True'}
	#print Y
	#print e
	if tables[Y]['prob'] != -1:
		prob = tables[Y]['prob'] if e[Y] else 1 - tables[Y]['prob']
	else:
		parents = tuple(e[par] for par in tables[Y]['parents'])
		prob = tables[Y]['condprobs'][parents] if e[Y] else 1 - tables[Y]['condprobs'][parents]
	#print "hello"
	#print float(prob)
	#print "heyyyyyyyyyyyyyyyyyyyy"
	return float(prob)

def normalize(Q):
	#print tuple(x * 1/(sum(Q)) for x in Q)
	return tuple(x * 1/(sum(Q)) for x in Q)

def pointwise_product(f1,f2):
	newvars = []
	newtab = {}
	h = {}
	#key = ()
	#print f1[0]
	#print f2[0]
	for y in range(len(f1[0])):
		newvars.append(f1[0][y])
	for z in range(len(f2[0])):
		newvars.append(f2[0][z])
	newvars = list(set(newvars))
	newvars.sort()
	#print newvars
	combinations = list(itertools.product([True,False],repeat=len(newvars)))
	#print combinations
	for comb in combinations:
		#print "hjjjjjjjjjjjjj"
		#print newvars
		#print comb
		newpairs = []
		for g in range(len(newvars)):
			newpairs.append(newvars[g])
			newpairs.append(comb[g])
		#print newpairs
		tuplelist = [(newpairs[i],newpairs[i+1]) for i in xrange(0,len(newpairs),2)]
		for eachpair in tuplelist:
			h[eachpair[0]] = eachpair[1]
		key = tuple(h[v] for v in newvars)
		#for v in newvars:
			#key.append(tuple(h[v]))
		key1 = tuple(h[v] for v in f1[0])
		key2 = tuple(h[v] for v in f2[0])
		prob = f1[1][key1]*f2[1][key2]
		newtab[key] = prob
	return (newvars,newtab)

def makefactor(v,facvars,e):
	possibleentries = {}
	j = {}
	vars = facvars[v]
	vars.sort() 
	everyvar = cp.deepcopy(tables[v]['parents'])
	everyvar.append(v)
	combinations = list(itertools.product([True,False],repeat=len(everyvar)))
	for combination in combinations:
		flag = False
		for pair in zip(everyvar,combination):
			if pair[0] in e and e[pair[0]]!=pair[1]:
				flag =True
				break
			j[pair[0]]=pair[1]
		if flag:	
			continue
		key = tuple(j[v] for v in vars)
		prob = calcgivenprobs(v,j)
		possibleentries[key] = prob
	return (vars,possibleentries)

def sumout(var,factors):
	havingvar = [] 
	indices = []
	newinds = []
	for i,factor in enumerate(factors):
		if var in factor[0]:
			havingvar.append(factor)
			indices.append(i)
	if len(havingvar) > 1:
		#indlen=len(indices)
		#for d in range(indlen,0,-1):
			#newinds.append(indices[d])
		for i in indices[::-1]:
			del factors[i]
		result = havingvar[0]
		for factor in havingvar[1:]:
			result = pointwise_product(result,factor)
		factors.append(result)
	for i, factor in enumerate(factors):
		for j, v in enumerate(factor[0]):
			if v == var:
				newvariables = factor[0][:j] + factor[0][j+1:]
				new = {}
				for thing in factor[1]:
					thing = list(thing)
					newkey = tuple(thing[:j] + thing[j+1:])
					thing[j] = True
					prob1 = factor[1][tuple(thing)]
					thing[j] = False
					prob2 = factor[1][tuple(thing)]
					prob = prob1 + prob2                       
					new[newkey] = prob
				factors[i] = (newvariables,new)
				if len(newvariables) == 0:
					del factors[i]
	return factors

def elimination_ask(X,e,type):
	#print "hgg"
	#print X.items()[0][1]
	#print e
	elimset = set()
	factors = []
	while len(elimset) < len(tables):
		rand = []
		#print "hkjlk"
		#print list(tables.keys())
		#print elimset
		for g in range(len(list(tables.keys()))):
			if list(tables.keys())[g] not in elimset:
				rand.append(list(tables.keys())[g])
		#print "rand"
		#print rand
		#for g in range(len(list(tables.keys()))):
			#if list(tables.keys())[g] not in elimset:
				#variables.append(list(tables.keys())[g])
		rand = filter(lambda v: all(c in elimset for c in tables[v]['children']),rand)
		#for h in range(len(rand)):
			#if all(c in elimset for c in tables[rand[h]]['children']):
				#rand.append(rand[h])
		factorvariables = {}
		for v in rand:
			factorvariables[v] = [p for p in tables[v]['parents'] if p not in e ]
			if v not in e:
				factorvariables[v].append(v)
		var = sorted(factorvariables.keys(), key=(lambda x: (len(factorvariables[x]), x)))[0]
		#print var
		if len(factorvariables[var]) > 0:
			factors.append(makefactor(var,factorvariables,e))
		if var != X.items()[0][0] and var not in e:
			factors = sumout(var,factors)
		elimset.add(var)
		for factor in factors:
			k = {}
			combins = list(itertools.product([True,False],repeat=len(factor[0])))
			combins.sort()
			for c in combins:
				newpairs = []
				#print factor[0]
				#print c
				#print list(c)
				for g in range(len(factor[0])):
					newpairs.append(factor[0][g])
					newpairs.append(c[g])
				#print "hhyyyyyyyy"
				#print tuple(newpairs)
				tuplelist = [(newpairs[i],newpairs[i+1]) for i in xrange(0,len(newpairs),2)]
				#print polylist
				for pair in tuplelist:
					#print pair
					k[pair[0]] = pair[1]
				key = tuple(k[v] for v in factor[0])
	if len(factors) >= 2:
		res = factors[0]
		p = factors[1:]
		for pp in p:
			result = pointwise_product(res,pp)
	else:
		result = factors[0]
	res1 = normalize((result[1][(False,)], result[1][(True,)]))
	#print result
	if X.items()[0][1]==False:
		return res1[0]
	else:
		return res1[1]

def enumeration_ask(bn,X,E,type):
	#print X
	#print E
	randome = []
	randomx = []
	dict = []
	flist = []
	randome.append([x[0] for x in E])
	randomx.append([x[0] for x in X])
	#print"huuu"
	#print randome
	#print randomx
	for x in range(len(randome[0])):
		for t in range(len(toposorted)):
			if toposorted[t]==randome[0][x]:
					dict.append(t)
	for y in range(len(randomx[0])):
		for s in range(len(toposorted)):
			if toposorted[s]==randomx[0][y]:
					dict.append(s)
					
	#print dict
	#key_max = max(dict.keys(), key=(lambda k: dict[k]))
	#print max(dict)
	reqlist = toposorted[:max(dict)+1]
	#print reqlist
	for l in range(len(reqlist)):
		if reqlist[l] not in decisionnodes:
			flist.append(reqlist[l])
	#print flist
	if type == 'P':  #if query is about probability
		Q = []
		e=cp.deepcopy(E)
		#print e
		for x in [False,True]:
			#print "heyyyyyyyyyyyyyyyyyyyyyyyyyyy"
			e[X.items()[0][0]]=x
			#print e
			#print toposorted
			Q.append(enumerate_all(reqlist,e)) #['A', 'B', 'C'],{'A': False, 'C': 'True'}
			#print Q
			#print "fffff"
			N=normalize(Q)
		#print "nihaa"
		if X[X.items()[0][0]]==False:
			return N[0]
		else:
			return N[1]
	elif type == 'E': # if query is EU
		#print "X&E"
		#print X
		#print E
		L = []
		list  = []
		#for x in [False,True]:   #not required coz we will be setting the value of X before calling this func.
		e=cp.deepcopy(E)
		e[X.items()[0][0]]=X.items()[0][1]
		#toposorted = topologicalsort(tables)  #sorting original bayes net nodes and deleting decision nodes
		for g in range(len(toposorted)):
			if toposorted[g] not in decisionnodes:
				list.append(toposorted[g])		
		#print toposorted
		#print list
		L.append(enumerate_all(list,e)) #['A', 'B', 'C'],{'A': False, 'C': 'True'}
		#print "Lv"
		#print L
		return L
		
def enumerate_all(vars,e):
	#print vars
	#print e
	#print len(vars)
	if len(vars)==0:
		#print "heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
		return 1.0
	Y=vars[0] #A
	if Y in e:
		#print "jdk"
		prob = calcgivenprobs(Y,e) * enumerate_all(vars[1:],e) # calcgivenprobs(A,{'A': False, 'C': 'True'}) * enumerate_all([B,C],{'A': False, 'C': 'True'})
	else:
		#print "hbg"
		probabilities = []
		e1=cp.deepcopy(e)
		for y in [True,False]:
			e1[Y]=y
			probabilities.append(calcgivenprobs(Y,e1) * enumerate_all(vars[1:],e1))
			#print probabilities
		prob=sum(probabilities)	
	return prob

def findexputility(vals,origquery):
	#print vals
	origquery1 = list(origquery.replace("=","").replace(" ","").replace(",","").replace(")","").replace("(",""))
	#print origquery1
	fr = ()
	pn = []
	pn = list(utility[0].split('|')[1].replace(" ",""))
	#print pn
	if any((True for x in decisionnodes if x in pn)):
		for h in range(len(pn)):
			if pn[h] in decisionnodes:
				if origquery1[origquery1.index(pn[h])+1]=='+':
					fr = fr + (True,)
				elif origquery1[origquery1.index(pn[h])+1]=='-':
					fr = fr + (False,)
			else:
				continue
		#print 'fr'
		#print fr
		products = []
		for j in range(len(vals)):
			tr = vals.keys()[j]
			#print 'tr'
			#print tr
			tr = tr + (fr)
			#print tr
			#print vals[vals.keys()[j]]
			#print float(utilitydict[tr])
			t=vals[vals.keys()[j]]*float(utilitydict[tr])
			products.append(t)
		s = sum(products)
		#print s
		return s
	else:
		#print vals
		#print utilitydict
		products = []
		for j in range(len(vals)):
			#print vals[vals.keys()[j]]
			#print float(utilitydict[vals.keys()[j]])
			t=vals[vals.keys()[j]]*float(utilitydict[vals.keys()[j]])
			products.append(t)
		#print products
		s = sum(products)
		#print products
		#print s
		return s
	

def main():
	#print tables
	for i in range(len(queries)): 
		if queries[i][0]=='P':
			E=makee(queries[i])
			#print "E:"
			#print E
			X=makex(queries[i])
			#print "hello"
			#print X
			#print E
			if len(X)==1 and len(E)>=1:
				#print "len1"
				result = elimination_ask(X,E,'P')
				#print result
				solution = round(result,2)
				#print solution
				#print "rounnnnnnd"
				print format(solution, '.2f')
			else:				#breaking down into single query varibles|mutiple evidence form # P(A,B|C,D)=P(A,B,C,D)/P(C,D)
				#print "ke"
				prod1 = []
				prod2 = []
				numerator=1
				denominator=1
				Q = mergedicts(queries[i]) # making P(A,B,C,D)
				for j in range(len(Q)):  #calculating P(A,B,C,D)= P(A|B,C,D)*P(B|C,D)*P(C|D)*P(D)
					x = collections.OrderedDict()
					e = collections.OrderedDict()
					x.update(Q.items()[j:j+1])
					e.update(Q.items()[j+1:])
					#print "gfg"
					#print x
					#print e
					prod1.append(elimination_ask(x,e,'P'))
					#print prod1
				#print prod1
				for k in range(len(prod1)):
					numerator=numerator*prod1[k]
				#print numerator
				for j in range(len(E)):  #calculating P(A,B,C,D)= P(A|B,C,D)*P(B|C,D)*P(C|D)*P(D) for evidence to give denominator
					x1 = collections.OrderedDict()
					e1 = collections.OrderedDict()
					x1.update(E.items()[j:j+1])
					e1.update(E.items()[j+1:])
					#print "hjjjk"
					#print x1
					#print e1
					prod2.append(elimination_ask(x1,e1,'P'))
					#print prod2
				#print prod2
				for l in range(len(prod2)):
					denominator=denominator*prod2[l]
				#print denominator
				finalres=round(numerator/denominator,2)
				#print "rounddd"
				print format(finalres, '.2f')
		elif queries[i][0]=='E':
			parents = []
			vals = []
			numerator=1
			t = list(utility[0].split('|')[1].replace(" ",""))
			for p in range(len(t)):
				if t[p] not in decisionnodes:
					parents.append(t[p]) 		#extracting utility nodes parents
			#print parents
			lengthofparents = len(parents)
			combs = list(itertools.product([True,False],repeat=lengthofparents)) #generating 2 power n combinations of T,F where n= no. of parents
			#print combs
			combodict = {}
			for v in range(len(combs)):	#set parent to each value call enum_ask
				#for w in range(lengthofparents):
					querieslist1 = collections.OrderedDict()
					evidence1 = collections.OrderedDict()
					numdict = collections.OrderedDict()
					prod3  = []
					den = []
					#prod4 = []
					randlist = []
					numerator = 1
					denominator = 1
					randlist = combs[v]
					combodict[tuple(randlist)]=0
					for f in range(len(randlist)):
						querieslist1[parents[f]]=randlist[f]
					evidence1 = mergedicts(queries[i])
					numdict=cp.deepcopy(querieslist1) #merging query and evidence into one dict.
					numdict.update(evidence1)
					#print "looop"
					#print querieslist1
					#print evidence1
					#print numdict
					for j in range(len(numdict)):
						x = collections.OrderedDict()
						e = collections.OrderedDict()
						x.update(numdict.items()[j:j+1])
						e.update(numdict.items()[j+1:])
						#print x
						#print e
						if x.keys()[0] not in decisionnodes:
							if x.keys()[0] in evidence1:
								den.append(elimination_ask(x,e,'P'))
								prod3.append(elimination_ask(x,e,'P'))
							else:
								prod3.append(elimination_ask(x,e,'P'))
							#print prod3
					#print "slow!"
					#print prod3
					for k in range(len(prod3)):
						numerator=numerator*prod3[k]
					#print numerator
					'''
					for j in range(len(evidence1)):
						x1 = collections.OrderedDict()
						e1 = collections.OrderedDict()
						x1.update(evidence1.items()[j:j+1])
						e1.update(evidence1.items()[j+1:])
						print x1
						print e1
						if x1.keys()[0] not in decisionnodes:
							print x1
							prod4.append(enumeration_ask(dectables,x1,e1,'P'))
							print "prod4"
							print prod4
					print "slowwww!"
					print prod4
					'''
					for l in range(len(den)):
						denominator=denominator*den[l]
						#print denominator
					#print numerator
					#print denominator
					finalres=numerator/denominator
					#print finalres
					#print type(finalres)
					combodict[tuple(randlist)]=finalres
					#print combodict
			ExpU=findexputility(combodict,queries[i])
			print int(round(ExpU))
		elif queries[i][0]=='M':
				conslist = []
				if '|' in queries[i]:
					fulllength = queries[i].replace(" ","").replace(",","")
					#print fulllength
					#print queries[i].index('|')
					decnodes=list(fulllength[4:fulllength.index('|')])
					#print decnodes
					combns = list(itertools.product(['+','-'],repeat=len(decnodes)))
					#print combns
					for z in range(len(combns)):
						newquery1 = "EU("
						for y in range(len(decnodes)):
							newquery1 = newquery1+decnodes[y]+" = "+combns[z][y]+','
						lenn=len(newquery1)
						newquery1=newquery1[:lenn-1]+" "+queries[i][queries[i].index('|'):]
						conslist.append(newquery1)
					#print conslist
				else:
					fulllength = queries[i].replace(" ","").replace(",","").replace(")","")
					decnodes=list(fulllength[4:])
					#print decnodes
					combns = list(itertools.product(['+','-'],repeat=len(decnodes)))
					#print combns
					for z in range(len(combns)):
						newquery = "EU("
						for y in range(len(decnodes)):
							newquery = newquery+decnodes[y]+" = "+combns[z][y]+','
						lenn=len(newquery)
						newquery=newquery[:lenn-1]+')'
						conslist.append(newquery)
					#print conslist
				meucands = {}
				for q in range(len(conslist)):
					parents = []		#CODE OF EU
					vals = []
					numerator=1
					t = list(utility[0].split('|')[1].replace(" ",""))
					for p in range(len(t)):
						if t[p] not in decisionnodes:
							parents.append(t[p]) 		#extracting utility nodes parents
					#print parents
					lengthofparents = len(parents)
					combs = list(itertools.product([True,False],repeat=lengthofparents)) #generating 2 power n combinations of T,F where n= no. of parents
					#print combs
					combodict = {}
					for v in range(len(combs)):	#set parent to each value call enum_ask
						#for w in range(lengthofparents):
							querieslist1 = collections.OrderedDict()
							evidence1 = collections.OrderedDict()
							numdict = collections.OrderedDict()
							prod3  = []
							prod4 = []
							randlist = []
							numerator = 1
							denominator = 1
							randlist = combs[v]
							#print tuple(randlist)
							combodict[tuple(randlist)]=0
							for f in range(len(randlist)):
								querieslist1[parents[f]]=randlist[f]
							evidence1 = mergedicts(conslist[q])
							numdict=cp.deepcopy(querieslist1) #merging query and evidence into one dict.
							numdict.update(evidence1)
							#print numdict
							for j in range(len(numdict)):
								x = collections.OrderedDict()
								e = collections.OrderedDict()
								x.update(numdict.items()[j:j+1])
								e.update(numdict.items()[j+1:])
								if x.keys()[0] not in decisionnodes:
									#print 'look here'
									#print x.keys()[0]
									prod3.append(elimination_ask(x,e,'P'))
							for k in range(len(prod3)):
								numerator=numerator*prod3[k]
							#print numerator
							for j in range(len(evidence1)):
								x1 = collections.OrderedDict()
								e1 = collections.OrderedDict()
								x1.update(evidence1.items()[j:j+1])
								e1.update(evidence1.items()[j+1:])
								if x1.keys()[0] not in decisionnodes:
									prod4.append(elimination_ask(x1,e1,'P'))
								#print prod2
								#print prod2
							#print prod4
							for l in range(len(prod4)):
								denominator=denominator*prod4[l]
								#print denominator
							finalres=numerator/denominator
							#print finalres
							combodict[tuple(randlist)]=finalres
					ExpU=findexputility(combodict,conslist[q])
					sent = conslist[q].split('|')[0].replace(" ","")
					signs = []
					#print sent
					for f in range(len(sent)):
						if sent[f]=='=':
							signs.append(sent[f+1])
					stringg=''
					#print signs
					for l in range(len(signs)):
						stringg=stringg+signs[l]+' '
					lll=len(stringg)
					meucands[stringg[:lll-1]]=ExpU
					#print meucands
				key_max = max(meucands.keys(), key=(lambda k: meucands[k]))
				print key_max,
				print int(round(meucands[key_max]))
if __name__=='__main__': main()