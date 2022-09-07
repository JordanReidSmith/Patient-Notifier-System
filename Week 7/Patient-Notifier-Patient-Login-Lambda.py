import json
import pymysql
import boto3
import datetime

def lambda_handler(event, context):
    # Get database credentials from AWS Secrets
    creds = get_secret()
    
    # Attempt connection to MySQL server
    try:
        # Connect to database using secret credentials
        conn = pymysql.connect(host=creds['host'], user=creds['username'], passwd=creds['password'], db="patient-notifier-schema", connect_timeout=5)
    except pymysql.MySQLError as e:
        # If connection failed, report back exception and end execution
        return {
        'statusCode': 69,
        'body': json.dumps(str(e))
    }
    
    #Get values from triggering event and save into variables
    patientID = attempt_login(conn, event["username"], event["password"])
    
    # Execute SQL code on the database, in this case retrieving the field that intersects the triggering events coloumn and ID 
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT dateOfSending, notiTitle, notiDesc FROM notificationHistoryTable WHERE patientID = {0};".format(patientID))
            notifications = cur.fetchall()
            cur.execute("SELECT fullName, email, age, weights, steps FROM patientDataTable WHERE patientID = {0};".format(patientID))
            patientData = cur.fetchall()
            cur.execute("SELECT unreadNotis FROM loginTable WHERE patientID = {0};".format(patientID))
            newNotifications = cur.fetchone()
            cur.execute("UPDATE loginTable SET unreadNotis = 0 WHERE patientID = {0};".format(patientID))
            conn.commit()
        except Exception as e:
            return str(e)
    
    return {
        'statusCode': 200,
        'body': "Succesfully retrieved patient data",
        'patientData': patientData,
        'notifications': notifications,
        'newNotifications': newNotifications
    }
    
def get_secret():
    # Secret manager reference
    secret_name = "patient-notifier-database-creds"
    region_name = "ap-southeast-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    # Get encrypted secret value
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    # Turn stringified secret back into JSON
    return json.loads(secret)

def attempt_login(conn, username, password):
    with conn.cursor() as cur:
        try:
            cur.execute('SELECT pass, patientID FROM loginTable WHERE username = "{0}";'.format(username))
        except Exception as e:
            return str(e)
    
    results = cur.fetchone()
    matchingPass = results[0]
    returnID = results[1]
    
    if password == matchingPass:
        return returnID
    
    raise Exception("Sorry, incorrect login information")