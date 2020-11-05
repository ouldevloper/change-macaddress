import os 
import re
import sys
import random
import subprocess

class changeMacAddress:
    def __init__(self,args):
        self.args=args
        self.allowedSymbols="0123456789ABCDEF"
        self.roles=["--mac","--random","--iface"]
        self.supportedPlatforms=["linux","linux2","darwin"]
        self.errors=[]
        self.parsedArgs={"iface":"","mac":""}
        self.run()
        

    def run(self):
        self.detectOs()
        self.hasRootPrivilege()
        self.parseArgs()
        

        if len(self.errors)==0:
            self.changeMacAddress()
            return

        else:
            os.system("clear")
            print(f"Usage: sudo {sys.argv[0]} --iface=<Network Interface> < --mac=<Mac address> or --random=True >")
            for i in self.errors:
                print(f"[x] {i}")

    def detectOs(self):
        self.errors.append("Os not supported") if sys.platform not in self.supportedPlatforms else ""

    def parseArgs(self):
        if len(sys.argv)>2:
            try:
                for index,arg in enumerate(self.args):                    
                    if index>0:
                        p=arg.split("=")

                        if p[0] not in self.roles:
                            self.usage()

                        elif p[0]=="--random":
                            self.randomMacAddress()

                        elif p[0]=="--mac":
                            self.parsedArgs["mac"]=p[1]

                        else:
                            self.parsedArgs[p[0][2:]]=p[1]
        
            except Exception as er:
                self.usage()
        else:
            self.usage()
        self.parseMacAddress()

    def parseMacAddress(self):
        if self.isValideMAc():
            mac=""
            str=self.parsedArgs["mac"]
            for i in range(0,len(str),2):
                mac+=str[i:i+2]+":"
            self.parsedArgs['mac']=mac.strip(":")
        else:
            self.errors.append("mac addrress not valid .")
    
    def isValideMAc(self):
        r=re.compile("^[\dABCDEFabcdef]{12}$")
        return True if r.match(self.parsedArgs['mac']) is not None else False

    def hasRootPrivilege(self):
        self.errors.append("use script as root .") if os.getuid()!=0 else ''

    def randomMacAddress(self):
        self.parseArgs["mac"]=''.join(random.choice(self.allowedSymbols) for i in range(12))

    def changeMacAddress(self):
        try:
            os.system(f"sudo ifconfig {self.parsedArgs['iface']} down")
            os.system(f"sudo ifconfig {self.parsedArgs['iface']} hw ether {self.parsedArgs['mac']}")
            os.system(f"sudo ifconfig {self.parsedArgs['iface']} up")
            print("Mac Changed Successfully")
        except Exception as er:
            print("Error Could Not Change The Mac Address")     
  
    def usage(self):
        os.system("clear")
        usage="""

        """
        print(f"Usage: sudo {sys.argv[0]} --iface=<Network Interface> < --mac=<Mac address> or --random=True >")
        print("--iface  --> Interface")
        print("--mac    --> Mac Address")
        print("--random --> Generate Mac Address Randomly")
        print("PS: Use only one argument --mac or --random")
        
changeMacAddress(sys.argv)