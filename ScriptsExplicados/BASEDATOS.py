from iota import Address, Iota, Transaction, TryteString
#MODULOS NECESARIOS DE LA API DE IOTA
import time
from Crypto.PublicKey import RSA
#MODULO NECESARIO PARA DESENCRIPTAR LA INFORMACION
from Crypto.Cipher import PKCS1_OAEP
#MODULO NECESARIO PARA DESENCRIPTAR CON LA CLAVE PRIVADA
from datetime import datetime

def lista_timestamp_interv(api, upper_fecha, lower_fecha, hashes):
#ES UNA FUNCION QUE, RECIBIENDO LA CONEXION DE NUESTRA CARTERA CON EL NODO, UN 
#DICT hashes Y UNAS FECHAS LIMITE ENTRE LAS QUE BUSCAR, DEVUELVE TODAS LAS 
#TRANSACCIONES REALIZADAS EN ESAS FECHAS.
    
    lista_ord=[]
    #OBJETO TIPO LIST DONDE SE VAN A GUARDAR TODAS LAS FECHAS DE LAS TRANSACCIONES
    lista_hashes_ord = []
    #OBJETO TIPO LIST DONDE SE VAN A GUARDAR TODOS LOS HASHES DE LAS TRANSACCIONES 
    #EN EL ORDEN DE lista_ord.
    lista_hashes = hashes['hashes']
    #OBJETO TIPO LISTA CON TODOS LOS HASHES DE LAS TRANSACCIONES QUE SE ENCUENTRAN 
    #EN EL DICT HASHES, QUE RECOGE TODAS LAS TRANSACCIONES DE LA DIRECCION INDICADA.
    
    for item in lista_hashes:
    #BUCLE QUE ITERA POR TODOS LOS ELEMENTOS DE lista_hashes, OBTIENE SU CONTENIDO
    #EN EL ALFABETO TERNARIO Y ANALIZA EL TIMESTAMP DE TODAS PARA ORDENARLAS
    
        messageTrytes = api.get_trytes(hashes = [item])['trytes']
        #api.get_trytes() ES UNA FUNCION DE pyota QUE PERMITE OBTENER UN DICT CON
        #TODOS LOS TRYTES DE LA LISTA DE HASHES QUE SE LE PASA. SE LLAMA A LA 
        #FUNCION HASH POR HASH YA QUE NOS INTERESA UN DATO PUNTUAL DE CADA UNA
        #DE ELLAS Y NO TRADUCIR EL MENSAJE ENTERO. SE ESCOGEN LOS TRYTES DENTRO
        #DEL DICT, OBTENIENDOSE UNA LIST.
        
        transaccion = Transaction.from_tryte_string(messageTrytes[0])
        #Transaction ES UNA FUNCION QUE TRANSFORMA LA ENTRADA EN UN OBJETO DE
        #TIPO TREANSACTION. LA FUNCION from_tryte__string PERMITE CONVERTIR UN TEXTO
        #EN ALFABETO TERNARIO A UN STRING. DE messageTrytes UNICAMENTE NOS
        #INTERESA SU PRIMER ELEMENTO
        
        lista_ord.append(time.mktime(datetime.fromtimestamp(transaccion.timestamp).timetuple()))
        #LA FUNCION datetime TRANSFORMA UN OBJETO TIMESTAMP EN UN OBJETO DATETIME.
        #LA FUNCION fromtimestramp PERMITE OBTENER EL TIMESTAMP DE UN OBJETO
        #TIPO TRANSACTION. EL OBJETO DATETIME SE TRANSFORMA EN UN TIEMPO POSIX.
        #POR TANTO, SE OBTIENE UNA LISTA DE TODOS LOS TIMESTAMP DE LAS TRANS, SIN
        # UN ORDEN ESPECIFICO.
        
        lista_ord_sorted = sorted(lista_ord, reverse=False)
        #SE ORDENA lista_ord DE LOS MAS RECIENTES A LOS MAS ANTIGUOS
        
    date = proxim(lista_ord_sorted, upper_fecha, lower_fecha)
   #SE LLAMA A LA FUNCION proxim() DANDOLE COMO INPUTS LA LISTA DE TIMESTAMPS
   #ORDENADOS Y LOS LIMITES ENTRE LOS QUE VAMOS A BUSCAR; Y SE GUARDA EL 
   #RESULTADO EN UNA LIST 
    
    for item in date:
    #BUCLE QUE ITERA POR CADA ELEMENTO DE LOS TIMESTAMP DENTRO DE LOS LIMITES Y
    #LO RELACIONA CON LA POSICION DE LA LISTA DE HASHES GENERAL
    
        i=0
        #CONTADOR DE APOYO QUE PERMITE ITERAR POR LA LISTA DE HASHES Y TIMESTAMPS.
        for item1 in lista_ord:
        #BUCLE QUE ITERA POR CADA ELEMENTO DE LA LISTA DE TIMESTAMPS GENERAL
            if item==item1:
            #CONDICION EN LA QUE SI COINCIDEN LOS TIMESTAMP, SE GUARDA EN
            #lista_hashes_ord EL HASH CORRESPONDIENTE A LA POSICION SENNALADA POR
            #EL CONTADOR i. 
               lista_hashes_ord.append(lista_hashes[i])
               i+=1
            else: 
            #SI NO COINCIDEN, SE AUMENTA EL CONTADOR SIN ANNADIR NINGUNA INFO.
                i+=1
                pass
            
    for item2 in lista_hashes_ord:
    #BUCLE QUE ITERA POR TODOS LOS ELEMENTOS DE LA LISTA CON LOS HASHES DE LAS
    #TRANSACCIONES QUE SE ENCUENTRAN ENTRE LOS LIMITES, OBTIENE SU INFORMACION
    #EN TRYTES, Y LLAMA A OTRA FUNCION PARA QUE DESENCRIPTE LA INFORMACION. A
    #CONTINUACION, MUESTRA POR PANTALLA CADA MENSAJE DE LA LISTA DESENCRIPTADO
    
        final1= api.get_trytes(hashes = [item2])['trytes']
        #FUNCION EXPLICADA ENTRE LAS LINEAS 29-33
        
        final = Transaction.from_tryte_string(final1[0])
        #FUNCION EXPLICADA ENTRE LAS LINEAS 36-39
        
        mensaje = lect_info(final) 
        #LLAMADA A LA FUNCION lect_info PASANDO COMO INPUT LA INFORMACION EN
        #TRYTES DE CADA TRANSACCION QUE SE ENCUENTRA EN LOS LIMITES. DEVUELVE
        #EL MENSAJE DESENCRITPTADO Y SE GUARDA EN mensaje
        
        if (len(mensaje[0]) + len(mensaje[1]) + len(mensaje[2]) )!=0:   
        #CONDICIONAL EMPLEADO PARA ELIMINAR TRANSACCIONES "BASURA". AQUELLAS 
        #TRANSACCIONES QUE NO HAN SIDO ENCRIPTADAS POR NOSOTROS Y QUE, POR TANTO,
        #NO TENDRAN NINGUN TAMANNO CUANDO SEAN DESENCRIPTADAS.
        
            print(time.asctime(datetime.fromtimestamp(final.timestamp).timetuple()))
            #MUESTRA POR PANTALLA LA FECHA DE LA ULTIMA MEDIDA DEL PAQUETE DE
            #DATOS QUE ESTAMOS DESENCRIPTANDO, Y QUE ESTA ENTRE NUESTRAS FECHAS
            
            print(mensaje)
            #MUESTRA POR PANTALLA EL MENSAJE DESENCRIPTADO
        else: pass
    
