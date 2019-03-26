import csv 
import operator
in_file=str(input("Input File Name:"))
out_file=str(input("Output File Name:"))

solution={}

def outputSolution(solution):
    global out_file
    slot_duplicate = {}
    finalOutput = []
    for sub, tSlot in solution.items():
        if tSlot not in slot_duplicate:
            slot_duplicate[tSlot] = 1
        else:
            slot_duplicate[tSlot] += 1
    with open(out_file, 'w') as csvfile:
        fieldnames = ['SUBJECT', 'TIME_SLOT', 'ROOM']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for sub in solution.keys():
            finalOutput.append([sub[0], solution[sub], "R"+str(slot_duplicate[solution[sub]])])
            writer.writerow({'SUBJECT': sub[0], 'TIME_SLOT': solution[sub], 'ROOM': "R"+str(slot_duplicate[solution[sub]])})
            slot_duplicate[solution[sub]] -= 1
    print(finalOutput)
    return finalOutput

#select the most constartint variable returns variable,cost and its option
def selectMostConstrainedVar(valAssignment,csp):
   unassigned=[]
   for sub in valAssignment:
    if(valAssignment[sub]=="Null"): 
        unassigned.append(sub[0])
   mostConstrained=[]
   minm=float("inf")
   for sub in unassigned:
     if(len(csp[sub])-1<minm):
        mostConstrained[::]=[]
        minm=len(csp[sub])-1
        mostConstrained.append(sub)
     elif(len(csp[sub])-1==minm):
        mostConstrained.append(sub)
   levels={}
   ## understand
   for sub in mostConstrained:
     level=0
     opt=0
     for k1 in range(1,len(csp[sub])):
        for k2 in csp.keys():
         if sub!=k2:
             for k3 in range(1,len(csp[k2])):
                if(csp[sub][k1]==csp[k2][k3]):
                    if(csp[sub][0]=="o" and csp[k2][0]=='o'):
                       level+=1
                       opt+=1
                    else:
                        level+=2
     levels[sub]=(level,opt)
   minm = (-float('inf'),float('inf'))
   mostConstrainedval=''
   for sub in levels.keys():
       if(levels[sub][0]>minm[0]):
           mostConstrainedval=sub
           minm=(levels[sub][0],levels[sub][1])
       elif(levels[sub][0]==minm[0] and levels[sub][1]<minm[1]):
           mostConstrainedval=sub
           minm=(levels[sub][0],levels[sub][1])
   return mostConstrainedval

#returns the least constraining value
def  leastConstraintVal(sub,csp):
    timeslots=csp[sub][1::]
    levels={}
    for slot in timeslots:
     level=0
     for k1 in csp:
        for k2 in range (1,len(csp[k1])):
          if(slot==csp[k1][k2]):
              if(csp[k1][0]=='o' and csp[sub][0]=='o' and k1!=sub):
                  level+=1
              elif(k1!=sub):
                  level+=2
     levels[slot]=level
    levels=sorted(levels.items(),key=operator.itemgetter(1))
    leastOrdered=[]
    for i in range(len(levels)):
       leastOrdered.append(levels[i][0])
    return leastOrdered


def checkConsistancy(slot, valAssignment,rooms):
    if slot not in valAssignment.values():
        return True
    elif slot in valAssignment.values():
        count = 0
        for sub, tSlot in valAssignment.items():    
            if (tSlot == slot) and (sub[1] == "o"):
                count += 1
        if (count > 0) and (count < rooms):
            return True
        else:
            return False  
def isComplete(valAssignment):
    if('Null' in valAssignment.values()):
        return False
    else:
        return True

def recursiveBackTrack(valAssignment,csp,rooms):
    global solution
    if(isComplete(valAssignment)):
        solution=valAssignment
        return valAssignment
    else:
     var=selectMostConstrainedVar(valAssignment,csp)
     for slot in leastConstraintVal(var,csp):
        if(checkConsistancy(slot,valAssignment,rooms)):
             valAssignment[(var,csp[var][0])]=slot
             if csp[var][0] == "c":
               for k in csp.keys():
                if (slot in csp[k]):
                 csp[k].remove(slot)
             if (recursiveBackTrack(valAssignment, csp,rooms)):
                    return True
             else:
                valAssignment[(var, csp[var][0])] = "Null"   

    return False  


def backTrack(csp,rooms):
    valAssignment={}
    for sub in csp:
       valAssignment[(sub,csp[sub][0])]="Null"
    if(recursiveBackTrack(valAssignment, csp,rooms) == True):
        outputSolution(solution)
    else:
        print ("no result found")
        with open('output.csv', 'w') as csvfile:
            fieldnames = ['no result found']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


def FormProblem(in_file):
    var_val=[]
    val2=[]
    csp={}
    with open(in_file,newline='') as problem:
     data=csv.reader(problem,delimiter='\t')
     for row in data:
         var_val.append(list(filter(None,row[0].split(','))))
    val2=var_val.pop()
    for i in range(len(var_val)):
     csp[var_val[i][0]] =var_val[i][1::]
    backTrack(csp,len(val2))
FormProblem(in_file)








     
    






