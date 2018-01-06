import numpy as np
import copy as cp
import operator
import sys
weights = [['99','-8','8','6','6','8','-8','99'],['-8','-24','-4','-3','-3','-4','-24','-8'],
['8','-4','7','4','4','7','-4','8'],['6','-3','4','0','0','4','-3','6'],['6','-3','4','0','0','4','-3','6'],
['8','-4','7','4','4','7','-4','8'],['-8','-24','-4','-3','-3','-4','-24','-8'],['99','-8','8','6','6','8','-8','99']]

f = open('input.txt','r')
current_player = f.readline().strip()
cutoff_depth = int(f.readline().strip())        
initial_board = [] 
for line in f:
		line= line.strip()
		initial_board.append( list(line) ) 
f.close()
#refreshed_board = []
copy_board=cp.deepcopy(initial_board)
final_scores = {}
trans_log = []



def main():
		AVAILABLE_MOVES=sorted(getAvailableMoves(initial_board,current_player)) #(4,4) (5,5)
		best_move = []
		#print AVAILABLE_MOVES
		#print AVAILABLE_MOVES[0]
		#print AVAILABLE_MOVES[1]
		#print len(AVAILABLE_MOVES)
		#print type(cutoff_depth)
		#best_move.append([0,0])
		#print best_move
		copy_board=cp.deepcopy(initial_board)
		best_move.append(alpha_beta_search(initial_board,current_player))
		#print best_move
		#print best_move[0][0][0]
		g = open("output.txt", 'w')
		sys.stdout = g
		if type(best_move[0]) == int:
			print board(initial_board)
			for i in range(0,len(trans_log)):
				print trans_log[i]
		else: 
			print board(refresh_board(initial_board,current_player,best_move[0]))
			for i in range(0,len(trans_log)):
				print trans_log[i]
		g.close()
		#print best_move
		#print refresh_board(copy_board,current_player,AVAILABLE_MOVES[0])
		#print refreshed_boards.keys()
		#print refreshed_boards
 	
def swap_player(current_player):
	if current_player=='X':
		return 'O'
	else:
		return 'X'
		
def max(a,b):
	if a>b:
		return a
	else:
		return b

def min(a,b):
	if a<b:
		return a
	else:
		return b

def alphabets(available_move):
	i=available_move[0]
	j=available_move[1]
	i=i+1
	j=chr(97+j)
	return j+str(i)

def board(input):
	for i in range(8):
		for j in range(8):
			print input[i][j],
		if i!=7:
			print "\r"
		else:
			pass
	return ""



def alpha_beta_search(initial_board,current_player):  #X
	MAX_available_moves = sorted(getAvailableMoves(initial_board,current_player)) #1 moves
	current_depth=0
	count=0
	alpha = float('-inf')
	beta = float('inf')
	value = float('-inf')
	
	if alpha==float('-inf'):
		A='-Infinity'
	elif alpha==float('inf'):
		A='Infinity'
	else:
		A=str(alpha)
	if beta==float('-inf'):
		B='-Infinity'
	elif beta==float('inf'):
		B='Infinity'
	else:
		B=str(beta)
	if value==float('-inf'):
		V='-Infinity'
	elif value==float('inf'):
		V='Infinity'
	else:
		V=str(value)
		
	trans_log.append('Node,Depth,Value,Alpha,Beta')	
	trans_log.append('root'+','+str(current_depth)+','+V+','+A+','+B)
	
	if len(MAX_available_moves)==0:	#no	
		count += 1 
		score = min_play(initial_board,swap_player(current_player),current_depth+1,count,alpha,beta,value,MAX_available_moves) 
		if alpha==float('-inf'):
				A='-Infinity'
		elif alpha==float('inf'):
				A='Infinity'
		else:
				A=str(alpha)
		if beta==float('-inf'):
				B='-Infinity'
		elif beta==float('inf'):
				B='Infinity'
		else:
				B=str(beta)
		if value==float('-inf'):
				V='-Infinity'
		elif value==float('inf'):
				V='Infinity'
		else:
				V=str(value)
				
		trans_log.append('root'+','+str(current_depth)+','+str(score)+','+str(score)+','+B)
		#print score
		return 1000
	else:
		best_move = MAX_available_moves[0]  #(3,2)
		best_score = float('-inf') 
		current_depth=0
		for i in range(0,len(MAX_available_moves)): #0,
			copy_board=cp.deepcopy(initial_board)
			x=MAX_available_moves[i][0] #5
			y=MAX_available_moves[i][1] #0
			clone=refresh_board(copy_board,current_player,MAX_available_moves[i])
    		
			score = min_play(clone,swap_player(current_player),current_depth+1,count,alpha,beta,value,MAX_available_moves[i]) #min(XXX,O,1,0,-inf,inf,-inf,[3,2])
			final_scores.update({i:score})
			if score > best_score:
				best_score = score
				alpha = score
		trans_log.append('root'+','+str(current_depth)+','+str(best_score)+','+str(alpha)+','+'Infinity') ##doubt
	return best_move
  

