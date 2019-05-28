import psycopg2

def getEmails():
	
	get_email_query = "SELECT DISTINCT email FROM emails"
	connection = None
	
	try:
		connection = psycopg2.connect(user = "postgres",
									  password = "password",
									  host = "127.0.0.1",
									  port = "5432",
									  database = "ENC_Earthquake_Email_List")
									  
		cursor = connection.cursor()

		cursor.execute(get_email_query)
		emailArray = cursor.fetchall()

	except (Exception, psycopg2.Error) as error :
		emailArray = []
		print ("Error while connecting to Email Database", error)
	finally:
		if(connection):
			cursor.close()
			connection.close()
			print("Email Database connection is closed")
		return emailArray
		
		
print (getEmails())