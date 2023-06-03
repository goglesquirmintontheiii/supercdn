#CONFIG
MAX = 1 * 1024 * 1024 * 1024 #MAX; max storage each user gets
ML = 1 * 1024 * 1024 * 1024 #ML; max file size
TKB = 512 * 1024 * 1024 #TKB; Token bandwith; how much data can be POSTed using a token 
FN = "SuperCDN" #FN; flask app name
DIR = "CDNfiles" #DIR; directory for all SuperCDN files
TKLN = 50 #TKLN; Token length
CKLN = 100 #CKLN; Cookie length

from flask import Flask, Response, request, send_file
import json 
from time import sleep
import datetime
from datetime import timedelta
from pytz import timezone
import hashlib
import os
import random
import obfuscation
import jsmin
import shutil
import clusters
import threading

if __debug__:print("- [Running in debug mode] -")

nodel=[]
for i in range(20):
        nodel.append(f"https://cdnclust{i+1}.goglesquirmint1.repl.co")
for i in range(20):
        nodel.append(f"https://node{i+1}.goglestudiosalt.repl.co")
clusters.load_nodes(True,nodel)

#for n in nodel:
#    clusters.add_node(n)

app = Flask(FN)
app.config['MAX_CONTENT_LENGTH'] = ML
auth = {}

#clusters.write("beans.txt","Hi")
#clusters.write("CDNfiles/u1/u1beanis.txt","Hi")
#clusters.write("CDNfiles/u1/u1beanis2.txt","Hi")
#clusters.write("CDNfiles/u1/u1beanis3.txt","Hi")
#clusters.write("CDNfiles/u1/u1beanis4.txt","Hi")
#clusters.write("CDNfiles/u2/u2beanis.txt","Hi")
#clusters.write("CDNfiles/u2/u2beanis2.txt","Hi")
#clusters.write("CDNfiles/u2/u2beanis3.txt","Hi")
#clusters.write("CDNfiles/u2/u2beanis4.txt","Hi")
#print(clusters.listdir("CDNfiles/u2"))


def is_mobile(user_agent_string):
    # Common keywords used in mobile user agents
    mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone']

    for keyword in mobile_keywords:
        if keyword in user_agent_string:
            return True

    return False

user_agent_string = "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"


with open("adb.json","r") as f:
    auth=json.loads(f.read())

def genstring(ln):
    seed="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    o=""
    for i in range(ln):
        o+=seed[random.randint(0,len(seed)-1)]
    return o

