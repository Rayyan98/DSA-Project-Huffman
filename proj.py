# Making Frequenc Dictionary From String
def make_frequency_dict(rawstr):
    frequency = {}
    for character in rawstr:
        if not character in frequency:
            frequency[character] = 1
        else:
            frequency[character] += 1
    return frequency

# Making String From File
def stringgen(file):
    string=''
    for character in file:
        # Adding chr(10) which is new line
        string=string+character+chr(10)
    return string[:-1]

# It is very obvious
def GetNodes(G):
    Nodes=[]
    for i in G.keys():
        Nodes.append(i)
    return Nodes

# Getting All the Nodes that have no parents
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

# Selection Sort to select Two minimum Elements
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
    rem=leng%7
    if rem==0:
        return string,0
    left=7-rem
    string="0"*left+string
    return string,left

def encoder(string):
    s=''
    tempstr=''
    for i in string:
        tempstr=tempstr+i
        if len(tempstr)==7:
            charcode=int(tempstr,2)
            char=chr(charcode)
            s = s+char
            tempstr=''
    return s

def masterencoder(filename):
    rawstr=stringgen(filename)
    charfreq=make_frequency_dict(rawstr)
    #print("char frequencies",charfreq)
    graph=Grapher(charfreq)
    #print("complete graph",graph)
    codes=assigncodes(graph)
    depth = maxleveler(codes)
    while depth%7 != 0:
        depth += 1
    protocol = ""
    for i in codes:
        j = codes[i]
        length = str(len(j))
        if len(length)==1:
            length  = "0" + length
        while len(j) != depth:
            j = "0"+j
        j = encoder(j)
        protocol += (i+j+length)
    #print(protocol)
    protocol += "}"
    protocol += "}"
    protocol += "}"
    # print("assigned codes",codes,"\n")
    encoded=replacer(rawstr,codes)
    encoded,left=completer(encoded)
    finalcode=encoder(encoded)
    write_file('compressed.txt',finalcode,protocol)
    return finalcode,left

def read_graph(filename):
    filename = open('compressed.txt','r')
    string = ""
    for i in filename:
        stop = ""
        for j in i:
            if j == "}":
                stop += j
            if j != "}" and len(stop) > 0:
                string += stop
                stop = ""
            if len(stop) == 0:
                string += j
            if stop == "}}}":
                break
        if stop == "}}}":
            break
    return decrypt_graph(string)
    
def decrypt_graph(string):
    graph = {}
    for i in range(0,len(string),5):
        graph[string[i]] = string[i+1:i+5]
    return graph


def write_file(name,text,protocol):
    file1 = open(name,"w+")
    for i in protocol:
        file1.write(i)
    for i in text:
        file1.write(i)
    file1.close()
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
sumi=sumi-1

fin=open('sample.txt')
l,lefty=masterencoder(fin)

# print("char in original file",sumi)
# a=(len(l))
# print("char in compressed file",a)
# print("percentage compression",(sumi-a)/sumi*100)
# print("max graph depth",maxlevel)

print(read_graph('compressed.txt'))
