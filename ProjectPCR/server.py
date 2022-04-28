# Les importations necessaires

from fileinput import close
from platform import release
import socket, threading
import math

# Mutex pour assurer l'exlusion mutuelle
bank_mutex=threading.Lock()

#Liste des actions autorisée par le serveur pour le client
actions_autorisees=[]
actions_autorisees.append("ConsulterCompte")
actions_autorisees.append("ConsulterTransaction")
actions_autorisees.append("ConsulterFacture")
actions_autorisees.append("Ajout")
actions_autorisees.append("Retrait")
current_threads=[]
msgsize=1024
facture="factures.txt"
compte="comptes.txt"
hist="histo.txt"


# Gestion des clients a travers les threads
class threadClients(threading.Thread):

    # Recuperer l'adresse et la socket du client connecté
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("nouvelle connexion est ajoutée: ", clientAddress)

    # Recuperer l'action autorisé pour le client connecté afin de l'excéuter
    def run(self):
        print ("connexion d'aprés : ", clientAddress)
        self.csocket.send(bytes("hello",'utf-8'))
        rsp = ''
        while True:
            try:
                data = self.csocket.recv(3072)          
            except socket.error as e:
                print("socket disconnectee !")
                break
            rsp = data.decode()
            if rsp!="Salut":
                print("communication d'aprés client necéssite une action:",rsp.split(",")[0])
                keyword=rsp.split(",")[0]
                if keyword in actions_autorisees:
                    NotificationServeur(clientAddress,rsp,self.csocket)
                elif rsp=='exit':
                    break
                else:
                    msg=" n'est pas reconnu comme une action !"
                    self.csocket.send(bytes(msg,'UTF-8'))

        print("client dont l'adresse est : ", clientAddress , " est deconnete ..")   
# fin de la classe



# Notifier a chaque fois le serveur de l'action effectuer par le(s) client(s) afin
# de poursuivre le process fait par chaque client

def NotificationServeur(ip,message,csock):
    elements=message.split(",")
    if elements[0] == "ConsulterCompte":
        msg=Consulter_Solde_Compte(elements[1])

        csock.send(bytes(msg,'UTF-8'))
    if elements[0] == "ConsulterTransaction":
        msg=Consulter_Transaction_Compte(elements[1])

        csock.send(bytes(msg,'UTF-8'))
    if elements[0] =="ConsulterFacture":
        msg=Consulter_Facture_Compte(elements[1])
        csock.send(bytes(msg,'UTF-8'))  
    if elements[0] == "Ajout":
        bank_mutex.acquire()
        if(Ajout(int(elements[1]),int(elements[2]))):
            
            msg="Ajout avec succes !"
            csock.send(bytes(msg,'UTF-8'))
        else:
            msg="reference invalide , verifiez !"
            csock.send(bytes(msg,'UTF-8'))
        bank_mutex.release()
    if elements[0] == "Retrait":
        bank_mutex.acquire()
        if(Retrait(int(elements[1]),int(elements[2]))):
            msg=" Retrait avec succes !"
            csock.send(bytes(msg,'UTF-8'))
        else:
            msg="Retrait echoue !!"
            csock.send(bytes(msg,'UTF-8'))          
        bank_mutex.release()


# Consulter les Details concernant un compte spécifique 

def Consulter_Solde_Compte(ref):
    comptes =open("comptes.txt",'r') 
    ligne_compte = comptes.readlines()
    for i in ligne_compte:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            sign = -1 if columns[2]=="Negative"  else 1
            comptes.close()
            msg="\nVotre solde est :{}".format(int(columns[1])*sign)   
            return  msg
    return "compte n'existe pas!"


# Suivre les transactions d'une reference bien précise 

def Consulter_Transaction_Compte(ref):
    response=""
    histo =open("histo.txt",'r') 
    hs_list_of_lines = histo.readlines()
    for i in hs_list_of_lines:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            response+="Transaction:\nType:{}   Valeur:{}   Resultat:{}   EtatCompteApresTransaction:{}\n".format(columns[1],columns[2],columns[3],columns[4])
    histo.close()
    if response=="":
        response="Pas de transactions faite avec cette reference"
    return response


# Parcourir le fichier Factures pour extraire le montant a payer au cas d'interet bancaire

def Consulter_Facture_Compte(ref):
    facture =open("factures.txt",'r') 
    fs_list_of_lines = facture.readlines()
    for i in fs_list_of_lines:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            return "la facture a payer est :"+columns[1]
    return "compte n'existe pas !"


# Verification de l'existance du compte au niveau du fichier comptes

def Verification_Compte_Existence(ref):
    comptes=open(compte,"r")
    ligne_compte = comptes.readlines()
    montantFacturee=0
    for i in range(len(ligne_compte)):
        columns=ligne_compte[i].split(',')
        if int(columns[0])==ref:
            return True
    return False


# Mise du factures aprés ajout ou retrait d'argent

def Maj_Factures(ref,Valeur):
    comptes=open(compte,"r")
    ligne_compte = comptes.readlines()
    montantFacturee=0
    for i in range(len(ligne_compte)):
        columns=ligne_compte[i].split(',')
        if int(columns[0])==ref:
            if(columns[2]=="Negative"):
                montantFacturee=Valeur*0.02
            else:
                montant=int(columns[1])
                if ((montant-Valeur)<0 ):
                    montantFacturee=-(montant-Valeur)*0.02
                    print("a facture is due")
                    break
                else:
                    break
    facture=open("factures.txt","r")
    ligne_facture = facture.readlines()

    for i in range(len(ligne_facture)):
        columns=ligne_facture[i].split(',')
        if columns[0]=="\n":
            break
        if int(columns[0])==ref:
            print("monatant facture :",montantFacturee)
            columns[1]=math.trunc(montantFacturee + int(columns[1]))
            if (i< len(ligne_facture)-1):
                ligne_facture[i]="{},{}\n".format(columns[0],columns[1])
                facture.close()
            else :
                ligne_facture[i]="{},{}\n".format(columns[0],columns[1])
                facture.close()
            break
    open('factures.txt', 'w').close()
    facture=open("factures.txt","a")
    for i in ligne_facture:
        facture.write(i)


