from iota import Address, ProposedTransaction, Tag, Iota, TryteString
import time
import pandas as pd
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def make_pd(path, api, address):
 oldest = min(os.listdir(path), key=lambda f: os.path.getctime("{}/{}".format(path,f)))
 path1=path+'/'+oldest
 db = open(path1,'r')
 data =db.read()
 db.close()
 data_dict=dict(eval(data))

 for key in data_dict.keys():
  for value in data_dict.values():
   for i in range(len(value)):
    data_dict[key][i]=float(data_dict[key][i])
 data_df=pd.DataFrame(data_dict)
 data_summary=data_df.describe([])
 data_sent=[
 ["CLIENTE A:","I(A)mean:"+str(data_summary.iloc[1,0].round(3)),"V(V):"+str(data_summary.iloc[1,13].round(3)),"P(W)mean:"+str(data_summary.iloc[1,6].round(3$
 ["CLIENTE B:","I(A)mean:"+str(data_summary.iloc[1,1].round(3)),"V(V):"+str(data_summary.iloc[1,14].round(3)),"P(W)mean:"+str(data_summary.iloc[1,7].round(3$
 ["CLIENTE C:","I(A)mean:"+str(data_summary.iloc[1,2].round(3)),"V(V):"+str(data_summary.iloc[1,15].round(3)),"P(W)mean:"+str(data_summary.iloc[1,8].round(3$
 ]
 send_iota(data_sent, data_summary, api, address)
 os.remove(path1)

def send_iota(data_crypt, data_summary, api, address):
 data_def = ''
 t0 = time.time()
 for i in range(3):
     path = '/home/pi/Documents/FJavierGb/ULTIMATES/Public_Key'
     path1 = path + str(i)
     path2 = path1+'.py'
     public_key = open(path2,'r')
     pubk = public_key.read()
     pubk1 = RSA.importKey(pubk)
     cipher1 = PKCS1_OAEP.new(pubk1)
     data_crypt[i]= cipher1.encrypt(str(data_crypt[i]))
     public_key.close()
     data_def = data_def + data_crypt[i]
 api.send_transfer(
            transfers=[ProposedTransaction(
            address = Address(address[0]),
            message = TryteString.from_bytes(data_def),
            tag     = Tag(b'RPICTVFCOJAVIER'),
            value   = 0,
            timestamp = float(int(data_summary.iloc[5,12]))
                    )])
 t1= time.time()
 t2=t1-t0
 print('Enviado en:',t2)

def main():
    SEED = 'KHVIEEVSFJNGFWANSVKNACCVABFEOTKSY9BYUEB99L9YLCJFZEPLUDNQO9QYBVYVWUIBDSPBTKXMYJMMX'
    NODE = 'https://nodes.thetangle.org:443'
    api = Iota(NODE, SEED)
    address = [Address('XPVUPUY9XEHE9QKFNLVYFTITCTJQXXUOUEPVRBZBFXMLWBS9NNFWNIVQUROOCLHGIKAZKHYMQJPRCXRYX')]
    path='/home/pi/Documents/FJavierGb/DATOSRPICTV'
    stop=False
    while stop==False:
        try:
            make_pd(path, api, address)
        except KeyboardInterrupt:
            stop=True
            sys.exit()
main()
