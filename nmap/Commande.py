import subprocess

class Commande():
    def __init__(self, db):
        self.db = db
        self.resetData()
        self.startDb()
        self.listingPort=False

    def start(self):
        proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            self.parse(str(line.decode()))

    def resetData(self):
        self.data = {"nom":"", "mac":"", "ip":"", "nomMac":"", "os_sure":1000, "type":"", "os":"", "ports":""}

    def sanitizeData(self):
        for k in self.data.keys():
            self.data[k] = str(self.data[k]).replace("'", "").strip(";")

    def startDb(self):
        self.ip, self.date = self.db.getSession()
        self.id = self.db.execu("INSERT INTO nmapData(ip, date) VALUES ('"+self.ip+"', '"+str(self.date)+"')", insertId=True)


class CommandeRapide(Commande):
    def __init__(self, cmd="nmap -sn %ip%/24", ip="192.168.0.2/24", db=None):
        Commande.__init__(self, db)
        if ip:
            self.ip = ip
        self.cmd = cmd.replace("%ip%", self.ip)

    def parse(self, line):
        if line.startswith("Nmap scan report"):
            try :
                try:
                    self.insertData()
                    self.resetData()
                except Exception as e : print("Impossible d'inserer les resultats : "+str(e))
                self.data["ip"] = line.strip().split(" ")[-1].strip("(").strip(")")
                self.data["nom"]
            except Exception as e:
                print ("Impossible de lire l'IP de la ligne : "+line+"\n")
                raise e

        if line.startswith("MAC"):
            try :
                self.data["mac"] = line.split(" ")[2]
                self.data["nomMac"] = line.split("(")[1].split(")")[0]

            except: print("Impossible de parser la MAC : "+line)


    def insertData(self):
        self.sanitizeData()
        if self.data["ip"] == "": return
        stri="INSERT INTO ip(data, nomMac, nom, mac, ip)" \
             " VALUES ("+str(self.id)+", '"+self.data["nomMac"]+"', '"+self.data["nom"]+"', '"+self.data["mac"]+"', '"+self.data["ip"]+"')"
        print(stri)
        self.db.execu(stri)

class CommandeComplete(Commande):
    def __init__(self, cmd="nmap -O -sS %ip%/24", ip="192.168.0.2/24", db=None):
        Commande.__init__(self, db)
        if ip:
            self.ip = ip
        self.cmd = cmd.replace("%ip%", self.ip)

    def insertData(self): # the insertion add to the current datas based on the ip
        self.sanitizeData()
        if self.data["ip"] == "": return
        stri="UPDATE ip SET ports='"+self.data["ports"]+"', nom='"+self.data["nom"]+"', os='"+self.data["os"]+"', os_sure="+self.data["os_sure"]+", type='"+self.data["type"]+"' WHERE ip = '"+self.data["ip"]+"' AND DATA = "+str(self.id-1)
        print(stri)
        self.db.execu(stri)

    def parse(self, line):
        print(line)

        if self.listingPort:# if were listing ports, we check if its still listing them, in wich case we add tehm
            if "/" in line.split(" ")[0]:
                if "open" in line:
                    self.data["ports"]+=line.split(" ")[0]+";"
            else:
                self.listingPort = False
        if line.startswith("PORT"):
            self.listingPort=True
        if line.startswith("Nmap scan report"): #if its the firt line of a report, we set the ip in which were working on
            self.insertData()
            self.resetData()
            self.data["ip"] = line.strip().split(" ")[-1].strip("(").strip(")")
            self.data["nom"] = line.split("for ")[1].split("(")[0]
        if line.startswith("Device type"):
            self.data["type"] = line.split(": ")[-1]
        if line.startswith("Running (JUST"):
            self.data["os"] = line.split(":")[1].split(" (")[0]
            self.data["os_sure"] = 2
        if line.startswith("OS details:"):
            self.data["os_sure"] = 0
            self.data["os"] = line.split(":")[1]


