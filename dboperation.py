import psycopg2


class DBWebscraping:
    def __init__(self):
        pass

    def list_search(self,connection):
        try:
            list_items = []
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "select descripcion from keyword_search"
            cur.execute(sql)
            for fila in cur:
                fila2=str(fila).replace("(","").replace(",)","").replace(" ","%20")
                list_items.append(fila2)
            cur.close()
            mydb.close() 
        except (Exception, psycopg2.DatabaseError) as error:                
                print (error)
                mydb.close()
              
        return list_items

    def insert_webscraping(self, connection, carga):
        try:
          mydb = connection.connect()         
          cur = mydb.cursor() 
          # insertando un registro
          sql = "insert into webscraping (busqueda, busqueda_area, pagina_web, url_pagina, url_busqueda,fecha_creacion,fecha_modificacion,id_keyword) values (%s,%s,%s,%s,%s,current_date,current_date,%s)"
          params = (carga["busqueda"], carga["busqueda_area"], carga["pagina"], carga["url_principal"],carga["url_busqueda"],carga["id_keyword"])
                    
          cur.execute(sql, params)                 

          mydb.commit()

          sql = "SELECT last_value FROM webscraping_id_webscraping_seq"
          cur.execute(sql)  
          row_id = int(cur.fetchone()[0])
          
          # close the communication with the PostgreSQL
          cur.close()
          mydb.close()      
        except (Exception, psycopg2.DatabaseError) as error:                
                print (error)
                mydb.close()
        
        print(row_id)        
        return row_id


class DBOferta:
    def __init__(self):
        pass

    #Valida ofertas repetidas
    def validar_oferta(self, connection, url):
        existe = False
        print(url)
        try:
            mydb = connection.connect()
            cur = mydb.cursor()   
            sql = "select COUNT(*) from oferta where url_oferta='"+url+"'"
            cur.execute(sql)
            num = int(cur.fetchone()[0])
            if num!=0:
                print("hay {} ofertas repetidas".format(str(num)))
                existe = True
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()    

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        

        return existe

    def insert_oferta(self, connection, oferta):        
        try:
            mydb = connection.connect()
            cur = mydb.cursor()                                    
            sql = "insert into Oferta (id_webscraping, titulo,empresa,lugar,salario,oferta_detalle,url_oferta,url_pagina,fecha_publicacion,fecha_creacion,fecha_modificacion,time_publicacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,current_date,current_date,%s)"            
            params = (oferta["id_carga"], oferta["puesto"].strip(), oferta["empresa"].strip(), oferta["lugar"].strip(),oferta["salario"].strip(),oferta["detalle"].strip(), oferta["url"], oferta["url_pagina"], oferta["fecha_publicacion"], oferta["timepublicacion"])
            cur.execute(sql, params)   
            mydb.commit()            


            sql = "SELECT last_value FROM Oferta_id_Oferta_seq"
            cur.execute(sql)  
            row_id = int(cur.fetchone()[0])  
            
            # close the communication with the PostgreSQL
            cur.close()
            mydb.close()                           

        except (Exception, psycopg2.DatabaseError) as error:                
                print ("-------------Exception, psycopg2.DatabaseError-------------------")
                print (error)
                mydb.close()        
            
        return row_id


class DBOfertadetalle:
    def __init__(self):
        pass

    def update_ofertadetalle(self, connection, requisito):
        mydb = connection.connect()
        mycursor = mydb.cursor()
        sql = "UPDATE OFERTA_DETALLE SET descripcion_normalizada=:1 where id_ofertadetalle=:2"
        params = (requisito["descripcion_normalizada"], requisito["iddescripcion"])

        mycursor.execute(sql, params)
        mydb.commit()

    def insertOfertaDetalle(self, connection, detalle):
        try:
            mydb= connection.connect()
            mycursor= mydb.cursor()
            sql= "insert into oferta_detalle ( id_ofertadetalle, id_oferta, descripcion, fecha_creacion, fecha_modificacion) values (DEFAULT,%s,%s,current_date,current_date)"
            params= (detalle["id_oferta"],detalle["descripcion"])
            mycursor.execute(sql, params)
            mydb.commit()
            # close the communication with the PostgreSQL
            mycursor.close()
            mydb.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print ("-------------Exception, psycopg2.DatabaseError-------------------")
            print (error)
            mydb.close()
        
        return 1
