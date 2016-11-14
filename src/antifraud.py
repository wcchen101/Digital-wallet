import string
import csv
import os
import tempfile

#This is to get the current path and set the path name for our own need
cwd = os.getcwd()
parentPath = os.path.abspath(os.path.join(cwd, os.pardir))

class Graph:
	""" Overview of the class.
	This is the Graph for PayMo in order to save the friends informaiton.

	Function:
		__init__(self): A deafult constructor
		__iter__(self): a function for iterate the graph
		__contains__(self, key): function to find the certain vertex in graph
		addVertex(self, key): A function can add the friends as a key attribute into the graph structure.
		getVertex(self, n): A function to get the friends information as a key node.
		addEdge(self, f1, f2): A function to set up relationship between two friends.
		getVertices(self): A function to get all friends(vertices) inside the Graph 
	"""
	def __init__(self):
		self.verticeList = {}
		self.verticeNum = 0

	def __iter__(self):
		return iter(self.verticeList.values())

	def __contains__(self, key):
		return key in self.verticeList

	def addVertex(self, key):
		self.verticeNum = self.verticeNum + 1
		newVertex = Vertex(key)
		self.verticeList[key] = newVertex
		return newVertex

	def getVertex(self, n):
		if n in self.verticeList:
			return self.verticeList[n]
		else:
			return None

	def addEdge(self, f1, f2):
		if f1 not in self.verticeList:
			nv = self.addVertex(f1)
		if f2 not in self.verticeList:
			nv = self.addVertex(f2)
		self.verticeList[f1].addNeighbor(self.verticeList[f2])
		self.verticeList[f2].addNeighbor(self.verticeList[f1])

	def getVertices(self):
		return self.verticeList.keys()

class Vertex:
	""" Overview of the class.
		This Vertex class is to define a friends node. 

		Function:
		__init__(self, key): this function is the vertex constructor
		__str__(self): this function is to print out the value of certain vertext which is firend info
		addNeighbor(self, neighbor): This function is to add new friends inside the friend's node. 
		getValue(self): This function is to get the friend self identity number
		getConnections(self): This function is to show all related connection for certain friend
	"""
	def __init__(self, key):
		self.id = key
		self.adjacent = {}
	
	def __str__(self):
		return str(self.id) + str([x.id for x in self.adjacent])
	
	def addNeighbor(self, neighbor):
		self.adjacent[neighbor] = neighbor

	def getValue(self):
		return self.id

	def getConnections(self):
		return self.adjacent.keys()

def open_txt():
	""" The overview of this funciton.
	This function mainly contains two part: adding friends connection from the batch_payment.txt, 
	and validatae the payment from the stream_payment.txt.
		Attribute:
			batch_payment_filename: This is the filep ath for batch_payment.txt
			stream_payment_filename: this is the file path for stream_payment.txt
	"""

	batch_payment_filename = "paymo_input/batch_payment.txt"
	stream_payment_filename = "paymo_input/stream_payment.txt"
	
	f = open(parentPath + '/'+ batch_payment_filename, "r")
	next(f)
	g = Graph()

	#get the batch_payment information, and build up the payment records
	for line in f:
		try:  
			fields = line.split(',')
			field1 = fields[1]
			field2 = fields[2]
			if (field1 not in g.verticeList):
				g.addVertex(field1)
			if (field2 not in g.verticeList):
				g.addVertex(field2)

			payer = g.getVertex(field1)
			receiver = g.getVertex(field2)
			g.addEdge(field1, field2)
			# print(field1, field2)
		except IndexError:
			continue
	print("batch payment added sccessfully!")

	#get the stream_payment information, and validate the payment
	checkFile = open(parentPath + '/'+ stream_payment_filename, "r")
	next(checkFile)
	for line in checkFile:
		try:  
			fields = line.split(',')
			field1 = fields[1]
			field2 = fields[2]
			isTrusted = False
			payer = g.getVertex(field1)
			receiver = g.getVertex(field2)
			check_payment_record(payer, receiver)
			check_friends_friednds(payer, receiver)
			check_4th_degree_friends(payer, receiver)
		except IndexError:
			continue
	print("validate the stream_payment sucessfully")

def check_one_degree(payers, receivers):
	""" Summary of the function.
		This function is to check if two friends are one degree friend for each other.
		It just simply check if payers' adjacent friends showing receivers. If yes, make
		isTrusted to True. Otherwise, false.

		Attributes: 
			isTrusted: this boolean attribute shows that if this two friends are in one degree. 

		Retrun:
			the return value is isTrusted. If the two friends are in one degree should return true.
			Otherwise, it returns False.

	"""

	isTrusted = False
	for payer in payers.adjacent:
		valPayer = payer.getValue()
		valReceiver = receivers.getValue()
		if valPayer == valReceiver:
			isTrusted = True
	return isTrusted

def check_in_2nd_degree(payers, recievers):
	""" Summary of the function.
		This function is the algorithm to check if two firends are in 2nd degree for each other.
		The idea of this algorithm is to add the payer's adjacent friends into a unique set.
		Then use the receivers's adjacent friends to check if it has any overlapping friends.
		Once the receivers find the friends is in the payers' friends. It breaks the loop to 
		optimize the process. Then change the isIn2ndDegree to True.

		Attributes: 
			isIn2ndDegree: it shows boolean attribute whether two friends are in 2nd degree

		Return:
			The return vale is isIn2ndDegree. If they are in 2nd degree friends return True.
			Otherwise, it returns false.
	"""	

	isIn2ndDegree = False
	checkSet = set()
	for payer in payers.adjacent:
		val = payer.getValue()
		checkSet.add(val)

	for receive in recievers.adjacent:
		val = receive.getValue()
		if val in checkSet:
			isIn2ndDegree = True
			break
	return isIn2ndDegree