def min_play(board,player,current_depth,count,alpha,beta,value,move): #min(XXX,O,1,0,-inf,inf,-inf,[3,2]) #XXX,X,3,2,-Infinity,Infinity,-Infinity,[]
	moves = sorted(getAvailableMoves(board,player)) # 0 moves
	best_score = float('inf')
	value = float('inf')
	
	if current_depth==cutoff_depth:
		value=Evaluation_function(board,'X')
		if alpha==float('-inf'):
			A='-Infinity'
		elif alpha==float('inf'):
			A='Infinity'
		else:
			A=str(alpha)
		if beta==float('-inf'):
			B='-Infinity'
		elif beta==float('inf'):
			B='Infinity'
		else:
			B=str(beta)
		if value==float('-inf'):
			V='-Infinity'
		elif value==float('inf'):
			V='Infinity'
		else:
			V=str(value)
		if count==3:
			pass
		else:
			trans_log.append('pass'+','+str(current_depth)+','+V+','+A+','+B)   # print pass,3,4,-Infinity,Infinity
		return value
	else:
		pass
	if ( count <= 2 and len(moves) == 0 ): #yes
		count += 1 #count=1
		if alpha==float('-inf'):
			A='-Infinity'
		elif alpha==float('inf'):
			A='Infinity'
		else:
			A=str(alpha)
		if beta==float('-inf'):
			B='-Infinity'
		elif beta==float('inf'):
			B='Infinity'
		else:
			B=str(beta)
		if value==float('-inf'):
			V='-Infinity'
		elif value==float('inf'):
			V='Infinity'
		else:
			V=str(value)
		if ( count == 1 and len(moves) == 0 and  current_depth==1 and len(move) != 0):
			trans_log.append(alphabets(move)+','+str(current_depth)+','+V+','+A+','+B)  ##CHANGED HERE! # print c4,1,Infinity,-Infinity,Infinity
		elif ( count == 1 and len(moves) == 0 and  current_depth==1 and len(move) == 0 ):
			trans_log.append('pass'+','+str(current_depth)+','+V+','+A+','+B)
		else:
			trans_log.append('pass'+','+str(current_depth)+','+V+','+A+','+B) # print pass+1+inf+-inf+inf
		
		
		best_score = max_play(board,swap_player(player),current_depth+1,count,alpha,beta,value) #XXX,O,2,1,Infinity,-Infinity,Infinity
		
		if alpha==float('-inf'):
			A='-Infinity'
		elif alpha==float('inf'):
			A='Infinity'
		else:
			A=str(alpha)
		if beta==float('-inf'):
			B='-Infinity'
		elif beta==float('inf'):
			B='Infinity'
		else:
			B=str(beta)
		if value==float('-inf'):
			V='-Infinity'
		elif value==float('inf'):
			V='Infinity'
		else:
			V=str(value)
		if len(move) != 0:
			trans_log.append(alphabets(move)+','+str(current_depth)+','+str(best_score)+','+A+','+str(best_score)) # print availablemove too
		else:
			trans_log.append('pass'+','+str(current_depth)+','+str(best_score)+','+A+','+str(best_score))
		return best_score
	else:
		for i in range(0,len(moves)):
			copy_board=cp.deepcopy(initial_board)
			x=moves[i][0]
			y=moves[i][1]
			
			if alpha==float('-inf'):
				A='-Infinity'
			elif alpha==float('inf'):
				A='Infinity'
			else:
				A=str(alpha)
			if beta==float('-inf'):
				B='-Infinity'
			elif beta==float('inf'):
				B='Infinity'
			else:
				B=str(beta)
			if value==float('-inf'):
				V='-Infinity'
			elif value==float('inf'):
				V='Infinity'
			else:
				V=str(value)
			
			trans_log.append(str(current_depth)+','+V+','+A+','+B)    #print availablemove too
			
			clone=refresh_board(copy_board,current_player,moves[i])
			score = max_play(clone,swap_player(player),current_depth+1,count,alpha,beta,value)
			#print score
			#print score
			if score < best_score:
				best_move = moves[i]
				best_score = score
			if best_score < alpha:
				return best_score
			beta = min(best_score,beta)
			return best_score

