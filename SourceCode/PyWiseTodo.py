from time import sleep, strftime
from os import system, remove
from subprocess import Popen
from traceback import print_exc

DevMode = 0 #set to 1 to get bug reports
File = "TodoTXT.txt" #chage flie name as needed
List = []
PriList = []
#CACHE variables
StartUpCount = 0 	#Stored on line 1
ErrorCount = 0 		#Stored on line 2
TaskCount = 0		#Stored on line 3

def load(): #Open text file and load items to list
	global List
	global File
	List = []
	State = open(File, "r+")
	for Line in State:
		Line = Line.replace("\n", "")
		List.append(Line)
	loadPri()

def save(): #Update text file
	global List
	global PriList
	global File
	remove(File)
	State = open(File, "a")
	C = 0
	for Item in List:
		State.write(List[C]+"PRI"+PriList[C]+"\n")
		C = C+1

def loadPri(): #Split the loaded list into list of text and pri list
	global PriList
	global List
	PriList = []
	TempList = []
	Lenght = len(List)
	C = 0
	while C < Lenght:
		CUT = List[C].split("PRI")
		TempList.append(CUT[0])
		PriList.append(CUT[1])
		C = C+1
	List = []
	List = TempList

def post(): #Post list to screen with colors
	global List
	global PriList
	system("cls")
	print(" ")
	print("\t"+"\t"+"\033[1;37;40m "+"\t--Todo List--")
	print(" ")
	C = 0
	Max = len(List)
	while C < Max:
		Coef = str(C+1)
		if PriList[C] == "1":
			print("\t"+"\033[1;32;40m "+Coef+"\t"+ List[C])
		elif PriList[C] == "2":
			print("\t"+"\033[1;33;40m "+Coef+"\t"+ List[C])
		elif PriList[C] == "3":
			print("\t"+"\033[1;31;40m "+Coef+"\t"+ List[C])
		else:
			print("\t"+"\033[1;37;40m "+Coef+"\t"+List[C])
		C = C+1
	print("\033[1;37;40m "+" ")
	if len(List) == 0:
		print("\t"+"\033[1;35;40m "+"\tNothing To Do !!")
		print("\033[1;37;40m "+" ")

def add(Item): #add item to list
	global List
	global PriList
	List.append(Item)
	PriList.append("0")

def pri(Num, NP): #chage pri of item in list
	global PriList
	Max = len(PriList)
	C = int(Num)-1
	if C >= Max or C < 0:
		return
	if int(NP) > 3 or int(NP) < 0:
		return
	PriList[C] = NP

def done(Num): #remove item from list
	global List
	global PriList
	global TaskCount
	Max = len(List)
	C = int(Num)-1
	if C >= Max or C < 0:
		return
	del List[C]
	del PriList[C]
	TaskCount = TaskCount+1
	UpCACHE(3, TaskCount)

def switch(NumO,NumT): #witch position of two items in list
	global List
	global PriList
	CO = int(NumO)-1
	CT = int(NumT)-1
	Max = len(List)
	if CO >= Max or CT >= Max or CO < 0 or CT < 0:
		return
	TempVal = ""
	TempVal = List[CO]
	List[CO] = List[CT]
	List[CT] = TempVal
	TempVal = "0"
	TempVal = PriList[CO]
	PriList[CO] = PriList[CT]
	PriList[CT] = TempVal

def fliter(TEXT): #filter by a search term
	global List
	global PriList
	system("cls")
	print(" ")
	print("\t"+"\t"+"\t--Filtered List--")
	print(" ")
	FlitList = []
	FLP = []
	C = 0
	for Item in List:
		if TEXT in Item:
			FlitList.append(Item)
			FLP.append(PriList[C])
		C = C+1
	C = 0
	Max = len(FlitList)
	while C < Max:
		Coef = str(C+1)
		if FLP[C] == "1":
			print("\t"+"\033[1;32;40m "+Coef+"\t"+ FlitList[C])
		elif FLP[C] == "2":
			print("\t"+"\033[1;33;40m "+Coef+"\t"+ FlitList[C])
		elif FLP[C] == "3":
			print("\t"+"\033[1;31;40m "+Coef+"\t"+ FlitList[C])
		else:
			print("\t"+"\033[1;37;40m "+Coef+"\t\asdfgsd"+FlitList[C])
		C = C+1
	print("\033[1;37;40m "+" ")
	print(" ")
	print("Press any key to continue")
	input("")

