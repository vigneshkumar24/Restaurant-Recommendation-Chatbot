# Importing required libraries
import multiprocessing
from pymongo import MongoClient
import mysql.connector
import psycopg2
import json

# Processes running on parallel
def process_cursor(skip_n,limit_n):

    print('Starting process',skip_n//limit_n,'...')
    # Connect to the MongoDB
    collection = MongoClient().yelp_data.rawdata
    cursor = collection.find({}).skip(skip_n).limit(limit_n)
 
    # Connect to the MySQL
    mydb = psycopg2.connect(user='postgres', password='Sheldon@1', database='yelp')
    mycursor = mydb.cursor()

    # Insert query
    sql = 'INSERT INTO yelp_business (business_id, name, address, city, state, stars, review_count, is_open, attributes, categories, hours) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)'
    #sql1 = 'INSERT INTO yelp_business(hours) VALUES (%s)'
    # Loop through the cursor
    for doc in cursor:
        # Insert values from MongoDB to MySQL
        if doc['categories'] is None:
            continue
        #'Restaurants' in doc['categories']) and
        if ('Restaurants' in doc['categories']) and ('Restaurants' in doc['categories']) and (doc['state'] in ['ON', 'BC']):
            if doc['hours'] is not None:
                doc['hours'] = [x + ': ' + doc['hours'][x] + ', ' for x in doc['hours']]

            if doc['attributes'] is not None:
                doc['attributes'] = [x + ': ' + doc['attributes'][x] + ', ' for x in doc['attributes']]

                #doc['hours'] = list(map(lambda x: json.dumps(x), doc['hours']))
            val = (doc['business_id'], doc['name'].encode("ascii", "ignore").decode(), doc['address'], doc['city'], doc['state'], doc['stars'], doc['review_count'], doc['is_open'], doc['attributes'], doc['categories'], doc['hours'])

            print(val)
            mycursor.execute(sql,val)
            #mycursor.execute(sql1,list(doc['hours']))
            #print(mycursor)

            mydb.commit()

    print('Completed process',skip_n//limit_n,'...')


if __name__ == '__main__':
    n_cores = 4
    collection_size = 160585
    # Size of batches
    batch_size = round(collection_size/n_cores+0.5)
    # Generator to skip the cursors 
    skips = range(0, n_cores*batch_size, batch_size)

    # Creating multiple process to run on parallel
    processes = [ multiprocessing.Process(target=process_cursor, args=(skip_n,batch_size)) for skip_n in skips]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
