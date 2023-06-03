import requests
import json
import os

node_script="""
from flask import Flask, request, send_file
from threading import Thread
import json 
import os
if not os.path.exists('files'):
    os.mkdir("files")
if not os.path.exists('home.html'):
    with open("home.html","w") as f:
        f.write("<html><head><title>StorageCluster</title></head><body><label>This is a generic storage cluster.</label></body></html>")
# create handler for each connection
app = Flask('')
global num
num = 0
global rqsts
rqsts = {}
@app.route('/')
def home():
    with open("home.html", "rb") as f:
      return f.read()#"/files/<file> [POST, GET, PATCH, DELETE] - access a file <br> /files [GET] - get a list of all the files stored"
def ext(path):
  return path.split(".")[1]
@app.route('/files', methods=['GET'])
def list():
    return json.dumps({"files": os.listdir("files/")})
@app.route('/files/<arg>', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def createlink(arg):
    if request.method == "GET":
        if not os.path.exists("files/" + arg):
            return "File not found", 404
        try:
            return send_file("files/" + arg)
        except:
            return "Internal server error", 500
    elif request.method == "POST":
        try:
            #err 500 if fail
            with open("files/" + arg, "wb") as f:
                f.write(request.data)
        except:
            return "Internal server error", 500
    elif request.method == "DELETE":
        if not os.path.exists("files/" + arg):
            return "File not found", 404
        try:
            os.remove("files/" + arg)
        except:
            return "Internal server error", 500
    elif request.method == "PATCH":
        if os.path.exists("files/" + arg):
            try:
                with open("files/" + arg, "wb") as f:
                    f.write(request.data)
            except:
                return "Internal server error", 500
        else:
            return 'File not found', 404
    return '', 200
def run():
  app.run(host='0.0.0.0', port=80)
run()
"""
"""The script that all storage nodes should use. Modifying the script or using a different scripts is likely to cause errors."""

mini_node_script="""
L='PATCH'
K='DELETE'
J='POST'
H='GET'
G='home.html'
F='files'
E=open
B='files/'
from flask import Flask,request as D,send_file as M
from threading import Thread
import json,os as A
if not A.path.exists(F):A.mkdir(F)
if not A.path.exists(G):
	with E(G,'w')as I:I.write('<html><head><title>StorageCluster</title></head><body><label>This is a generic storage cluster.</label></body></html>')
C=Flask('')
global N
N=0
global O
O={}
@C.route('/')
def Q():
	with E(G,'rb')as A:return A.read()
def R(path):return path.split('.')[1]
@C.route('/files',methods=[H])
def list():return json.dumps({F:A.listdir(B)})
@C.route('/files/<arg>',methods=[J,H,L,K])
def S(arg):
	I='File not found';F='Internal server error';C=arg
	if D.method==H:
		if not A.path.exists(B+C):return I,404
		try:return M(B+C)
		except:return F,500
	elif D.method==J:
		try:
			with E(B+C,'wb')as G:G.write(D.data)
		except:return F,500
	elif D.method==K:
		if not A.path.exists(B+C):return I,404
		try:A.remove(B+C)
		except:return F,500
	elif D.method==L:
		if A.path.exists(B+C):
			try:
				with E(B+C,'wb')as G:G.write(D.data)
			except:return F,500
		else:return I,404
	return'',200
def P():C.run(host='0.0.0.0',port=80)
P()
"""



clusters=[] #All files will be stored in a cluster node. 20 CDN nodes currently exist.
"""The node list. Supports an infinite number of nodes. Note: a single repl account can only host up to 20 nodes."""
index=[]
"""The list of files in all nodes."""
sizes=[]
"""The sizes of files in each node."""

#loads up the default nodes
def load_default_nodes():
    global clusters
    for i in range(20):
        clusters.append(f"https://cdnclust{i+1}.goglesquirmint1.repl.co")
        #index.append([])
        #sizes.append([])
"""Loads the goglesquirminton nodes."""

def split(path):
    # Normalize the path to handle different path separators
    normalized_path = os.path.normpath(path)
    
    # Split the path into its components
    components = normalized_path.split(os.sep)
    
    # Return the components as a list
    return components
"""Splits a path."""

def add_node(node_address):
    global clusters
    clusters.append(node_address)
    #index.append([])
    #sizes.append([])
    __save__()
"""Adds an existing node to the list without importing the file list from it."""