def proxim(lista_ord_sorted, upper_pivot, lower_pivot):
#FUNCION LLAMADA EN lista_stamp_interv() Y QUE PERMITE OBTENER UNA
#LISTA DE TODAS LOS TIMESTAMPS COMPRENDIDOS ENTRE LOS LIMITES (upper_pivot y 
#lower_pivot) DADOS
    
    fechasD=[]
    #OBJETO TIPO LIST DONDE SE VAN A GUARDAR TODOS LOS TIMESTAMP BUSCADOS
    
    for item in lista_ord_sorted:
    #BUCLE QUE ITERA POR TODOS LOS TIMESTAMP DE lista_ord_sorted Y COMPRUEBA SI 
    #ESTAN DENTRO DE LOS LIMITES. SI ESTAN DENTRO, LO UNE A LA LISTA fechasD
        if (item >= lower_pivot and item <= upper_pivot):
        #CONDICION PARA PODER UNIR EL TIMESTAMP
            fechasD.append(item)
            #UNION DEL TIMESTAMP A LA LISTA
        else: pass
        #SI NO CUMPLE LA CONDICION, NO HACE NADA Y PASA AL SIGUIENTE ELEMENTO
    return fechasD
    #SE DEVUELVE A LA LLAMADA LA LISTA ORDENADA DE LOS TIMESTAMP
         
