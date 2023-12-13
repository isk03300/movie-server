from flask import request
from flask_restful import Resource
from mysql.connector import Error
from flask_jwt_extended import  get_jwt_identity, jwt_required
from mysql_connection import get_connection

class ReviewCountResource(Resource) :
    def get(self) :

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select m.id, m.title, 
            count(r.content) countContent, avg(r.rating) avgRating
                                    from movie m
                                    left join review r
                                    on m.id = r.movieId
                                    group by m.id
                                    order by countContent desc
                                    limit '''+str(offset) +''', '''+str(limit) +''' ;'''
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result_list = cursor.fetchall()



            print()
            print(result_list)
            
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : str(result_list),
                "count" : len(result_list)} , 200
    
    
class ReviewRatingResource(Resource) :

    def get(self) :

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select m.id, m.title, 
            count(r.content) countContent, avg(r.rating) avgRating
                                    from movie m
                                    left join review r
                                    on m.id = r.movieId
                                    group by m.id
                                    order by avgRating desc
                                    limit '''+str(offset) +''', '''+str(limit) +''' ;'''
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            result_list = cursor.fetchall()



            print()
            print(result_list)
            
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"result" : "fail" , "error" : str(e)}, 500


        return {"result" : "success" , 
                "items" : str(result_list),
                "count" : len(result_list)} , 200
    
class ReviewSource(Resource) :
    def get(self,movie_id) :

        try :
            connection = get_connection()
            query = '''select r.id , u.nickname, u.gender, r.rating
                            from movie m
                            join review r
                            on m.id = r.movieId
                            join user u
                            on r.userId = u.id
                            where m.id = %s;'''
            
            record = (movie_id, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            relust_list = cursor.fetchall()

            print()
            print(relust_list)

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)} , 400
        

        return {'result' : 'success',
                'review' : relust_list,
                'count' : len(relust_list)},200
    




class MyReviewResource(Resource) :
    @jwt_required()
    def post(self) :

        

        data = request.get_json()

        user_id = get_jwt_identity()

        print(data)
        print()

        try :

            conncetion = get_connection()
            query = '''insert into review
                        (movieId, userId, rating, content)
                        values
                        (%s,%s,%s,%s);'''
            
            record = (data['movieId'],
                      user_id,
                      data['rating'],
                      data['content'])
            
            cursor = conncetion.cursor()
            cursor.execute(query,record)

            conncetion.commit()

            cursor.close()
            conncetion.close()


        except Error as e :
            print(e)
            cursor.close()
            conncetion.close()
            return {'error' : str(e)},400


        return {'result' : 'success'},200

    @jwt_required(optional=True)
    def get(self) :
        movieId = request.args.get('movieId')
        offset = request.args.get('offset')
        limit = request.args.get('limit')

        try :
            connection = get_connection()
            query = '''select r.id , u.nickname, u.gender, r.rating
                            from review r
                            join user u
                            on r.userId = u.id
                            where r.movieId = %s
                            order by r.createdAt desc
                            limit '''+str(offset) +''','''+str(limit) +''';'''
            
            record = (movieId, )

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query,record)

            relust_list = cursor.fetchall()

            print()
            print(relust_list)

            cursor.close()
            connection.close()


        except Error as e:
            print(e)
            cursor.close()
            connection.close()
            return {'error' : str(e)} , 400
        

        return {'result' : 'success',
                'review' : relust_list,
                'count' : len(relust_list)},200
    