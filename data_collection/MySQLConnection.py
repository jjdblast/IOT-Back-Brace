import json

def getDBConnectionProps(credentialFile):
	# Open MYSQL credentials file to get username and password
	with open(credentialFile, 'r') as f:
		creds = json.load(f)

	# Establish an object that will hold the MYSQL database connection properties
	connectionProperties = {
	"user":creds["user"],
	"password":creds["password"],
	"driver":"com.mysql.jdbc.Driver"
	}
	
	return connectionProperties

if __name__ == '__main__':
	print(getDBConnectionProps('/home/erik/mysql_credentials.txt'))