def lista_timestamp_conc(api,fecha, hashes):
#ES UNA FUNCION QUE, RECIBIENDO LA CONEXION DE NUESTRA CARTERA CON EL NODO, UN 
#DICT hashes Y UNA FECHAS CONCRETA, DEVUELVE LA INFORMACION DEL PAQUETE DE DATOS
#EN EL QUE SE INCLUYE ESA FECHA
    
    lista_ord=[]
    #LISTA EXPLICADA EN LINEA 16
    lista_hashes = hashes['hashes']
    #LISTA EXPLICADA EN LINEAS 21-22
    
    for item in lista_hashes:
    #BUCLE EXPLICADO EN LINEAS 25-26
        messageTrytes = api.get_trytes(hashes = [item])['trytes']
        #FUNCION Y TERMINO EXPLICADOS EN LINEAS 29-33
        transaccion = Transaction.from_tryte_string(messageTrytes[0])
        #FUNCION EXPLICADA EN LINEAS 36-39
        lista_ord.append(time.mktime(datetime.fromtimestamp(transaccion.timestamp).timetuple()))
        #FUNCION EXPLICADA EN LINEA 42-46
        lista_ord_sorted = sorted(lista_ord, reverse=False)
        #FUNCION EXPLICADA EN LINEA 49
        
    date = nearest(lista_ord_sorted, fecha)
   #SE LLAMA A LA FUNCION nearest() DANDOLE COMO INPUTS LA LISTA DE TIMESTAMPS
   #ORDENADOS Y LA FECHA QUE TIENE QUE INCLUIRSE Y SE GUARDA EL RESULTADO EN 
   #UNA VARIABLE
    
    n=0
    #CONTADOR DE APOYO QUE PERMITE ITERAR POR LA LISTA DE HASHES Y TIMESTAMPS.
    for l in lista_ord:
    #BUCLE QUE ITERA POR CADA ELEMENTO DE LA LISTA DE TIMESTAMPS GENERAL
        if l == date:
        #CONDICIONAL QUE AVISA DEL HASH CUYO TIMESTAMP COINCIDE CON LA FECHA 
        #BUSCADA, AUNQUE ESTA PUEDA SER UNA TRANSACCION "BASURA".
           
           final1= api.get_trytes(hashes = [lista_hashes[n]])['trytes']
           #FUNCION EXPLICADA ENTRE LAS LINEAS 29-33
           final = Transaction.from_tryte_string(final1[0])
           #FUNCION EXPLICADA ENTRE LAS LINEAS 36-39
           mensaje = lect_info(final) 
          #LLAMADA A LA FUNCION lect_info PASANDO COMO INPUT LA INFORMACION EN
          #TRYTES DE LA TRANSACCION MÁS PROXIMA Y SUPERIOR A NUESTRA MEDIDA. 
          #DEVUELVE EL MENSAJE DESENCRITPTADO Y SE GUARDA EN mensaje
          
           boolean = True
           #BOOLEANO QUE PERMITE CREAR UN BUCLE PARA SABER SI NO ES UNA TRANSACCION
           #BASURA
           while boolean==True:
             if (len(mensaje[0]) + len(mensaje[1]) + len(mensaje[2]) )==0:   
             #CONDICIONAL QUE ANALIZA SI EL MENSAJE ES UNA TRANSACCION BASURA,
             #SI LO ES, ANALIZA LOS SIGUIENTES HASHES HASTA ENCONTRAR UNO 
             #VÁLIDO
               n += 1
               final1= api.get_trytes(hashes = [lista_hashes[n]])['trytes']
               #FUNCION EXPLICADA ENTRE LAS LINEAS 29-33
               final = Transaction.from_tryte_string(final1[0])
               #FUNCION EXPLICADA ENTRE LAS LINEAS 36-39
               mensaje = lect_info(final) 
               #FUNCION EXPLICADA EN LAS LINEAS 160-162
             else: boolean = False
             #CONDICIONAL QUE ROMPE EL BUCLE CUANDO UNA TRANSACCION NO ES BASURA
        else:
            n+=1
            pass   
        
    print(mensaje)