def max_play(board,player,current_depth,count,alpha,beta,value):  #XXX,O,2,1,Infinity,-Infinity,Infinity
	moves = sorted(getAvailableMoves(board,player)) #0 moves #count pass
	best_score = float('-inf')
	score = 0
	value = float('-inf')
	if ( len(moves)==0 and count==2 ):
		count += 1
		best_score = min_play(board,swap_player(player),current_depth+1,count,alpha,beta,value,moves)
		if alpha==float('-inf'):
				A='-Infinity'
		elif alpha==float('inf'):
				A='Infinity'
		else:
				A=str(alpha)
		if beta==float('-inf'):
				B='-Infinity'
		elif beta==float('inf'):
				B='Infinity'
		else:
				B=str(beta)
		if value==float('-inf'):
				V='-Infinity'
		elif value==float('inf'):
				V='Infinity'
		else:
				V=str(value)
				
		trans_log.append('pass'+','+str(current_depth)+','+str(best_score)+','+A+','+B)
		return best_score

	if ( count <= 2 and len(moves) == 0 ): #pass case
			if alpha==float('-inf'):
				A='-Infinity'
			elif alpha==float('inf'):
				A='Infinity'
			else:
				A=str(alpha)
			if beta==float('-inf'):
				B='-Infinity'
			elif beta==float('inf'):
				B='Infinity'
			else:
				B=str(beta)
			if value==float('-inf'):
				V='-Infinity'
			elif value==float('inf'):
				V='Infinity'
			else:
				V=str(value)
				
			trans_log.append('pass'+','+str(current_depth)+','+V+','+A+','+B) #print pass+2+-inf+-inf+inf
			
			count += 1 #count=2
			best_score = min_play(board,swap_player(player),current_depth+1,count,alpha,beta,value,moves) #XXX,X,3,2,-Infinity,Infinity,-Infinity,[]
			alpha=best_score
			if alpha==float('-inf'):
				A='-Infinity'
			elif alpha==float('inf'):
				A='Infinity'
			else:
				A=str(alpha)
			if beta==float('-inf'):
				B='-Infinity'
			elif beta==float('inf'):
				B='Infinity'
			else:
				B=str(beta)
			if value==float('-inf'):
				V='-Infinity'
			elif value==float('inf'):
				V='Infinity'
			else:
				V=str(value)
				
			trans_log.append('pass'+','+str(current_depth)+','+str(best_score)+','+A+','+B)  #AMBIGIOUS ALPHA! have to set alpha to best score and print?
			
			return best_score
	else:
		if current_depth==cutoff_depth:
			value=Evaluation_function(board,player)
			#print value
			return value
	
		else:
			for i in range(0,len(moves)):
				copy_board=cp.deepcopy(initial_board)
				x=moves[i][0] #4
				y=moves[i][1] #4
				best_score = float('-inf')
				clone=refresh_board(copy_board,current_player,moves[i])
				score = min_play(clone,swap_player(player),current_depth+1,count,alpha,beta,value,moves[i])
				#this at depth 2 after returning from leaf node, now set alpha and value to evaluate function
				
				value = score
				#print score
				#print best_score
				
				if score > best_score:
					best_move = moves[i]
					best_score = score
					#print best_score
				if best_score >= beta:
					return best_score
				alpha = max(best_score,alpha)
				#print best_score
			return best_score	