def getsize(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            total_size += os.path.getsize(filepath)
    return total_size

def dellarg(directory):
    largest_file = None
    largest_file_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            file_size = os.path.getsize(filepath)
            if file_size > largest_file_size:
                largest_file = filepath
                largest_file_size = file_size
    os.remove(largest_file)

def scan(directory, limit):
    size = getsize(directory)
    if size > limit:
        dellarg(directory)
        scan(directory, limit)

#def obfuscate_js(js_code):
#    # Escape single quotes in the JavaScript code
#    js_code = js_code.replace("'", "\\'")

#    # Create an instance of the PyExecJS runtime
#    runtime = execjs.get()

#    # Define the obfuscation code
#    obfuscation_code = """
#    var obfuscator = require('javascript-obfuscator');
#    var result = obfuscator.obfuscate('{0}', {{
#      compact: true,
#      controlFlowFlattening: true
#    }});
#    result.getObfuscatedCode();
#    """.format(js_code)

#    # Evaluate the obfuscation code using the PyExecJS runtime
#    obfuscated_code = runtime.eval(obfuscation_code)

#    # Return the obfuscated code
#    return obfuscated_code

def buildjs(): #Auto obfuscate all JS
    for f_i in os.listdir("indevjs"):
        i=os.path.join("indevjs",f_i)
        with open(i,"r") as f:
            obf=jsmin.jsmin(f.read(), quote_chars="'\"`")
            #obf=obfuscation.obfuscate(f.read())#.read(), quote_chars="'\"`")#obf = obfuscate_js(f.read())
        with open(os.path.join("js",f_i),"w") as f:
            f.write(obf)

buildjs()

def hash(txt): #SHA256
    hash_object = hashlib.sha256(txt.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig

def saveauth():
    global auth
    with open("adb.json","w") as f:
        f.write(json.dumps(auth))
def mkauth(usr,pss,eml): #Make account
    global auth
    global DIR
    global MAX
    for i in auth.keys():
        if i == usr:
            return False
    auth[usr] = {"password": hash(pss), "cookies": [], "tokens": [], "capacity": MAX, "email": eml}
    with open("adb.json","w") as f:
        f.write(json.dumps(auth))
    os.mkdir(os.path.join(DIR,usr))
    return True

def login(mkc,*args): #Check cookie / check user+pass / make cookie
    #mck: whether to make a cookie or not; false to just verify login info or a cookie
    global auth
    global CKLN
    if len(args) == 2:
        #username, password
        pw=hash(args[1])
        for i in auth.keys():
            if auth[i]["password"] == pw and i == args[0]:
                if mkc:
                    cookie="WARNING_SHARING_THIS_WILL_LET_OTHERS_LOGIN_TO_YOUR_ACCOUNT_"+genstring(CKLN)
                    auth[i]["cookies"].append(cookie)
                    saveauth()
                    return cookie
                else:
                    return i
    elif len(args) == 1:
        #cookie
        return vck(args[0])
    return None

def vck(ck): #Verify cookie
    global auth
    for i in auth.keys():
        if ck in auth[i]["cookies"]:
            return i
    return None

def vtk(tk): #verify token
    global auth
    for i in auth.keys():
        for tkn in auth[i]["tokens"]:
            if tkn[1] > 0 and tkn[0] == tk:
                return i
    return None

def mtk(usr,pss): #make token
    global auth
    global TKLN
    global TKB
    for i in auth.keys():
        if i == usr:
            if hash(pss) == auth[i]["password"]:
                tkn = genstring(TKLN)
                auth[i]["tokens"].append([tkn,TKB])
                with open("adb.json","w") as f:
                    f.write(json.dumps(auth))
                return tkn
    return None

def modtk(tkn,amnt=0): #use or grab token info
    global auth
    for i in auth.keys():
        for tk in auth[i]["tokens"]:
            if tk[0] == tkn:
                tk[1] += amnt
                with open("adb.json","w") as f:
                    f.write(json.dumps(auth))
                return tk 
    return None

def gauth():
    global auth
    return auth

def log(data): #Log any data
        with open("log.txt","a") as f:
            f.write("\n")
            tz = timezone('EST')
            current_time = datetime.datetime.now(tz) + timedelta(hours=1)
            f.write(str(current_time)+": "+str(data))

@app.route('/')
def home():
    return send_file(os.path.join("html","index.html"))

@app.route('/api/register', methods=["POST"])
def registerapi():
    d=json.loads(request.data)
    for i in ["password","username","email"]:
        if not i in d.keys():
            return Response(f"Missing parameter {i}.",status=400)
    return str(mkauth(d["username"],d["password"],d["email"]))
@app.route('/api/login', methods=["POST"])
def loginapi():
    d=json.loads(request.data)
    for i in ["password","username"]:
        if not i in d.keys():
            return Response(f"Missing parameter {i}.",status=400)
    return str(login(True,d["username"],d["password"]))
@app.route('/login', methods=["GET"])
def loginpage():
    return send_file(os.path.join("html","login.html"))

@app.route('/register')
def registerpage():
    return send_file(os.path.join("html","register.html"))

@app.route('/files')
def filespage():
    return send_file(os.path.join("html","files.html"))

@app.route('/tos')
def tospage():
    return send_file(os.path.join("html","tos.html"))

@app.route('/developer')
def developerpage():
    return send_file(os.path.join("html","tokens.html"))

@app.route('/js/<rsn>')
def jsresource(rsn):
    user_agent_string = request.headers.get('User-Agent', '')
    mb=is_mobile(user_agent_string)
    if mb:
        mbp=rsn.split('.')[0]+"_mobile.js"
        mbfp=os.path.join("js",mbp)
        if os.path.exists(mbfp):
            return send_file(mbfp)

    if rsn=="rebuild":
      buildjs()
      return "JS rebuilt."
    if os.path.exists(os.path.join("js",rsn)):
        return send_file(os.path.join("js",rsn))
    else:
        return Response("The file was not found on the server.", status=404)

@app.route('/css/<rsn>')
def cssresource(rsn):
    user_agent_string = request.headers.get('User-Agent', '')
    mb=is_mobile(user_agent_string)
    if mb:
        mbp=rsn.split('.')[0]+"_mobile.css"
        mbfp=os.path.join("css",mbp)
        if os.path.exists(mbfp):
            return send_file(mbfp)
    if os.path.exists(os.path.join("css",rsn)):
        return send_file(os.path.join("css",rsn))
    else:
        return Response("The file was not found on the server.", status=404)

@app.route('/api/files', methods=["GET","POST","DELETE","PATCH"])
def fileop():
    global DIR
    global MAX
    if not "Authorization" in request.headers.keys():
        return Response(status=401)
    auth=request.headers["Authorization"]
    if auth.startswith("BEARER "):
        typ="Token"
        auth=auth.removeprefix("BEARER ")
    else:
        typ="Cookie"
    #auth = request.args.get('auth',None)
    fn = request.args.get('file',None)
    if fn == None or fn == "":
        return Response("Missing file parameter.",status=400)
    #typ = request.args.get('authtype',None) #Only acceptable values: Cookie,Token - this argument is optional
    if typ is None:
        typ = "Cookie"
    else:
        if not typ in ["Cookie","Token"]:
            fn = None
            auth = None
            #Set both to none to trigger 400 bad request ^^
    if auth == None:
        return Response("Missing auth header.",status=400)
    u="" #Username
    if typ == "Cookie":
        u=vck(auth)
    else:
        u=vtk(auth)
    if u is None:
        return Response(status=403)
    #Note: status=413 for payload too large
    dr = os.path.join(DIR,u) #User's directory
    fp=os.path.join(dr,fn) #Filepath
    if request.method == "POST":
        if typ == "Token":
            bth=modtk(auth)
            if bth < len(request.data):
                return Response("Not enough remaining bandwith.",status=413)
        try:
            clusters.write(fp,request.data)
            #with open(fp,"wb") as f:
            #    f.write(request.data)
        except:
            return Response("Couldn't write to the file.",status=500)
            #print("Couldn't write to the file.")
            #print(request.text)
        if typ == "Token":
            modtk(auth,-len(request.data))
        #scan(dr,gauth()[u]["capacity"])
        return "OK"
    if request.method == "GET":
        if fn=="filelist.index":
            fl=clusters.listdir(dr)
            otp=[]
            for i in fl:
                otp.append(f"{i},{clusters.getsize(os.path.join(dr,i))}")
            return "\n".join(otp)
        if os.path.exists(fp):
            tempf = clusters.read(fp,True)
            return send_file(tempf, as_attachment=True, download_name=fp.split(os.path.sep)[-1])
        else:
            return Response(status=404)
    if request.method == "DELETE":
        if os.path.exists(fp):
            try:
                clusters.remove(fp)
                return "OK"
            except:
                return Response("The file was not found on the server.", status=404)
        else:
            return Response("The file was not found on the server.", status=404)
    if request.method == "PATCH":
        fn2=request.args.get('dest',None)
        if os.path.exists(fp):
            clusters.move(fp,os.path.join(dr,fn2))
            return "OK"

@app.route("/api/verify")
def checkauthreq():
    if not "Authorization" in request.headers.keys():
        return Response(status=401)
    auth=request.headers["Authorization"]
    if auth.startswith("BEARER "):
        typ="Token"
        auth=auth.removeprefix("BEARER ")
        res=str(vtk(auth))
    else:
        typ="Cookie"
        res=str(vck(auth))
    return res

def pingsingle(idx):
    active = clusters.ping(idx)
    if not active:
        log(f"cluster {idx} was found offline.")

def pingthread():
    while True:
        print("Pinging nodes..")
        clusters.ping()
        sleep(120)
threading.Thread(target=pingthread).start()
log("Starting flask app..")
app.run("0.0.0.0",8080)