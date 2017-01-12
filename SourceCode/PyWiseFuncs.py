from time import sleep, strftime
from os import system, remove
from subprocess import Popen
from traceback import print_exc
from msvcrt import getch

class AllFunctions():
	def load(FileName): #Open text file and return todo list and pri list
		ToList = []
		State = open(FileName, "r")
		for Line in State:
			Line = Line.replace("\n", "")
			ToList.append(Line)
		PList = []
		TempList = []
		Lenght = len(ToList)
		C = 0
		while C < Lenght:
			CUT = ToList[C].split("PRI")
			TempList.append(CUT[0])
			PList.append(CUT[1])
			C = C+1
		ToList = []
		ToList = TempList
		return(ToList, PList)

	def save(FileName, ToList, PList): #Update text file to current lsit state
		remove(FileName)
		State = open(FileName, "a")
		C = 0
		for Item in ToList:
			State.write(ToList[C]+"PRI"+PList[C]+"\n")
			C = C+1

	def post(ToList, PList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode): #Post list to screen with colors
		system("cls")
		print(" ")
		print("\t"+"\t"+"\033[1;37;40m "+"\t--Todo List--")
		print(" ")
		C = 0
		Max = len(ToList)
		while C < Max:
			Coef = str(C+1)
			if PList[C] == "1":
				print("\t"+"\033[1;"+PriOneCode+";40m "+Coef+"\t"+ ToList[C])
			elif PList[C] == "2":
				print("\t"+"\033[1;"+PriTwoCode+";40m "+Coef+"\t"+ ToList[C])
			elif PList[C] == "3":
				print("\t"+"\033[1;"+PriThreeCode+";40m "+Coef+"\t"+ ToList[C])
			else:
				print("\t"+"\033[1;"+PriZeroCode+";40m "+Coef+"\t"+ToList[C])
			C = C+1
		print("\033[1;37;40m "+" ")
		if len(ToList) == 0:
			print("\t"+"\033[1;35;40m "+"\tNothing To Do !!")
			print("\033[1;37;40m "+" ")

	def add(Item, ToList, PList): #add item to list
		ToList.append(Item)
		PList.append("0")
		return(ToList, PList)

	def pri(Num, NP, PList): #chage pri of item in list
		Max = len(PList)
		C = int(Num)-1
		if C >= Max or C < 0:
			return
		if int(NP) > 3 or int(NP) < 0:
			return
		PList[C] = NP
		return(PList)

	def done(Num, ToList, PList): #remove item from list
		Max = len(ToList)
		C = int(Num)-1
		if C >= Max or C < 0:
			return
		del ToList[C]
		del PList[C]
		return(ToList, PList)

	def switch(NumO, NumT, ToList, PList): #witch position of two items in list
		CO = int(NumO)-1
		CT = int(NumT)-1
		Max = len(ToList)
		if CO >= Max or CT >= Max or CO < 0 or CT < 0:
			return
		TempVal = ""
		TempVal = ToList[CO]
		ToList[CO] = ToList[CT]
		ToList[CT] = TempVal
		TempVal = "0"
		TempVal = PList[CO]
		PList[CO] = PList[CT]
		PList[CT] = TempVal
		return(ToList, PList)

	def fliter(TEXT, ToList, PList): #filter by a search term
		FlitList = []
		FLP = []
		C = 0
		for Item in ToList:
			if TEXT in Item:
				FlitList.append(Item)
				FLP.append(PList[C])
			C = C+1
		return(FlitList, FLP)

	def fliterpri(Num, ToList, PList): #filter by a priority level
		FlitList = []
		FLP = []
		C = 0
		for Item in PList:
			if Num in Item:
				FlitList.append(ToList[C])
				FLP.append(Item)
			C = C+1
		return(FlitList, FLP)

	def BulkAdd(ToList, PList): #open text flie to bulk add items
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
				ToList, PList = AllFunctions.add(Line, ToList, PList)
			C = C+1
		Info.close()
		remove("BulkAdd.txt")
		return(ToList, PList)

	def BulkWork(FileName): #open text file to bulk edit items
		p = Popen(('notepad.exe', FileName))
		p.wait()
		ToList, PList = AllFunctions.load(FileName)
		return(ToList, PList)

	def SortPri(ToList, PList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, S): #buble sort by priority
		if S == 0:
			system("cls")
			print("Sorting...")
		Lenght = len(PList)
		Cur = 0
		C = 1
		while AllFunctions.OrderCheck(PList):
			while C < Lenght:
				if int(PList[Cur]) <= int(PList[(Cur+1)]):
					ToList, PList = AllFunctions.switch((Cur+1), (Cur+2), ToList, PList)
				Cur = Cur+1
				C = C+1
				if S == 1:
					AllFunctions.post(ToList, PList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)
					sleep(0.02)
			C = 1
			Cur = 0
		return(ToList, PList)

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

	def SortDate(ToList, PList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, S): #buble sort by date
		DateList = []
		for Item in ToList:
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
		Lenght = len(ToList)
		Cur = 0
		C = 1
		while AllFunctions.OrderCheck(DateList):
			while C < Lenght:
				if int(DateList[Cur]) <= int(DateList[(Cur+1)]):
					ToList, PList = AllFunctions.switch((Cur+1), (Cur+2), ToList, PList)
					temp = DateList[Cur]
					DateList[Cur] = DateList[(Cur+1)]
					DateList[(Cur+1)] = temp
				Cur = Cur+1
				C = C+1
				if S == 1:
					AllFunctions.post(ToList, PList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)
					sleep(0.02)
			C = 1
			Cur = 0
		ToList.reverse()
		PList.reverse()
		return(ToList, PList)

	def PriByDate(ToList, PList): #prooritiz by date
		DateList = []
		for Item in ToList:
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
		for Item in ToList:
			if DateList[C] <= TDate:
				PList[C] = "3"
			elif DateList[C] < (TDate+86400):
				PList[C] = "3"
			elif DateList[C] <= (TDate+172800):
				PList[C] = "2"
			elif DateList[C] <= (TDate+604800):
				PList[C] = "1"
			else:
				PList[C] = "0"
			C = C+1
		return(ToList, PList)

	def Export(ToList, PList, ToFile): #export and move using a bat file
		Ex = open(ToFile, "w")
		C = 0
		Ex.write("\t\t -- Todo -- \n")
		Ex.write("\n")
		for Item in ToList:
			Ex.write("PRI: "+PList[C]+"\t"+ToList[C]+"\n")
			C = C+1
		Ex.close()
		system("start MoveList.bat")

	def UpCACHE(LineNum, Cvar, ToFile):
		LineNum = LineNum-1
		with open(ToFile, 'r+') as UP:
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

	def ReCACHE(StartUpCount, ErrorCount, TaskCount, ToFile):
		StartUpCount = 0
		ErrorCount = 0
		TaskCount = 0
		AllFunctions.UpCACHE(1, StartUpCount, ToFile)
		AllFunctions.UpCACHE(2, ErrorCount, ToFile)
		AllFunctions.UpCACHE(3, TaskCount, ToFile)

	def LoadCACHE(ToFile):
		with open(ToFile, "r+") as CACHE:
			CACHEList = []
			for Line in CACHE:
				CACHEList.append(Line[0:10])
			StartUpCount = int(CACHEList[0])
			ErrorCount = int(CACHEList[1])
			TaskCount = int(CACHEList[2])
			PO = CACHEList[3]
			PTW = CACHEList[4]
			PTH = CACHEList[5]
			PZ = CACHEList[6]
			CACHEList = []
			return(StartUpCount, ErrorCount, TaskCount, PO, PTW, PTH, PZ)

	def edit(text):
		C = len(text)
		A = 0
		while True:
			system("cls")
			print(text[:C]+"|"+text[C:])
			Ent = getch()
			if Ent == b'\x08':
				if C > 0:
					C = C-1
					text = text[:C]+text[(C+1):]
			elif Ent == b'\r':
				system("cls")
				return(text)
			elif Ent == b'\xe0':
				A = 1
				print(A)
			elif Ent == b'K' and A == 1:
				if C > 0:
					A = 0
					C = C-1
				elif Ent == b'M' and A == 1:
					if C < len(text):
						A = 0
						C = C+1
				elif Ent == b'S' and A == 1:
					if C < len(text):
						A = 0
						text = text[:C]+text[(C+1):]
				elif A == 1:
					A = 0
					pass
				else:
					Ent = str(Ent)
					Ent = Ent[2:]
					Ent = Ent[:1]
					text = text[:C]+Ent+text[C:]
					C = C+1

	def template():
		system("cls")
		print(" ")
		print("Templates Menu")
		print(" ")
		print("T - Open template file")
		print("S - switch back to TodoTXT")
		print(" ")
		Input = input("Choose an option: ")
		if Input == "T" or Input == "t":
			FileName = input("Enter template file name: ")
			if ".txt" in FileName:
				pass
			else:
				FileName = FileName+".txt"
			FileCreate = open(FileName, "a")
			FileCreate.close()
			return(FileName)
		elif Input == "S" or Input == "s":
			return("TodoTXT.txt")

	def color(ToFile, Pone, Ptwo, Pthree, Pzero):
		system("cls")
		print(" ")
		print("chage color for priority 0, 1, 2, or 3 ?")
		print(" ")
		Ent = input(":")
		if Ent == "0":
			P = 0
		elif Ent == "1":
			P = 1
		elif Ent == "2":
			P = 2
		elif Ent == "3":
			P = 3
		else:
			return
		C = 0
		A = 0
		while True:
			system("cls")
			print(" ")
			print("\033[1;37;40m Pick a color, use the up down arrow keys")
			print(" ")
			if C == 0:
				print("\033[1;37;40m White")
			elif C == 1:
				print("\033[1;36;40m Cyan")
			elif C == 2:
				print("\033[1;35;40m Purple")
			elif C == 3:
				print("\033[1;34;40m Blue")
			elif C == 4:
				print("\033[1;33;40m Yellow")
			elif C == 5:
				print("\033[1;32;40m Green")
			elif C == 6:
				print("\033[1;31;40m Red")
			Ent = getch()
			if Ent == b'\r':
				system("cls")
				if C == 0:
					Col = 37
				elif C == 1:
					Col = 36
				elif C == 2:
					Col = 35
				elif C == 3:
					Col = 34
				elif C == 4:
					Col = 33
				elif C == 5:
					Col = 32
				elif C == 6:
					Col = 31
				if P == 0:
					AllFunctions.UpCACHE(7, Col, ToFile)
					return(Pone, Ptwo, Pthree, str(Col))
				elif P == 1:
					AllFunctions.UpCACHE(4, Col, ToFile)
					return(str(Col), Ptwo, Pthree, Pzero)
				elif P == 2:
					AllFunctions.UpCACHE(5, Col, ToFile)
					return(Pone, str(Col), Pthree, Pzero)
				elif P == 3:
					AllFunctions.UpCACHE(6, Col, ToFile)
					return(Pone, Ptwo, str(Col), Pzero)
			elif Ent == b'\xe0':
				A = 1
				print(A)
			elif Ent == b'P' and A == 1:
				A = 0
				if C > 0:
					C = C-1
				else:
					C = 6
			elif Ent == b'H' and A == 1:
				A = 0
				if C < 6:
					C = C+1
				else:
					C = 0
			else:
				A = 0
				pass
