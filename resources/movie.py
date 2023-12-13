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
                result_list[i]['avgRating'] = float(row['avgRating'])
                i = i + 1

            print(result_list[0])

            cursor.close()
            connection.close()

        
        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500

        return {"result" : "success" , 
                "items" : result_list[0]
                } , 200
    
class MovieListResourece(Resource) :

    @jwt_required()
    def get(self) :

        order = request.args.get('order')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''select m.id, m.title, count(r.id) reviewCnt,
                                ifnull(avg(r.rating),0) as avgRating ,
                                if( f.id is null  , 0 , 1 ) as isFavorite
                                from movie m
                                left join review r
                                on r.movieId = m.id
                                left join favorite f
                                on m.id = f.movieId and f.userId = %s
                                group by m.id
                                order by '''+order+''' desc
                                limit '''+offset+''', '''+limit+''' ;'''
            
            record = (user_id , )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query,record)

            result_list = cursor.fetchall()

            
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
        
        
        i = 0
        for row in result_list :
            result_list[i]['avgRating'] = float(row['avgRating'])
            i = i + 1


        return {'result' : 'success',
                'items' : result_list,
                'count' : len(result_list)}, 200
    
class MovieSearchResource(Resource) :

    
    @jwt_required()
    def get(self) :


        

        keyword = request.args.get('keyword')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :

            connection = get_connection()

            query = '''select m.id, m.title, m.summary, count(r.id) reviewCnt,
                                ifnull(avg(r.rating),0) as avgRating 
                                from movie m
                                left join review r
                                on m.id = r.movieId 
                                where m.title like '%'''+keyword+'''%' or m.summary like '%'''+keyword+'''%'
                                group by m.id
                                order by reviewCnt desc
                                limit 0, 25;'''
            
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)}, 500
        
        
        i = 0
        for row in result_list :
            result_list[i]['avgRating'] = float(row['avgRating'])
            i = i + 1


        return {'result' : 'success',
                'items' : result_list,
                'count' : len(result_list)}, 200
    