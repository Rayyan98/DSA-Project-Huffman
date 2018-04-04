def make_frequency_dict(rawstr):
    frequency = {}
    for character in rawstr:
        if not character in frequency:
            frequency[character] = 1
        else:
            frequency[character] += 1
    return frequency

def stringgen(file):
    string=''
    for character in file:
        string=string+character+chr(10)
    return string[:-1]
    
def GetNodes(G):
    Nodes=[]
    for i in G.keys():
        Nodes.append(i)
    return Nodes

def heapTops(G):
    Nodes=GetNodes(G)
    tops=[]
    for i in Nodes:
        check=False
        for j in G.values():
            if i in j:
                check=True
                break
        if not check:
            tops.append(i)
    return tops
    
def Truecount(sub,G):
    if sub in G:
        return G[sub]
    else:
        return sub

def min2(lis,G):
    for i in range(min(2,len(lis))):
        mini=i
        for j in range(i+1,len(lis)):
            if Truecount(lis[j],G)<Truecount(lis[mini],G):
                mini=j
        lis[mini],lis[i]=lis[i],lis[mini]
    return lis

def Grapher(G):
    BigG={}
    lis=GetNodes(G)
    for i in lis:
        BigG[i]=[]
    biglis=heapTops(BigG)
    count=0
    while len(biglis)>1:
        min2(biglis,G)
        val1,val2=biglis[0],biglis[1]
        nodename='alp'+str(count)
        count+=1
        sumi=Truecount(val1,G)+Truecount(val2,G)
        G[nodename]=sumi
        BigG[nodename]=[val1,val2]
        biglis.pop(0)
        biglis.pop(0)
        biglis=heapTops(BigG)
    return BigG

def mothernode(G):
    lis=heapTops(G)
    return lis[0]
    
def assigncodes(G):
    leaf=[]
    codes={}
    for i in G:
        if not G[i]:
            leaf.append(i)
    for i in leaf:
        codes[i]=''
    path=[mothernode(G)]
    visited=[mothernode(G)]
    string=''
    while path:
        top=path[-1]
        neigh=G[top]
        check=False
        for i in range(len(neigh)):
            if neigh[i] not in visited:
                path.append(neigh[i])
                visited.append(neigh[i])
                check=True
                if i==0:
                    string=string+'0'
                elif i==1:
                    string=string+'1'
                break
        if not check:
            ntop=path.pop()
            if not G[ntop]:
                codes[ntop]=string
            string=string[:-1]
    return codes

def replacer(fil,codes):
    string=''
    for i in fil:
        string=string+codes[i]
    return string

def completer(string):
    leng=len(string)
    left=8-leng%8
    string="0"*left+string
    return string,left

def encoder(string):
    s=''
    tempstr=''
    for i in string:
        tempstr=tempstr+i
        if len(tempstr)==8:
            charcode=int(tempstr,2)
            char=chr(charcode)
            s = s+char
            tempstr=''
    return s

def masterencoder(filename):
    rawstr=stringgen(filename)
    charfreq=make_frequency_dict(rawstr)
    print("char frequencies",charfreq)
    graph=Grapher(charfreq)
    print("complete graph",graph)
    codes=assigncodes(graph)
    maxleveler(codes)
    print("assigned codes",codes,"\n")
    encoded=replacer(rawstr,codes)
    encoded,left=completer(encoded)
    finalcode=encoder(encoded)
    return finalcode

def maxleveler(codes):
    global maxlevel
    maxl=0
    for i in codes.values():
        if len(i)>maxl:
            maxl=len(i)
    maxlevel=maxl
    return maxl

maxlevel=1

bini=open('sample.txt')
sumi=0
for i in bini:
    sumi = sumi + len(i)+1
fin=open('sample.txt')
l=masterencoder(fin)

print("char in original file",sumi)
a=(len(l))
print("char in compressed file",a)
print("percentage compression",(sumi-a)/sumi*100)
print("max graph depth",maxlevel)