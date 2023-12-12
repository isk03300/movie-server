from flask import request
from flask_restful import Resource
from mysql.connector import Error
from flask_jwt_extended import  get_jwt_identity, jwt_required
from mysql_connection import get_connection

    
class MovieReource(Resource) :
    
    def get(self,movie_id) :


        try :
            connection = get_connection()
            query = '''select 
		        m.id , m.title, m.summary, 
                m.year, m.attendance, 
                avg(r.rating) avgRating
                from movie m
                left join review r
                on m.id = r.movieId
                where m.id = %s 
                group by m.id;'''
            
            record = (movie_id , )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            result_list = cursor.fetchall()

            i =0
            for row in result_list :
                result_list[i]['year'] = row['year'].isoformat()
                i = i + 1

            print(result_list)

            cursor.close()
            connection.close()

        
        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500

        return {"result" : "success" , 
                "items" : str(result_list)
                } , 200
    
