import psycopg2 

class Database():
	def __init__(self):
		self.connection = None
		self.cursor = None
		self.connected = False

		try:
			self.connection = psycopg2.connect(user = "postgres",
										  password = "password",
										  host = "127.0.0.1",
										  port = "5432",
										  database = "ENC_Earthquake_Email_List")
			self.cursor = self.connection.cursor()
			self.connected = True
		except (Exception, psycopg2.Error) as error:
			self.connected=False



	def __del__(self):
		self.cursor.close()
		self.connection.close()

	def getEmails(self, topic=None):

		if topic == None:
			#Query to get all unique emails from the database
			get_email_query = "SELECT DISTINCT email FROM emails"
		else:
			get_email_query = self.makeEmailQueryBasedOnTopic(topic)

		#Executing the query to get all email addresses
		self.cursor.execute(get_email_query)

		#Return Email Array
		return self.cursor.fetchall()

	def makeEmailQueryBasedOnTopic(self, topic):

		get_email_query_1 = "SELECT DISTINCT email FROM emails"
		get_email_query_2 = get_email_query_1 + " WHERE " + topic + " = TRUE"

		return get_email_query_2

	def addEmail(self, emailString):
		emails = self.getEmails()

		for email in emails:
			if email[0] == emailString.lower().strip():
				return False


		add_email_query = "INSERT INTO emails (email) values ('{0}')".format(emailString.lower().strip())

		self.cursor.execute(add_email_query)

		self.connection.commit()

		return True
