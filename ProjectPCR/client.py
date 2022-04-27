# les importations
import os
import socket
clear = lambda: os.system('cls')


#les actions autorisées par le serveur pour chaque client

# 1- 
def consulterCompte(client):
  clear()
  print("Entrez la reference du compte pour consulter le compte :",end="")
  ref=input()
  client.sendall(bytes("ConsulterCompte,{}".format(ref),'UTF-8'))  

# 2-
def consulterTransaction(client):
  clear()
  print("Entrez la reference du compte pour consulter transaction :")
  ref=input()
  client.sendall(bytes("ConsulterTransaction,{}".format(ref),'UTF-8'))  

# 3-
def consulterFacture(client):
  clear()
  print("Entrez la reference du compte pour consulter facture :")
  ref=input()
  client.sendall(bytes("ConsulterFacture,{}".format(ref),'UTF-8'))  


# une des actions effectue par le client : transaction qui présente l'ajout et la retrait d'argent du compte 
# en faisant les mise a jour necessaires 

def transactionCompte():
  clear()
  print("1- faire un ajout d'argent ")
  print("2- faire un retrait d'argent")
  print("3- quitter")
  rsp=input()
  while(int(rsp) not in [1,2,3]):
    print("Votre choix est invalide , essayez de nouveau [1,2,3] !")
    rsp=input()
  msg=""
  if int(rsp)==1:
    print("entrez votre code reference")
    ref=input()
    print("entrez le monatnt à ajouter")
    montant=input()
    msg="Ajout,{},{}".format(ref,montant)
    client.sendall(bytes(msg,'UTF-8'))  

  if int(rsp)==2:
    print("entrez votre code reference")
    ref=input()
    print("entrez le monatnt à retirer")
    montant=input()
    msg="Retrait,{},{}".format(ref,montant)
    client.sendall(bytes(msg,'UTF-8'))  

  if int(rsp)==3:
    actionClient(client)


# actions effectuees pour un client 

def actionClient(client):
  clear()
  response=0
  print("1- consulter le solde du compte")
  print("2- consulter l'historique du transaction")
  print("3- consulter la facture à payer")
  print("4- etablir une trasaction")
  print("choix d'action :",end="")
  response=input()
  while int(response)not in [1,2,3,4]:
    print("Votre choix est invalide , essayez de nouveau [1,2,3,4] !")
    response=input()
  if(int(response) ==1):
    consulterCompte(client)
  if(int(response) ==2):
    consulterTransaction(client)
  if(int(response) ==3):
    consulterFacture(client)
  if(int(response) ==4):
    transactionCompte()




# le type du socket : SOCK_STREAM pour le protocole TCP
# le type du socket : SOCK_DGRAM pour le protocole UDP

SERVER = "127.0.0.1"
PORT = 8084
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("Salut",'UTF-8'))
in_data =  client.recv(30720)
while True:

  actionClient(client) 
  in_data =  client.recv(5072)
  if(in_data.decode()!="Salut"):
    clear()
    print("From Server :" ,in_data.decode())
    input("Press Enter to continue...")
  
  if(in_data.decode()=="exit"):

    break
client.close()