def nearest(items, pivot):
#FUNCION LLAMADA EN lista_stamp_conc() Y QUE PERMITE OBTENER EL TIMESTAMP DE
#LA ULTIMA MEDIDA DEL PAQUETE EN EL QUE SE ENCUENTRA LA FECHA QUE SE SOLICITA.
#LA FUNCION ESTA TOMADA DEL SIGUIENTE LINK:
#https://stackoverflow.com/questions/32237862/find-the-closest-date-to-a-given-date  
    
  prox = min(items, key=lambda x: abs(x - pivot))
  #FUNCION QUE ITERA POR TODOS LOS TIMESTAMPS DE lista_ord_sorted Y GUARDA AQUEL
  #CUYA DIFERENCIA CON LA FECHA BUSCADA SEA MENOR. ES DECIR, ENCUENTRA EL TIMESTAMP 
  #MAS PROXIMO. AUNQUE ESTO NO NOS VALE UNICAMENTE, PORQUE NUESTRA MEDIDA SIEMPRE
  #ESTARA EN UN PAQUETE CUYA ULTIMA MEDIDA SEA SUPERIOR A LA NUESTRA
  
  if pivot > prox:
  #SI LA FECHA MAS PROXIMA ES INFERIOR A LA FECHA BUSCADA, PODEMOS ESTAR SEGUROS
  #DE QUE NUESTRA MEDIDA NO SE ENCUENTRA EN ESE PAQUETE DE MEDIDAS, ES DECIR, EN
  #ESE TIMESTAMP, SI NO EN EL SIGUIENTE.
  
      if items.index(prox) == len(items)-1:
      #ES UN CONDICIONAL QUE EVITA QUE SE ESCOJA UN TERMINO FUERA DE LA LISTA. SI
      #NO HAY MEDIDAS TOMADAS, SE MUESTRA LA ULTIMA DISPONIBLE Y SE AVISA.
          nearest=prox
          print('No se han tomado medidas en esa fecha')
          
      else: nearest = items[items.index(prox)+1]
      #SI NO SE SALE DE LA LISTA, SE COGE EL SIGUIENTE TIMESTAMP AL MAS PROXIMO.
      
  else:
  #EN CASO DE QUE EL TIMESTAMP MAS PROXIMO SEA ADEMAS MAYOR QUE NUESTRA FECHA,
  #PODEMOS ESTAR SEGUROS DE QUE NUESTRA MEDIDA ESTARA EN ESE PAQUETE Y QUE NO
  #NOS SALDREMOS DEL INDICE DE LA LISTA
      nearest = prox
      
  return nearest
  #DEVUELVE EL TIMESTAMP ESPECIFICADO EN LA PARTE SUPERIOR