# Retrait du montant desiré du compte en faisant la mise à jour necessaire au niveau des fichiers 
# et on respectant le plafont du débit précisé pour chaque compte

def Retrait(ref,montant):
    success=False
    estNegative=False
    if montant<0:
        print("vous nous pouvez pas retirez un montant negative ! ")
        return False
    if Verification_Compte_Existence(ref):
        comptes=open(compte,"r")
        ligne_compte = comptes.readlines()
        for i in range(len(ligne_compte)):
            columns=ligne_compte[i].split(',')
            if int(columns[0])==ref:
                if(columns[2]=="Negative"):
                    estNegative=True
                    
                    if (int(columns[1])+montant)<=int(columns[3]):
                        Maj_Factures(ref,montant)
                        columns[1]=int(columns[1])+montant
                        ligne_compte[i]="{},{},Negative,{}".format(columns[0],columns[1],columns[3])
                        comptes.close()
                        success=True
                        break

                        
                if(columns[2]=="Positive"):
                    if (int(columns[1])-montant)>0:
                        columns[1]=int(columns[1])-montant
                        ligne_compte[i]="{},{},Positive,{}".format(columns[0],columns[1],columns[3])
                        comptes.close()
                        success=True
                        break
                    elif abs(int(columns[1])-montant)<= int(columns[3]):
                        Maj_Factures(ref,montant)
                        ligne_compte[i]="{},{},Negative,{}".format(columns[0],abs(int(columns[1])-montant),columns[3])
                        comptes.close()
                        success=True
                        estNegative=True
                        break
        open('comptes.txt', 'w').close()  
        comptes=open(compte,"a")
        for i in ligne_compte:
            comptes.write(i)
        histo =open(hist,'a') 
        if success:
            if estNegative:
                histo.write("\n{},Retrait,{},Success,Negative".format(ref,montant))
            else:
                histo.write("\n{},Retrait,{},Success,Positive".format(ref,montant))
        else:
            if estNegative:
                histo.write("\n{},Retrait,{},Echec,Negative".format(ref,montant))
            else:
                histo.write("\n{},Retrait,{},Echec,Positive".format(ref,montant))
        histo.close()
        return success              
    else:
        return False


# Ajout du montant desiré au compte en faisant la mise à jour necessaire au niveau des fichiers 

def Ajout(ref,montant):
    if(Verification_Compte_Existence(ref)):
        fact=open(facture,"r") 
        # payer facture au cas d'intérêt bancaire
        ligne_facture=fact.readlines()
        fact.close()
        comptes=open(compte,"r")
        ligne_compte=comptes.readlines()
        comptes.close()
        histo=open(hist,"a")
        for i in range(len(ligne_facture)):
            columns=ligne_facture[i].split(',')
            if int(columns[0])==ref:
                if(int(columns[1])>=montant):
                    columns[1]=int(columns[1])-montant
                    montant=0
                    ligne_facture[i]="{},{}".format(columns[0],columns[1])
                else:
                    montant-=int(columns[1])
                    columns[1]=0
                    if(i!=len(ligne_facture)-1):
                        ligne_facture[i]="{},{}\n".format(columns[0],columns[1])
                    else:
                        ligne_facture[i]="{},{}".format(columns[0],columns[1])

                # Maj du compte apres transaction et payement facture
                for i in range(len(ligne_compte)):
                    columns=ligne_compte[i].split(',')
                    if int(columns[0])==ref:
                        if(columns[2]=="Negative"):
                            if  int(columns[1])>montant:
                                columns[1]= int(columns[1])-montant
                                ligne_compte[i]="{},{},{},{}".format(columns[0],columns[1],columns[2],columns[3])
                                histo.write("\n{},Ajout,{},Success,Negative".format(columns[0],montant)) 
                            else:
                                histo.write("\n{},Ajout,{},Success,Positive".format(columns[0],montant)) 
                                columns[1]= montant-int(columns[1])
                                ligne_compte[i]="{},{},{},{}".format(columns[0],columns[1],"Positive",columns[3])
                        else:
                            columns[1]= int(columns[1])+montant
                            histo.write("\n{},Ajout,{},Success,Positive".format(columns[0],montant)) 
                            ligne_compte[i]="{},{},{},{}".format(columns[0],columns[1],"Positive",columns[3])     
        histo.close()
        open(compte,'w').close()  
        open(facture,'w').close() 
        comptes=open(compte,"a")
        factures=open(facture,"a")
        for i in ligne_compte:
            comptes.write(i)        
        for i in ligne_facture:
            factures.write(i)
        comptes.close()
        factures.close() 
        return True
    else:
        return False       
        


             
LOCALHOST = "127.0.0.1"
PORT = 8084
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Serveur disponible")
print("En attente pour les requtes des clients..")
while True:
    # Boucle principale
    server.listen(1)
    clientsock, clientAddress = server.accept()
    # retourner le couple (socket,addresse)
    newthread = threadClients(clientAddress, clientsock)
    newthread.start()
    current_threads.append(newthread)

