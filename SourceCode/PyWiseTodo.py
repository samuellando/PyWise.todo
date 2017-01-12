from PyWiseFuncs import AllFunctions as pw
from os import system
from traceback import print_exc
from time import sleep

DevMode = 0 #set to 1 to get bug reports
File = "TodoTXT.txt" #chage flie name as needed
List = []
PriList = []
#CACHE variables
StartUpCount = 0 	#Stored on line 1
ErrorCount = 0 		#Stored on line 2
TaskCount = 0		#Stored on line 3
PriOneCode = "32"
PriTwoCode = "33"
PriThreeCode = "31"
PriZeroCode = "37"
ExportFile = "TodoList.txt"
CACHEFile = "CACHE.txt"

def listen(): #listen for a comand
	global LOOP
	global DevMode
	global PriList
	global List
	global File
	global PriOneCode
	global PriTwoCode
	global PriThreeCode
	global PriZeroCode
	global ExportFile
	global CACHEFile
	global TaskCount
	Input = input("~")
	if Input == "exit":
		LOOP = 1
	elif Input == "ba":
		List, PriList = pw.BulkAdd(List, PriList)
	elif Input == "bw":
		List, PriList = pw.BulkWork(File)
	elif Input == "sp":
		List, PriList = pw.SortPri(List, PriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, 0)
	elif Input == "sps":
		List, PriList = pw.SortPri(List, PriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, 1)
	elif Input == "sd":
		List, PriList = pw.SortDate(List, PriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, 0)
	elif Input == "sds":
		List, PriList = pw.SortDate(List, PriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode, 1)
	elif Input == "pd":
		List, PriList = pw.PriByDate(List, PriList)
	elif Input == "ex":
		pw.Export(List, PriList, ExportFile)
	elif Input == "te":
		File = pw.template()
		List, PriList = pw.load(File)
	elif Input == "colors":
		PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode = pw.color(CACHEFile, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)
	elif Input == "er" and DevMode == 1:		#DevMode only
		system("start PyWiseTodo.py")
		exit()
	elif Input == "rc" and DevMode == 1:		#DevMode only
		pw.ReCACHE(StartUpCount, ErrorCount, TaskCount, CACHEFile)
	elif Input == "h" or Input == "help":
		HT = open("HELP.txt", "r")
		system("cls")
		for Line in HT:
			Line = Line.replace("\n", "")
			sleep(0.05)
			print(Line)
		print(" ")
		print("Press any key to continue")
		input("")								#normal comands
	if "`" in Input:
		Input = Input.split("`")
		if len(Input) > 2:
			return
		if Input[0] == "a" or Input[0] == "add":
			List, PriList = pw.add(Input[1], List, PriList)
		elif Input[0] == "p" or Input[0] == "pri":
			Vals = Input[1].split(" ")
			PriList = pw.pri(Vals[0], Vals[1], PriList)
		elif Input[0] == "d" or Input[0] == "done":
			List, PriList = pw.done(Input[1], List, PriList)
			TaskCount = TaskCount+1
			pw.UpCACHE(3, TaskCount, CACHEFile)
		elif Input[0] == "s" or Input[0] == "switch":
			Vals = Input[1].split(" ")
			List, PriList = pw.switch(Vals[0], Vals[1], List, PriList)
		elif Input[0] == "f" or Input[0] == "filter":
			pw.FList, FPriList = pw.fliter(Input[1], List, PriList)
			pw.post(FList, FPriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)
			input("Press enter to return")
		elif Input[0] == "fp" or Input[0] == "filterpri":
			pw.FList, FPriList = fliterpri(Input[1], List, PriList)
			pw.post(FList, FPriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)
			input("Press enter to return")					#special comands
		elif Input[0] == "ed" or Input[0] == "edit":
			I = int(Input[1])
			I = I-1
			if I > len(List)-1 or I < 0:
				pass
			else:
				List[I] = pw.edit(List[I])
		elif Input[0] == "load":
			if ".txt" in Input[1]:
				print(" ")
			else:
				Input[1] = Input[1]+".txt"
				TList, TPriList = pw.load(Input[1])
				C = 0
				for Item in TList:
					List.append(TList[C])
					PriList.append(TPriList[C])
					C = C+1

StartUpCount, ErrorCount, TaskCount, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode = pw.LoadCACHE(CACHEFile)
PriOneCode = PriOneCode[8:]
PriTwoCode = PriTwoCode[8:]
PriThreeCode = PriThreeCode[8:]
PriZeroCode = PriZeroCode[8:]
StartUpCount = StartUpCount+1	#Increment StartUpCount
pw.UpCACHE(1, StartUpCount, CACHEFile)		#Update Cache

if StartUpCount == 1:			#first startup only
	print("\nWELCOME to todo list it is your frst time using the program, so")
	print("we recomend reading the README file.")
	print("\nPress R and then ENTER to open the file, otherwise just press ENTER.")
	print("\nHope you enjoy the program :)")
	if input(":").upper() == "R":
		system("start README.txt")

List, PriList = pw.load(File)

LOOP = 0			#keep inner loop going
while True:			#MAIN loop
	try:
		while LOOP == 0:	#inner loop
			pw.save(File, List, PriList)			#save after each comand
			system("cls")
			pw.post(List, PriList, PriOneCode, PriTwoCode, PriThreeCode, PriZeroCode)			#update screen
			if File != "TodoTXT.txt":
				print("editing template:"+File)
				print(" ")
			listen()		#wait for comand
		break

	except:
		ErrorCount = ErrorCount+1
		pw.UpCACHE(2, ErrorCount, CACHEFile)
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
			print("to enter DevMode see line 5 of PyWiseTodo.py code")
		print("\033[1;37;40m ")
		print("If this presists, try closeing and reopening the program\n")
		print("press enter to do an internal reset")
		print("")
		input()