def lect_info(transaccion):
#ES LA FUNCION ENCARGADA DE DESENCRIPTAR EL MENSAJE CONTENIDO DE LAS TRANSACCIONES.
#RECIBE COMO INPUTS LOS TRYTES DE UNA TRANSACCION, Y MEDIANTE FUNCIONES DE LA 
#LIBRERIA Iota SEPARA LOS TRYTES PERTENECIENTES A CADA ELEMENTO (VER APARTADO 3.4)
    
    j=0
    #CONTADOR DE APOYO PARA DIVIDIR LA FIRMA EN 3 BLOQUES
    
    MENSAJE = ['','','']
    #DECLARACION DE LA LISTA DE STRINGS DONDE SE VA A GUARDAR EL MENSAJE EN TRYTES  
    #QUE PERTENECE A CADA CLIENTE
    
    MENSAJE_BYTES = [TryteString(''), TryteString(''), TryteString('')]
    #DECLARACION DE LA LISTA DE TRYTESTRINGS DONDE SE VAN A GUARDAR LOS BYTES
    #QUE PERTENECEN A CADA CLIENTE
    
    for i in str(transaccion.signature_message_fragment):
    #BUCLE QUE ITERA POR TODOS LOS CARACTERES DE LA FIRMA DEL MENSAJE (VER 
    #APARTADO 3.4) Y LOS GUARDA EN FUNCION DE LA POSICION QUE OCUPAN.
    #NO ES CASUALIDAD QUE ESTE DIVIDIDO EN 2^8 CARACTERES, SI NO QUE ES 
    #CONSECUENCIA DE LA SEGURIDAD EMPLEADA EN LA ENCRIPTACION.
    #LAS MEDIDAS SE ENCRIPTAN SIEMPRE CON UN TAMANNO DE 128 BYTES, QUE SE 
    #CORRESPONDE CON 256 TRYTES.
    
        j = j + 1
        if j<=256:
        #CONDICIONAL QUE SELECCIONA LA PARTE DEL CLIENTE A
            MENSAJE[0] += i
        if 256<j<=512:
        #CONDICIONAL QUE SELECCIONA LA PARTE DEL CLIENTE B
            MENSAJE[1] += i
        if 512<j<=768:
        #CONDICIONAL QUE SELECCIONA LA PARTE DEL CLIENTE C
            MENSAJE[2] += i

    try:
    #CONDICIONAL QUE SIEMPRE INTENTA REALIZAR LAS SIGUIENTES FUNCIONES
        MENSAJE_BYTES[0]=TryteString.as_bytes(TryteString(MENSAJE[0]))
        #FUNCION QUE CONVIERTE EL OBJETO TryteString A UNA CADENA DE BYTES. SE
        #CORRESPONDE CON LOS BYTES ENCRIPTADOS DEL CLIENTE A
        MENSAJE_BYTES[1]=TryteString.as_bytes(TryteString(MENSAJE[1]))
        #FUNCION QUE CONVIERTE EL OBJETO TryteString A UNA CADENA DE BYTES. SE
        #CORRESPONDE CON LOS BYTES ENCRIPTADOS DEL CLIENTE B
        MENSAJE_BYTES[2]=TryteString.as_bytes(TryteString(MENSAJE[2]))
        #FUNCION QUE CONVIERTE EL OBJETO TryteString A UNA CADENA DE BYTES. SE
        #CORRESPONDE CON LOS BYTES ENCRIPTADOS DEL CLIENTE C
        
    except Exception:
    #CUANDO UN MENSAJE NO PUEDE TRANSFORMARSE DE TRYTE A BYTE, PASAMOS
        pass

    messageD=['','','']
    #DECLARACION DE LA LISTA DE STRINGS DONDE SE VA A GUARDAR EL MENSAJE FINAL
    
    for i in range(3):
    #RANGO QUE ITERA ENTRE LOS 3 CLIENTES PARA DESENCRIPTAR SU PARTE CORRESPONDIENTE
    
     path = 'C:\\Universidad\\TFG\\Scripts\\Nuevos\\Datos\\Private_key'
     path1 = path + str(i)
     path2 = path1+'.py'
     #METODO EMPLEADO PARA LOCALIZAR EL DOCUMENTO DONDE CADA CLIENTE TIENE SU LLAVE
     #PRIVADA, NECESARIA PARA DESENCRIPTAR EL MENSAJE QUE SE HABIA CIFRADO CON
     #SU CLAVE PUBLICA, A DISPOSICION DEL AUTOR DEL PROYECTO.
     
     private_key = open(path2,'r')
     pivk = private_key.read()
     #FUNCIONES EMPLEADAS PARA ABRIR Y GUARDAR EN LA VARIABLE pivk LA CLAVE 
     #PRIVADA DEL CLIENTE ESPECIFICO EN CADA ITERACION.
     
     pivk1 = RSA.importKey(pivk)
     dcipher1 = PKCS1_OAEP.new(pivk1)
     #FUNCIONES QUE PREPARAN EL ALGORITMO A UTILIZAR JUNTO A LA CLAVE PRIVADA
     #PARA DESENCRIPTAR EL MENSAJE EN BYTES. VER APARTADO 3.3.
   
     try:
         messageD[i]= dcipher1.decrypt(MENSAJE_BYTES[i])
     #DESENCRIPTA EL MENSAJE CON LA CLAVE PRIVADA DE CADA CLIENTE 
     #SEGUN LA ITERACION DEL BUCLE. SOLO PODRA DESENCRIPTAR LA PARTE DEL MENSAJE
     #QUE HAYA SIDO ENCRIPTADA CON LA CORRESPONDIENTE LLAVE PUBLICA.
     
     except Exception:
         pass
     #EVITA QUE SALTE UN ERROR CUANDO SE INTENTA DESENCRIPTAR UNA PARTE QUE NO HA
     #SIDO ENCRIPTADA CON LA LLAVE PUBLICA CORRESPONDIENTE.
     
     private_key.close()
     #CIERRA EL ARCHIVO DONDE SE ENCUENTRA LA CLAVE PRIVADA
    
    return messageD
    #ESTA FUNCION DEVUELVE EL MENSAJE DESENCRIPTADO DE LA CADENA DE TRYTES DE 
    #UNA TRANSACCION.