def fliterpri(Num): #filter by a priority level
	global List
	global PriList
	system("cls")
	print(" ")
	print("\t"+"\t"+"\t--Filtered List--")
	print(" ")
	FlitList = []
	FLP = []
	C = 0
	for Item in PriList:
		if Num in Item:
			FlitList.append(List[C])
			FLP.append(Item)
		C = C+1
	C = 0
	Max = len(FlitList)
	while C < Max:
		Coef = str(C+1)
		if FLP[C] == "1":
			print("\t"+"\033[1;32;40m "+Coef+"\t"+ FlitList[C])
		elif FLP[C] == "2":
			print("\t"+"\033[1;33;40m "+Coef+"\t"+ FlitList[C])
		elif FLP[C] == "3":
			print("\t"+"\033[1;31;40m "+Coef+"\t"+ FlitList[C])
		else:
			print("\t"+"\033[1;37;40m "+Coef+"\t\asdfgsd"+FlitList[C])
		C = C+1
	print("\033[1;37;40m "+" ")
	print(" ")
	print("Press any key to continue")
	input("")

def BulkAdd(): #open text flie to bulk add items
	Info = open("BulkAdd.txt", "a")
	Info.write("--- Write Tasks Line by Line below ---\n+XX @XX/XX/2017 TEXT")
	Info.close()
	p = Popen(('notepad.exe', 'BulkAdd.txt'))
	p.wait()
	Info = open("BulkAdd.txt", "r+")
	C = 0
	for Line in Info:
		if "\n" in Line:
			Line = Line.replace("\n", "")
		if C > 0:
			add(Line)
		C = C+1
	Info.close()
	remove("BulkAdd.txt")

def BulkWork(): #open text file to bulk edit items
	global File
	p = Popen(('notepad.exe', File))
	p.wait()
	load()

def SortPri(S): #buble sort by priority
	if S == 0:
		system("cls")
		print("Sorting...")
	global PriList
	Lenght = len(PriList)
	Cur = 0
	C = 1
	while OrderCheck(PriList):
		while C < Lenght:
			if int(PriList[Cur]) <= int(PriList[(Cur+1)]):
				switch((Cur+1), (Cur+2))
			Cur = Cur+1
			C = C+1
			if S == 1:
				post()
				sleep(0.02)
		C = 1
		Cur = 0

def OrderCheck(L): #check order of items in list
	Lenght = len(L)
	Cur = 0
	C = 1
	while C < Lenght:
		if int(L[Cur]) >= int(L[(Cur+1)]):
			Cur = Cur+1
		else:
			return True
		C = C+1
	return False

def SortDate(S): #buble sort by date
	global List
	global PriList
	DateList = []
	for Item in List:
		if "@" in Item:
			day = Item[(Item.index("@")+1)]+Item[(Item.index("@")+2)]
			month = Item[(Item.index("@")+4)]+Item[(Item.index("@")+5)]
			year = Item[(Item.index("@")+7)]+Item[(Item.index("@")+8)]+Item[(Item.index("@")+9)]+Item[(Item.index("@")+10)]
			Date = (int(day)*86164)+(int(month)*2592000)+(int(year)*31563000)
			DateList.append(Date)
		else:
			DateList.append(0)
	if S == 0:
		system("cls")
		print("Sorting...")
	Lenght = len(List)
	Cur = 0
	C = 1
	while OrderCheck(DateList):
		while C < Lenght:
			if int(DateList[Cur]) <= int(DateList[(Cur+1)]):
				switch((Cur+1), (Cur+2))
				temp = DateList[Cur]
				DateList[Cur] = DateList[(Cur+1)]
				DateList[(Cur+1)] = temp
			Cur = Cur+1
			C = C+1
			if S == 1:
				post()
				sleep(0.02)
		C = 1
		Cur = 0
	List.reverse()
	PriList.reverse()

def PriByDate(): #prooritiz by date
	global List
	global PriList
	DateList = []
	for Item in List:
		if "@" in Item:
			day = Item[(Item.index("@")+1)]+Item[(Item.index("@")+2)]
			month = Item[(Item.index("@")+4)]+Item[(Item.index("@")+5)]
			year = Item[(Item.index("@")+7)]+Item[(Item.index("@")+8)]+Item[(Item.index("@")+9)]+Item[(Item.index("@")+10)]
			Date = (int(day)*86164)+(int(month)*2592000)+(int(year)*31536000)
			DateList.append(Date)
		else:
			DateList.append(0)
	TDay = int(strftime("%d"))
	TMonth = int(strftime("%m"))
	TYear = int(strftime("%y"))+2000
	TDate = (TDay*86164)+(TMonth*2592000)+(TYear*31536000)
	C = 0
	for Item in List:
		if DateList[C] <= TDate:
			PriList[C] = "3"
		elif DateList[C] < (TDate+86400):
			PriList[C] = "3"
		elif DateList[C] <= (TDate+172800):
			PriList[C] = "2"
		elif DateList[C] <= (TDate+604800):
			PriList[C] = "1"
		else:
			PriList[C] = "0"
		C = C+1

def Export(): #export and move using a bat file
	global List
	global PriList
	Ex = open("Todolist.txt", "w")
	C = 0
	Ex.write("\t\t -- Todo -- \n")
	Ex.write("\n")
	for Item in List:
		Ex.write("PRI: "+PriList[C]+"\t"+List[C]+"\n")
		C = C+1
	Ex.close()
	system("start MoveList.bat")