def check_in_4th_degree(payers, receivers):
	""" Summary of the funciton.
		This funciton is the algorithm to check if two friends are in 4th degree friends for each other.

		This algorithm contains two part: 
		1st part: is to use two loops to save the all payers in 2nd degree friends. A
		lso, prevent the payers' friends loop back to its payer. Then save all payer's friends into a common set
		2nd part: is also to use two loops to save all receivers in 2nd degree friends. However, at the same time
		it check if it has any overlapping friends by checking the common set. If yes, set isIn4thDegree to true.
		Otherwise, set false.

	"""

	isIn4thDegree = False
	ancestorSet = set()
	valPayers = payers.getValue()
	valReceivers = receivers.getValue()
	for payer in payers.adjacent:
		valPayer = payer.getValue()
		if valPayer in ancestorSet:
			isIn4thDegree = True
			return isIn4thDegree
		for payerChild in payer.adjacent:
			valPayerChild = payerChild.getValue()
			if valPayerChild != valPayers:
				if valPayerChild not in ancestorSet:
					ancestorSet.add(valPayerChild)
				else:
					isIn4thDegree = True
					return isIn4thDegree

	for receiver in receivers.adjacent:
		valReceiver = receiver.getValue()
		if valReceiver in ancestorSet:
			isIn4thDegree = True
			return isIn4thDegree
		for receiverChild in receiver.adjacent:
			valReceiverChild = receiverChild.getValue()
			if valReceiverChild != valReceivers:
				if valReceiverChild not in ancestorSet:
					ancestorSet.add(valReceiverChild)
				else:
					isIn4thDegree = True
					return isIn4thDegree
	return isIn4thDegree

def check_payment_record(payers, receivers):
	""" Summary of the function.
		This function is for insight coding challenge feature 1. 
		
		It will get if trusted information from the function check_one_dgree(), if it trusted
		return true and write trusted in the output1.txt file. Otherwise, write unverified in the
		output1.txt

		Attributes: 
			isTrusted: this is to check if the payment is trusted or not. and decide which to 
			write into the output1.txt file
	"""

	output1 = tempfile.TemporaryFile(mode='w+t')
	output1 = open(parentPath + '/'+ 'paymo_output/output1.txt', 'a')
	isTrusted = False

	#call if it is in one degree algorithm
	isTrusted = check_one_degree(payers,receivers)
	if isTrusted is False:
		output1.write("unverified" + "\n")
	else:
		output1.write("trusted" + "\n")
	output1.close()

def check_friends_friednds(payers, receivers):
	""" Summary of the function.
		This function is for insight coding challenge feature 2. 
		
		It will get if trusted information from the function check_one_dgree() and check_in_2nd_degree(),
		it will check if it is in first degree. If not in first degree, it will check if it is in 2nd degree.
		if it is trusted return true and write trusted in the output2.txt file. 
		Otherwise, write unverified in the output2.txt

		Attributes: 
			is2ndDegree: this is to check if the payment is trusted or not. and decide which to 
			write into the output2.txt file
	"""	

	output2 = open(parentPath + '/'+ 'paymo_output/output2.txt', 'a')
	is2ndDegree = False

	#check payment record first
	is2ndDegree = check_one_degree(payers, receivers)

	if is2ndDegree is True:
		output2.write("trusted"+ "\n")

	else:
		# check is in 2nd degree if neccessary
		is2ndDegree = check_in_2nd_degree(payers, receivers)
		if is2ndDegree is False:
			output2.write("unverified" + "\n")
		else:
			output2.write("trusted" + "\n")

		output2.close()

def check_4th_degree_friends(payers, receivers):
	""" Summary of the function.
		This function is for insight coding challenge feature 3. 
		
		It will get if trusted information from the function check_one_dgree(), check_in_2nd_degree() and 
		check_in_4th_degree. it will check if it is in first degree. If not in first degree, it will 
		check if it is in 2nd degree. if not, it will finally check if it is in 4th degree friends.
		if it is trusted return true and write trusted in the output3.txt file. 
		Otherwise, write unverified in the output3.txt

		Attributes: 
			isIn4thDegree: this is to check if the payment is trusted or not. and decide which to 
			write into the output3.txt file
	"""	
	output3 = open(parentPath + '/'+ 'paymo_output/output3.txt', 'a')
	isIn4thDegree = False
	
	#chech in first degree and in 2nd degree algorithm first
	is4thDegree1 = check_one_degree(payers, receivers)
	is4thDegree2 = check_in_2nd_degree(payers, receivers)

	if is4thDegree1 or is4thDegree2:
		isIn4thDegree = True
		output3.write("trusted" + "\n")

	else:
		#check if it is in 4th degree if necessary
		isIn4thDegree = check_in_4th_degree(payers, receivers)

		if isIn4thDegree is False:
			output3.write("unverified" + "\n")
		else:
			output3.write("trusted" + "\n")

	output3.close()

def main():
	"""Summary of this function.
		This is the function to start this program by calling open_txt()
	"""
	open_txt()

if __name__ == '__main__':
	main()