def main():
#FUNCION PRINCIPAL. SIEMPRE SE LLAMA Y EXISTE PARA DAR MAYOR GRANULIDAD AL 
#SCRIPT, MEJORANDO SU ENTENDIMIENTO Y EL ANALISIS DE ERRORES
    
    SEED = 'INTRODUCIR SEMILLA AQUI'
    #CLAVE PRIVADA DEL CLIENTE EN IOTA. VER EL APARTADO 3.4. PARA SABER COMO
    #DEBE CREARSE.
    
    NODE = 'https://nodes.thetangle.org:443'
    #NODO AL QUE VAMOS A CONECTARNOS Y LEER LAS TRANSACCIONES. PARA SABER MAS
    #DE ESTE NODO, VER EL APARTADO 3.4. 
    #SE TRATA DEL NODO DE LA PAGINA thetangle.org.

    api = Iota(NODE, SEED)
    #FUNCION QUE CONECTA NUESTRA SEED AL NODO CON EL QUE VAMOS A TRABAJAR.
    #HAY QUE TENER EN CUENTA QUE LAS TRANSACCIONES QUE VAN A ENCONTRARSE CON 
    #LAS FUNCIONES EMPLEADAS SON LAS QUE SE ENCUENTRAN EN EL TANGLE DESDE EL
    #ULTIMO SNAPSHOT (VER APARTADO 3.4.)
    #EN LA PÁGINA THETANGLE.ORG APARECERAN MAS DE LAS QUE SE ENCONTRARAN AQUI.
    #YA QUE MANTIENE UN REGISTRO DE TRANSACCIONES DESPUES DE SNAPSHOTS
    
    direccion = [Address('XPVUPUY9XEHE9QKFNLVYFTITCTJQXXUOUEPVRBZBFXMLWBS9NNFWNIVQUROOCLHGIKAZKHYMQJPRCXRYX')]
    #SE TRATA DE LA DIRECCION A LA QUE SE VAN A ENVIAR LAS TRANSACCIONES DE VALOR
    #CERO (VER APARTADO 3.4.), PERTENECIENTE A LA SEMILLA DEL AUTOR DEL PROYECTO.
    #SERA LA DIRECCION EN LA QUE TRATAREMOS DE LEER LA INFORMACION.
    
    hashes = api.find_transactions(addresses = direccion)
    #LA FUNCION api.find_transactions PERMITE OBTENER UN DICT CON TODAS LAS 
    #TRANSACCIONES QUE SE HAN ENVIADO A LA DIRECCION QUE SE ESPECIFIQUE. SE 
    #GUARDA EN hashes Y SOLO NOS INTERESA EL CONTENIDO DE 'hashes'.

    print('¿Quiere buscar una fecha concreta? Sí (1)/N (0)))')
    #SALIDA POR PANTALLA QUE PREGUNTA SI QUIERES BUSCAR UNA FECHA CONCRETA O UN
    #INTERVALO
    modo = input()
    #FUNCION QUE PERMITE INTRODUCIR POR PANTALLA EL MODO DE BUSQUEDA

    if modo==0:
    #CONDICIONAL SI SE SELECCIONA BUSCAR UN INTERVALO
        print('Escriba el intervalo:')
        #SALIDA POR PANTALLA QUE INDICA QUE DEBES INDICAR EL INTERVALO
        
        print('Escriba el límite superior:')
        #SALIDA POR PANTALLA QUE INDICA QUE DEBES INDICAR EL LIMITE SUPERIOR
        upper_fecha = time.mktime(datetime(
                input('Introduzca el anno:'),input('Introduzca el mes:'),
                input('Introduzca el dia:'),input('Introduzca la hora:'),
                input('Introduzca los min:'),input('Introduzca los seg:')).timetuple())
                #FUNCION QUE TRANSFORMA EN TIEMPO UNIX UN TIEMPO ESTRUCTURADO EN
                #ANNO, MES, DIA, HORA Y SEGUNDO PARA FACILITAR EL INPUT DEL 
                #LIMITE SUPERIOR.
                
        print('Escriba el límite inferior:')
        #SALIDA POR PANTALLA QUE INDICA QUE DEBES INDICAR EL LIMITE INFERIOR
        lower_fecha = time.mktime(datetime(
                input('Introduzca el anno:'),input('Introduzca el mes:'),
                input('Introduzca el dia:'),input('Introduzca la hora:'),
                input('Introduzca los min:'),input('Introduzca los seg:')).timetuple())
                #FUNCION QUE TRANSFORMA EN TIEMPO UNIX UN TIEMPO ESTRUCTURADO EN
                #ANNO, MES, DIA, HORA Y SEGUNDO PARA FACILITAR EL INPUT DEL 
                #LIMITE INFERIOR.
        
        lista_timestamp_interv(api,upper_fecha, lower_fecha, hashes)
        #LLAMADA A LA FUNCION lista_timestamp_interv PASANDOLE COMO INPUTS EL 
        #ACCESO AL NODO ESPECIFICADO, LAS FECHAS LIMITES Y EL LISTADO DE HASHES
        #DE LA DIRECCION ESPECIFICADA.
        
    if modo == 1: 
    #CONDICIONAL SI SE SELECCIONA BUSCAR UNA FECHA CONCRETA
        fecha = time.mktime(datetime(
                input('Introduzca el anno:'),input('Introduzca el mes:'),
                input('Introduzca el dia:'),input('Introduzca la hora:'),
                input('Introduzca los min:'),input('Introduzca los seg:')).timetuple())
        #FUNCION QUE TRANSFORMA EN TIEMPO UNIX UN TIEMPO ESTRUCTURADO EN
        #ANNO, MES, DIA, HORA Y SEGUNDO PARA FACILITAR EL INPUT DE LA FECHA.
        
        lista_timestamp_conc(api,fecha, hashes)
        #LLAMADA A LA FUNCION lista_timestamp_conc PASANDOLE COMO INPUTS EL 
        #ACCESO AL NODO ESPECIFICADO, LA FECHA BUSCADA Y EL LISTADO DE HASHES
        #DE LA DIRECCION ESPECIFICADA.

main()
#LLAMADA A FUNCION MAIN. SIEMPRE VA A OCURRIR; SE ENCIERRA EN FUNCIONES PARA
#MEJORAR EL CONTROL DEL SCRIPT

