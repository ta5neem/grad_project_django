# import mysql.connector
# import pymssql
# from sqlalchemy import create_engine
import os
import django
import sys
import sys
import os
from django.db import connections
from django.conf import settings
from django.shortcuts import render
from asgiref.sync import sync_to_async
from datetime import date
import sqlite3
from django.contrib.auth import get_user
# from channels.routing import ProtocolTypeRouter, URLRouter
# from myapp.middleware import UserMiddleware
from django.urls import path
# from myapp import consumers
from django.contrib.auth import get_user_model
outer_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'evaluation'))
# Add the outer folder path to sys.path
sys.path.append(outer_folder_path)
# Now you can import the file
# from evaluation import views

# import project.evaluation
# from evaluation import views


class DataBase : 
    
    mycursor =None
    user_id = 5
    def __init__(self,user_id) :
        print("my_variable" + str(user_id))  
        self.user_id = user_id


    def get_tables(path) : 
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        # Print the table names
        for table in tables:
            print(table[0])
        # print("the user Id" + str(self.user_id))
        # # Close the connection
        # # conn.close()
        

# class UserMiddleware(BaseMiddleware):
#     async def resolve_scope(self, scope):
#         scope['user'] = await database_sync_to_async(get_current_authenticated_user)()

#         application = ProtocolTypeRouter(
#             {
#                 "http": get_asgi_application(),
#                 "websocket": UserMiddleware(
#                     URLRouter(
#                         [
#                             path("ws/chat/", consumers.ChatConsumer.as_asgi()),
#                             # Add your WebSocket consumer paths here
#                         ]
#                     )
#                 ),
#             }
#         )


        # Example: Retrieve data from the table
        # cursor.execute("SELECT * FROM evaluation_evaluation")
        # rows = cursor.fetchall()
        # for row in rows:
        #     print(row)

        conn.commit()
        conn.close()    

        print ("done")

        # cnxn = pyodbc.connect('DRIVER={Devart ODBC Driver for SQLite};Direct=True;Database=mydatabase;String Types= Unicode')

#######################
        # sys.path.append('D:/Newfolder/Desktop/df/ProjectFolder/django/project/')
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
        # settings.BASE_DIR = 'D:/Newfolder/Desktop/df/ProjectFolder/django/project/project/'

        # sys.path.append(settings.BASE_DIR)


        # # Replace `project` with the actual name of your project.

        # connection = connections['default']
#################
        # Execute a SQL query
        # with connection.cursor() as cursor:
        #     cursor.execute('SELECT * FROM Evaluations')
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         print(row)

        

    def set_user_id(self ,value):      
        global user_id  # Declare global_var as global inside the function
        user_id = value
        print("my_variable" + str(user_id))

    def get_cols_name(path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor() 
        cursor.execute("PRAGMA table_info(evaluation_evaluation)")
        columns = cursor.fetchall()

        # Print the column names
        for column in columns:
            column_name = column[1]
            print(column_name)
        
        conn.commit()
        conn.close()    



    def store_vedio_cols(path,size,time,title,user_i):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        current_date = date.today()
        print(current_date)
        # user_i = user_id
        cursor.execute("INSERT INTO evaluation_video (size, time, title , date ,user_id_id) VALUES (?, ?, ? ,? ,?)", (size, time, title , current_date ,user_i))
        conn.commit()
        conn.close()
        # pass

    # def store_vedio_cols(size,time,title):
    #     conn = sqlite3.connect('D:\\Newfolder\\Desktop\\df\\ProjectFolder\\django\\project\\db.sqlite3')
    #     cursor = conn.cursor()
    #     current_date = date.today()
    #     print(current_date)
    #     user_id = 1
    #     cursor.execute("INSERT INTO evaluation_video (size, time, title , date ,user_id_id) VALUES (?, ?, ? ,? ,?)", (size, time, title , current_date ,user_id))
    #     conn.commit()
    #     conn.close()
    def eval_from_10( value,from_): 
        eval_from_10_= 10 - ((value * 10) /from_ )
        return eval_from_10_
    

    def store_Eval_cols(path,motion_count) : 
        conn = sqlite3.connect(path)
        cursor = conn.cursor()



    def store_Hands_cols(path,motion_count,total_time):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        HAND_ON_HEAD=0
        HAND_CROSSED=0
        HAND_ON_HIP=0
        STRAIGHT_DOWN=0
        CLOSED_U_HANDS=0
        CLOSED_D_HANDS=0
        OUT_BOX=0
        from_ = total_time / 5
        
        for key, value in motion_count.items():
                if key == 'HAND_ON_HEAD' :
                    # type: ignore
                    HAND_ON_HEAD +=  ((value * 10) /from_ )
                if key == 'HAND_CROSSED' :
                    HAND_CROSSED +=  ((value * 10) /from_ ) 
                if key == 'HAND_ON_HIP' :
                    HAND_ON_HIP +=  ((value * 10) /from_ ) 
                if key == 'STRAIGHT_DOWN' :
                    STRAIGHT_DOWN +=  ((value * 10) /from_ ) 
                if key == 'CLOSED_U_HANDS' :
                    CLOSED_U_HANDS += ((value * 10) /from_ )  
                if key == 'CLOSED_D_HANDS' :
                    CLOSED_D_HANDS +=  ((value * 10) /from_ )  
                if key == 'OUT_BOX' :
                    OUT_BOX +=  ((value * 10) /from_ )


        # Execute a SELECT query to get the last ID in the specific table
        cursor.execute("SELECT id FROM evaluation_evaluation ORDER BY id DESC LIMIT 1")
        # Fetch the result
        result = cursor.fetchone()
        last_id = result[0] if result else 0
        print ("the last " + str(last_id)) 
        evaluation_id = last_id+1
        current_date = date.today()
        print(current_date)
        user_id = 1
        cursor.execute("INSERT INTO evaluation_handeval (CLOSED_U_HANDS, HAND_CROSSED, HAND_ON_HIP , HAND_ON_HEAD ,STRAIGHT_DOWN , CLOSED_D_HANDS ,OUT_BOX ,evaluation_id_id) VALUES (?,?,?,?, ?, ? ,? ,?)", (CLOSED_U_HANDS, HAND_CROSSED, HAND_ON_HIP , HAND_ON_HEAD ,STRAIGHT_DOWN , CLOSED_D_HANDS ,OUT_BOX ,evaluation_id) )

        cursor.execute("SELECT id FROM evaluation_video ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        last_id = result[0] if result else None
        print ("the last " + str(last_id)) 
        total_eval = (HAND_ON_HEAD+HAND_CROSSED+ HAND_ON_HIP +STRAIGHT_DOWN +CLOSED_U_HANDS+OUT_BOX +CLOSED_D_HANDS)/7

        cursor.execute("INSERT INTO evaluation_evaluation (total_eval ,video_id_id) VALUES (?,?)", (total_eval ,last_id) )
        conn.commit()
        conn.close()   
        


    def get_hand_evals(self,id):

        query = "SELECT * FROM hand_evaluation WHERE evaluation_id = (SELECT id FROM evaluation WHERE video_id = 2)"
        id = "select * from hand_evals where id='%s'" % (id)
        self.mycursor.execute(id)
        id = self.mycursor.fetchall()

        sql = "select * from face_evals where id =  (%s)" % (id[0][0])
        self. mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        print (myresult)



         


