import mysql.connector
from mysql.connector import errorcode

import json

import rds_config

# Collect new papers from the database and return them as json object
def query_database():

	# Connect to the database
	cnx = mysql.connector.connect(user = rds_config.db_username,
								  password = rds_config.db_password,
								  database = rds_config.db_name,
								  host = rds_config.db_host
								 )
	print('Succesfully connected to the database')
	
	cursor = cnx.cursor()

	sql_recent_papers = ("SELECT title, authors, abstract, link, label FROM papers "
						 "WHERE date = (SELECT MAX(date) FROM papers)"
						)

	cursor.execute(sql_recent_papers)

	results = {}
	results['papers'] = []

	for title, authors, abstract, link, label in cursor.fetchall():

		single_result = {}
		single_result['name'] = title
		single_result['authors'] = authors
		single_result['abstract'] = abstract
		single_result['link'] = link
		single_result['tag'] = label

		results['papers'].append(single_result)

	print('New papers fetched from the database')

	# Close the database now that we have updated it
	cnx.close()
	print('Connection to the database closed')

	return json.dumps(results)

