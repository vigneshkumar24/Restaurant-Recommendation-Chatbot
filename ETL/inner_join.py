import mysql.connector
import psycopg2

mydb1 = psycopg2.connect(user='postgres',
                               password='Sheldon@1',
                               database='yelp')
mydb2 = psycopg2.connect(user='postgres',
                               password='Sheldon@1',
                               database='yelp')
mycursor1 = mydb1.cursor()
mycursor2 = mydb2.cursor()
#mycursor.execute('select * from business limit 5')

mycursor1.execute('SELECT b.business_id,b.name,b.address,b.city,b.state,b.categories,b.hours,r.review_id,r.text,r.stars FROM yelp_business b INNER JOIN yelp_reviews r ON b.business_id=r.business_id')

i = 0
for business_id,name,address,city,state,categories,hours,review_id,text,stars in mycursor1:
    values = (business_id,name,address,city,state,categories,hours,review_id,text,stars)
    query = 'INSERT INTO restaurant VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    mycursor2.execute(query,values)
    mydb2.commit()
    
    i += 1

    if i %10000 == 0:
        print(f'Inserted {i} rows')