def load_nodes(log=True,*nodes):
    _int=[]
    if len(nodes) == 1:
        if isinstance(nodes[0],list):
            _int = nodes[0]
        else:
            _int = [nodes[0]]
    else:
        _int = nodes
    for i in _int:
        if not i in clusters:
            if log:
                print(f"- Importing node '{i}'")
            node=[]
            size=[]
            try:
                fl=requests.get(i+"/files").json()["files"]
                if log:
                    print(f" - Reading {len(fl)} files")
                for fn in fl:
                    if log:
                        print(f"  - Reading '{fn}'")
                    sz=len(requests.get(i+"/files/"+fn).content)
                    size.append(sz)
                    node.append(fn)
            except:
                if log:
                    print(f" - Error: could not import node {i} due to an error.")
            print("")
            clusters.append(i)
            sizes.append(size)
            index.append(node)
    if log:
        print("Finishing up..")
    __save__()
"""Adds existing node(s) to the list and imports the file lists from them."""

def __parse__(path):
    lp=os.path.normpath(path)
    return lp.replace(os.path.sep,"SPL-")#"SPL-".join(split(path))

def __deparse__(path):
    return path.replace("SPL-",os.path.sep)

def __save__():
    comb = {"index":index,"sizes":sizes}
    with open("nodeindex.json","w") as f:
        f.write(json.dumps(comb))

def __load__():
    global index
    global sizes
    with open("nodeindex.json","r") as f:
        comb=json.loads(f.read())
        index = comb["index"]
        sizes = comb["sizes"]
    #if len(clusters) > len(sizes):
    #    for i in range(len(clusters) - len(sizes)):
    #        sizes.append([])
    #        index.append([])
    #    __save__()
if not (os.path.exists("nodeindex.json")):
    __save__()
__load__()

def __index__(path):
    for i in range(len(index)):
        if path in index[i]:
            return i
    return -1

def __location__(path):
    clust=__index__(path)
    for i in range(len(index[clust])):
        if index[clust][i] == path:
            return clust, i
    return clust, -1

def __insert__(rawpath,length):
    cmax=1024*1024*1024*1024
    dex=-1
    for i in range(len(clusters)):
        t=0
        for size in sizes[i]:
            t+=size
        if t < cmax:
            cmax=t
            dex=i
    if dex != -1:
        index[dex].append(rawpath)
        sizes[dex].append(length)
        __save__()
    return dex #return index of the cluster

def join(path,*paths):
    return os.path.join(path,paths)
"""Joins two paths. os.path.join equivalent."""

def exists(path) :
    return __index__(__parse__(path)) != -1
"""Checks if a file exists across the nodes."""

def getsize(path):
    if not exists(path):
        return -1
    else:
        main, sub = __location__(__parse__(path))

        return sizes[main][sub]
"""Gets the size of a file."""

def read(path, create_file=False) -> bytes or str:
    if not exists(path):
        return None
    p=__parse__(path)
    idx=__index__(p)
    url=clusters[idx]+"/files/"+p
    d=requests.get(url).content
    if create_file:
        tfp="temp/temp."+path.split('.')[-1]
        with open(tfp,"wb") as f:
            f.write(d)
        return tfp
    else:
        return d
"""Reads the content of a file. If create_file is True, the function will create a temporary file and return the filepath."""

def write(path, data: str or bytes) -> None:
    if not exists(path):
        dex = __insert__(__parse__(path),len(data))
    else:
        dex = __index__(__parse__(path))
    url=clusters[dex]+"/files/"+__parse__(path)
    requests.post(url,data)
"""Writes a string or bytes to a file."""

def remove(path) -> None:
     if exists(path):
        p=__parse__(path)
        main,sub=__location__(p)
        url=clusters[__index__(p)]+"/files/"+p
        requests.delete(url)
        sizes[main].pop(sub)
        index[main].pop(sub)
       
"""Deletes a file."""

def move(source,dest) -> None:
    dat=read(source,False)
    remove(source)
    write(dest,dat)
    main,sub=__location__(__parse__(source))
    index[main].pop(sub)
    __insert__(__parse__(dest),len(dat))
"""Renames or moves a file. Expect this to be slow."""

def listdir(path):
    _ip = __parse__(path)
    matches=[]
    for c in index:
        for f in c:
            if f.startswith(_ip):
                dep=__deparse__(f.removeprefix(_ip))
                if dep.startswith(os.path.sep):
                    dep = dep.removeprefix(os.path.sep)
                matches.append(dep)
    return matches

def ping(index=-1) -> dict or bool:
    if index < 0:
        alive={}
        for i in clusters:
            f=requests.get(i+"/files").text
            if f.startswith("{") and f.endswith("}"):
                alive[i] = True 
            else:
                alive[i] = False
        return alive
    else:
        f=requests.get(clusters[index]+"/files").text
        if f.startswith("{") and f.endswith("}"):
                return True 
        else:
                return False
"""Pings every node and checks to see if it is awake. Use index -1 for pinging all clusters at once."""