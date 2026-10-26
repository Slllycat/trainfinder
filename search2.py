import os,copy
files=["traindata.txt"]
time="23:43"    #when to go
day="Samstag"          #Mo-R
ort1="Prinzersdorf"          #from where
ort2="Amstetten"          #where to go
#Bahnhof doesnt always need to be included

def firstelin(l,s):
    for i in l:
        if i[0]==s:
            return True
    return False

def timeinsec(t):
    a=t.split(":")
    a=int(a[0])*60+int(a[1])
    return a

def gettime(time,searcht):
    if time=="x":
        return "x"
    time=timeinsec(time)
    searcht=timeinsec(searcht)
    return time-searcht

def err(word,orte):
    for i in range(len(word),0,-1):
        tmp2=[]
        for i2 in orte:
            if word[:i] in i2:
                tmp2.append(i2)
        if tmp2:
            return "\n".join(tmp2)


def getunique(l,t): # l is : [abfahrt,ankunf,dest]
    bestdict={}
    for i in l:
        if i[0]>=t:
            if i[2] not in bestdict or i[0]<bestdict[i[2]][0]:
                bestdict[i[2]]=i
    return list(bestdict.values())

def loadtext(file):
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, file)
    thefile = open(path, "r",encoding="utf-8")
    all_lines = thefile.readlines()
    thefile.close()
    text=""
    for i in all_lines:
        text+=i
    return text

def gettraindata(files):
    data=[]
    tmp2={}
    orte=[]
    for file in files:
        tmp=loadtext(file)
        ind=0
        for i in tmp.split("\n")[2:]:
            try:
                if i!="":
                    if "#" in i:
                        data.append(tmp2)
                        tmp2={}
                        tmp2["train"]=i[1:].split(",")[0]
                        tmp2["days"]=i[1:].split(",")[1]
                        tmp2["day"]=""
                        tmp2["halte"]=[]
                    else:
                        i=i.split(",")
                        if tmp2["day"]=="":
                            tmp2["day"]=i[2]
                        tmp2["halte"].append([i[1],i[3],i[4],i[5]])
                        if i[4] not in orte:
                            orte.append(i[4])
                    ind+=1
            except:
                print(ind)
                exit()
        if tmp2:
            data.append(tmp2)
    return data[1:],sorted(orte)

def anfrage(data,orte,time,day,start,end):
    week={
        "täglich":["montag","dienstag","mittwoch","donnerstag","freitag","samstag","sonntag"],
        "Mo-Sa":["montag","dienstag","mittwoch","donnerstag","freitag","samstag"],
        "Mo-Fr":["montag","dienstag","mittwoch","donnerstag","freitag"],
        "Mo-Do":["montag","dienstag","mittwoch","donnerstag"],
        "Sa-So":["samstag","sonntag"],
        "Mo":["montag"],
        "Di":["dienstag"],
        "Mi":["mittwoch"],
        "Do":["donnerstag"],
        "Fr":["freitag"],
        "Sa":["samstag"],
        "So":["sonntag"]
        }
    if not start in orte:
        if start+" Bahnhof" in orte:
            start+=" Bahnhof"
        else:
            print("\nStart might be:\n"+err(start,orte))
            return ""
    if not end in orte:
        if end+" Bahnhof" in orte:
            end+=" Bahnhof"
        else:
            print("\nEnd might be:\n"+err(end,orte))
            return ""
    data2=[]#every train after search and time in sec after search
    for i in data:
        if day.lower() in week[i["days"]]:
            tmp=copy.deepcopy(i)
            for i in range(len(tmp["halte"])):
                tmp["halte"][i][0]=gettime(tmp["halte"][i][0],time)
                tmp["halte"][i][1]=gettime(tmp["halte"][i][1],time)
            data2.append(tmp)
    data3={}
    for i in orte:
        data3[i]=[]
    for i in range(len(data2)):
        a=data2[i]
        for i in a["halte"]:
            if i[0]=="x":
                prevt=i[1]
                prevo=i[2]
            elif i[0]>0:
                data3[prevo].append([prevt,i[0],i[2]])
                prevt=i[1]
                prevo=i[2]
    test=[
        [["hi",0],["hi",0],["hi",0]],
        [["blh",0],["hi",0]]
    ]
    data4=[[[start,0]]]
    b=[]
    btime=999999999
    mintime=0
    ends=[]
    iii=0
    while mintime<btime:
        data4.sort(key=lambda x:x[-1][1])
        tmp=data3[data4[0][-1][0]]
        tmp=getunique(tmp,data4[0][-1][1])
        ttt=0
        for i in tmp:
            if not firstelin(data4[0],i[2]):
                ttt+=1
                if i[2]==end:
                    b.append(data4[0]+[[i[2],i[1]]])
                    btime=i[1]
                else:
                    data4.append(data4[0]+[[i[2],i[1]]])
        if ttt==0:ends.append(data4[0]+[[i[2],i[1]]])
        data4.pop(0)
        if len(data4)==0:
            break
        iii+=1
        mintime=min([i[-1][1] for i in data4])
    print(b)
    print(btime)


data,orte=gettraindata(files)
print("loading")
answer=anfrage(data,orte,time,day,ort1,ort2)
print(answer)