def refresh_board(board,current_player,move):
	 		x=move[0] #4
	 		y=move[1]#5
	 		if current_player=='X':
	 			#filling to the right
	 			if y!=7 and board[x][y+1]=='O':
	 				for k in range(y,8):   #k=2,8
	 					if board[x][k]=='*':
	 						board[x][k]='X'
	 					elif board[x][k]=='O':
	 						board[x][k]='X'
	 					elif board[x][k]=='X':
	 						break
	 			#filling to the left
	 			if board[x][y-1]=='O':
	 				for k in range(y,0,-1): #k=4,3,2,1
	 					if board[x][k]=='*':
	 						board[x][k]='X'
	 					elif board[x][k]=='O':
	 						board[x][k]='X'
	 					elif board[x][k]=='X':
	 						break
	 			#filling downwards
	 			if x!=7 and board[x+1][y]=='O'  :
	 					for k in range(x,8): #k=4,3,2,1
	 						if board[k][y]=='*':
	 							board[k][y]='X'
	 						elif board[k][y]=='O':
	 							board[k][y]='X'
	 						elif board[k][y]=='X':
	 							break
	 			#filling upwards
	 			if board[x-1][y]=='O':
	 				for k in range(x,0,-1): #k=4,3,2,1
	 					if board[k][y]=='*':
	 						board[k][y]='X'
	 					elif board[k][y]=='O':
	 						board[k][y]='X'
	 					elif board[k][y]=='X':
	 						break
	 			#filling downwards left
	 			if x!=7 and board[x+1][y-1]=='O': #x=1   y=5
	 				for k in range(0,8): 
	 					if board[x+k][y-k]=='*':
	 						board[x+k][y-k]='X'
	 					elif board[x+k][y-k]=='O':
	 						board[x+k][y-k]='X'
	 					elif board[x+k][y-k]=='X':
	 						break
	 			#filling upwards left
	 			if board[x-1][y-1]=='O': #x=5   y=5
	 				for k in range(0,8): 
	 					if board[x-k][y-k]=='*':
	 						board[x-k][y-k]='X'
	 					elif board[x-k][y-k]=='O':
	 						board[x-k][y-k]='X'
	 					elif board[x-k][y-k]=='X':
	 						break
	 			#filling upwards right
	 			if y!=7 and board[x-1][y+1]=='O': #x=5   y=1
	 				for k in range(0,8): 
	 					if board[x-k][y+k]=='*':
	 						board[x-k][y+k]='X'
	 					elif board[x-k][y+k]=='O':
	 						board[x-k][y+k]='X'
	 					elif board[x-k][y+k]=='X':
	 						break	
	 			#filling downwards right
	 			if x!=7 and y!=7 and board[x+1][y+1]=='O': #x=1   y=1
	 				for k in range(0,8): 
	 					if board[x+k][y+k]=='*':
	 						board[x+k][y+k]='X'
	 					elif board[x+k][y+k]=='O':
	 						board[x+k][y+k]='X'
	 					elif board[x+k][y+k]=='X':
	 						break
	 		if current_player=='O':
	 			#filling to the right
	 			if y!=7 and board[x][y+1]=='X':
	 				for k in range(y,8):   #k=2,8
	 					if board[x][k]=='*':
	 						board[x][k]='O'
	 					elif board[x][k]=='X':
	 						board[x][k]='O'
	 					elif board[x][k]=='O':
	 						break
	 			#filling to the left
	 			if board[x][y-1]=='X':
	 				for k in range(y,0,-1): #k=4,3,2,1
	 					if board[x][k]=='*':
	 						board[x][k]='O'
	 					elif board[x][k]=='X':
	 						board[x][k]='O'
	 					elif board[x][k]=='O':
	 						break
	 			#filling downwards
	 			if x!=7 and board[x+1][y]=='X':
	 				for k in range(x,8): #k=4,3,2,1
	 					if board[k][y]=='*':
	 						board[k][y]='O'
	 					elif board[k][y]=='X':
	 						board[k][y]='O'
	 					elif board[k][y]=='O':
	 						break
	 			#filling upwards
	 			if board[x-1][y]=='X':
	 				for k in range(x,0,-1): #k=4,3,2,1
	 					if board[k][y]=='*':
	 						board[k][y]='O'
	 					elif board[k][y]=='X':
	 						board[k][y]='O'
	 					elif board[k][y]=='O':
	 						break
	 			#filling downwards left
	 			if x!=7 and board[x+1][y-1]=='X': #x=1   y=5
	 				for k in range(0,8): 
	 					if board[x+k][y-k]=='*':
	 						board[x+k][y-k]='O'
	 					elif board[x+k][y-k]=='X':
	 						board[x+k][y-k]='O'
	 					elif board[x+k][y-k]=='O':
	 						break
	 			#filling upwards left
	 			if board[x-1][y-1]=='X': #x=5   y=5
	 				for k in range(0,8): 
	 					if board[x-k][y-k]=='*':
	 						board[x-k][y-k]='O'
	 					elif board[x-k][y-k]=='X':
	 						board[x-k][y-k]='O'
	 					elif board[x-k][y-k]=='O':
	 						break
	 			#filling upwards right
	 			if y!=7 and board[x-1][y+1]=='X': #x=5   y=1
	 				for k in range(0,8): 
	 					if board[x-k][y+k]=='*':
	 						board[x-k][y+k]='O'
	 					elif board[x-k][y+k]=='X':
	 						board[x-k][y+k]='O'
	 					elif board[x-k][y+k]=='O':
	 						break	
	 			#filling downwards right
	 			if x!=7 and y!=7 and board[x+1][y+1]=='X': #x=1   y=1
	 				for k in range(0,8): 
	 					if board[x+k][y+k]=='*':
	 						board[x+k][y+k]='O'
	 					elif board[x+k][y+k]=='X':
	 						board[x+k][y+k]='O'
	 					elif board[x+k][y+k]=='O':
	 						break	
	 		#print board		 				
	 		return board
	