def listen(): #listen for a comand
	global LOOP
	global DevMode
	Input = input("~")
	if Input == "exit":
		LOOP = 1
	elif Input == "ba":
		BulkAdd()
	elif Input == "bw":
		BulkWork()
	elif Input == "sp":
		SortPri(0)
	elif Input == "sps":
		SortPri(1)
	elif Input == "sd":
		SortDate(0)
	elif Input == "sds":
		SortDate(1)
	elif Input == "pd":
		PriByDate()
	elif Input == "ex":
		Export()
	elif Input == "er" and DevMode == 1:		#DevMode only
		system("start PyWiseTodo.py")
		exit()
	elif Input == "rc" and DevMode == 1:		#DevMode only
		ReCACHE()
	elif Input[0] == "h" or Input[0] == "help":
		HT = open("HELP.txt", "r")
		system("cls")
		for Line in HT:
			Line = Line.replace("\n", "")
			print(Line)
		print(" ")
		print("Press any key to continue")
		input("")								#normal comands
	if "`" in Input:
		Input = Input.split("`")
		if len(Input) > 2:
			return
		if Input[0] == "a" or Input[0] == "add":
			add(Input[1])
		elif Input[0] == "p" or Input[0] == "pri":
			Vals = Input[1].split(" ")
			pri(Vals[0], Vals[1])
		elif Input[0] == "d" or Input[0] == "done":
			done(Input[1])
		elif Input[0] == "s" or Input[0] == "switch":
			Vals = Input[1].split(" ")
			switch(Vals[0], Vals[1])
		elif Input[0] == "f" or Input[0] == "filter":
			fliter(Input[1])
		elif Input[0] == "fp" or Input[0] == "filterpri":
			fliterpri(Input[1])					#special comands

def UpCACHE(LineNum, Cvar):
	LineNum = LineNum-1
	with open("CACHE.txt", 'r+') as UP:
		LineLenghts = []
		for Line in UP:
			LineLenghts.append((len(Line)+1))
		C = 0
		Cur = 0
		while C < LineNum:
			Cur = Cur+LineLenghts[C]
			C = C+1
		UP.seek(Cur)
		PrintLen = len(str(Cvar))
		Offset = 10 - PrintLen
		while Offset > 0:
			UP.write("0")
			Offset = Offset-1
		UP.write(str(Cvar))

def ReCACHE():
	global StartUpCount
	global ErrorCount
	global TaskCount
	StartUpCount = 0
	ErrorCount = 0
	TaskCount = 0
	UpCACHE(1, StartUpCount)
	UpCACHE(2, ErrorCount)
	UpCACHE(3, TaskCount)

# START of program - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

with open("CACHE.txt", "r+") as CACHE:
	CACHEList = []
	for Line in CACHE:
		CACHEList.append(Line[0:10])
	StartUpCount = int(CACHEList[0])
	ErrorCount = int(CACHEList[1])
	TaskCount = int(CACHEList[2])
	CACHEList = []#cache load

StartUpCount = StartUpCount+1	#Increment StartUpCount
UpCACHE(1, StartUpCount)		#Update Cache

if StartUpCount == 1:			#first startup only
	print("\nWELCOME to todo list it is your frst time using the program, so")
	print("we recomend reading the README file.")
	print("\nPress R and then ENTER to open the file, otherwise just press ENTER.")
	print("\nHope you enjoy the program :)")
	if input(":").upper() == "R":
		system("start README.txt")

load()
LOOP = 0			#keep inner loop going
while True:			#MAIN loop
	try:
		while LOOP == 0:	#inner loop
			save()			#save after each comand
			system("cls")
			post()			#update screen
			listen()		#wait for comand

		break

	except:
		ErrorCount = ErrorCount+1
		UpCACHE(2, ErrorCount)
		system("cls")
		print("\033[1;31;40m ")
		print("\t\t---------------------------------------")
		print("\t\t EEEEE   RRRRR   RRRRR   OOOOO   RRRRR")
		print("\t\t E       R   R   R   R   O   O   R   R")
		print("\t\t EEEEE   RRRRR   RRRRR   O   O   RRRRR")
		print("\t\t E       R R     R R     O   O   R R")
		print("\t\t EEEEE   R  R    R  R    OOOOO   R  R")
		print("\t\t---------------------------------------\n")
		print("\033[1;32;40m please check your syntax 0n the input")
		print("\033[1;31;40m ")
		if DevMode == 1:
			print_exc()
			print("\033[1;37;40m ")
			print("\033[1;37;40m ")
			print("try er command for external reset")
		else:
			print("to enter DevMode see line 6 of todo.py code")
		print("\033[1;37;40m ")
		print("If this presists, try closeing and reopening the program\n")
		print("press enter to do an internal reset")
		print("")
		input()