def Evaluation_function(initial_board,current_player):
	sumofX=0
	sumofO=0
	for i in range(8):
		for j in range(8):
			if initial_board[i][j]=='X':
				sumofX=sumofX+int(weights[i][j])
			elif initial_board[i][j]=='O':
					sumofO=sumofO+int(weights[i][j])
	if current_player=='X':
		return sumofX-sumofO
	else:
		return sumofO-sumofX
		
def getAvailableMoves(board,current_player):
	valid_moves_X = []
	valid_moves_O = []
	if current_player=='X':
		for i in range(8):
			for j in range(8):
				if board[i][j]=='X':
					#checking to the right
					if j!=7 and board[i][j+1]=='O':
						for p in range(j+2,8):
							if board[i][p]=='O':
								continue
							elif board[i][p]=='*': 
								valid_moves_X.append([i,p])
								break
					#checking to the left
					if board[i][j-1]=='O':
						for p in range(j-2,0,-1):
							if board[i][p]=='O':
								continue
							elif board[i][p]=='*': 
								valid_moves_X.append([i,p])
								break	
					#checking above
					if board[i-1][j]=='O':
						for p in range(i-2,-1,-1):
							if board[p][j]=='O':
								continue
							elif board[p][j]=='*': 
								valid_moves_X.append([p,j])
								break
					#checking below
					if i!=7 and board[i+1][j]=='O':
						for p in range(i+2,8):
							if board[p][j]=='O':
								continue
							elif board[p][j]=='*': 
								valid_moves_X.append([p,j])
								break	
					#upper-right diagonal
					if j!=7 and board[i-1][j+1]=='O':
						p=i-2
						k=j+2
						while p>=0 and k<=7:
							if board[p][k]=='O':
								pass
							elif board[p][k]=='*':
								valid_moves_X.append([p,k])
								break
							p=p-1
							k=k+1
								
					#lower-right diagonal
					if i!=7 and j!=7 and board[i+1][j+1]=='O':
						p=i+2
						k=j+2
						while p<=7 and k<=7:
							if board[p][k]=='O':
								pass
							elif board[p][k]=='*':
								valid_moves_X.append([p,k])
								break
							p=p+1
							k=k+1
								
					#lower-left diagonal
					if i!=7 and board[i+1][j-1]=='O':
						p=i+2
						k=j-2
						while p<=7 and k>=0:
							if board[p][k]=='O':
								pass
							elif board[p][k]=='*':
								valid_moves_X.append([p,k])
								break
							p=p+1
							k=k-1
								
					#upper-left diagonal
					if board[i-1][j-1]=='O':
						p=i-2
						k=j-2
						while p>=0 and k>=0:
							if board[p][k]=='O':
								pass
							elif board[p][k]=='*':
								valid_moves_X.append([p,k])
								break
							p=p-1
							k=k-1
								
		return valid_moves_X
	if current_player=='O':
		for i in range(8):
			for j in range(8):
				if board[i][j]=='O':
					#checking to the right
					if j!=7 and board[i][j+1]=='X':
						for p in range(j+2,8):
							if board[i][p]=='X':
								continue
							elif board[i][p]=='*': 
								valid_moves_O.append([i,p])
								break
					#checking to the left
					if board[i][j-1]=='X':
						for p in range(j-2,-1,-1):
							if board[i][p]=='X':
								continue
							elif board[i][p]=='*': 
								valid_moves_O.append([i,p])
								break	
					#checking above
					if board[i-1][j]=='X':
						for p in range(i-2,-1,-1):
							if board[p][j]=='X':
								continue
							elif board[p][j]=='*': 
								valid_moves_O.append([p,j])
								break
					#checking below
					if i!=7 and board[i+1][j]=='X':
						for p in range(i+2,8):
							if board[p][j]=='X':
								continue
							elif board[p][j]=='*': 
								valid_moves_O.append([p,j])
								break	
					#upper-right diagonal
					if j!=7 and board[i-1][j+1]=='X':
						p=i-2
						k=j+2
						while p>=0 and k<=7:
							if board[p][k]=='X':
								pass
							elif board[p][k]=='*':
								valid_moves_O.append([p,k])
								break
							p=p-1
							k=k+1
								
					#lower-right diagonal
					if i!=7 and j!=7 and board[i+1][j+1]=='X':
						p=i+2
						k=j+2
						while p<=7 and k<=7:
							if board[p][k]=='X':
								pass
							elif board[p][k]=='*':
								valid_moves_O.append([p,k])
								break
							p=p+1
							k=k+1
								
					#lower-left diagonal
					if i!=7 and board[i+1][j-1]=='X':
						p=i+2
						k=j-2
						while p<=7 and k>=0:
							if board[p][k]=='X':
								pass
							elif board[p][k]=='*':
								valid_moves_O.append([p,k])
								break
							p=p+1
							k=k-1
								
					#upper-left diagonal
					if board[i-1][j-1]=='X':
						p=i-2
						k=j-2
						while p>=0 and k>=0:
							if board[p][k]=='X':
								pass
							elif board[p][k]=='*':
								valid_moves_O.append([p,k])
								break
							p=p-1
							k=k-1
															
		return valid_moves_O
						
#Evaluation_function(initial_board,current_player)
#get_curr_coord(initial_board,current_player)
#getAvailableMoves(initial_board,current_player)
if __name__ == "__main__": main()