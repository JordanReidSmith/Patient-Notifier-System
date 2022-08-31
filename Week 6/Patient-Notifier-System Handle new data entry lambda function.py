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
    patientID = event["id"]
    coloumn = event["coloumn"]
    value = event["value"]
    
    # Get today's date from datetime and turn it into a string with correct format
    today = datetime.date.today()
    todayDate = today.strftime("%d//%m//%Y")
    
    # Execute SQL code on the database, in this case retrieving the field that intersects the triggering events coloumn and ID 
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT {0} FROM patientDataTable WHERE patientID = {1};".format(coloumn, patientID))
        except Exception as e:
            return str(e)
            
    # Begin processing of notifications by extracting most recent stored data from database
    entries = cur.fetchone()[0]
    entries = json.loads(entries)
    
    # Seperate out the key/date and the value
    recentEntryDate = list(entries)[-1]
    recentEntry = entries[recentEntryDate]
    recentEntryDate = datetime.datetime.strptime(recentEntryDate, '%d//%m//%Y').date()
    
    # Process information for notifications
    if coloumn == 'weights':
        # Calculate the days between now and last entry
        dateDelta = (today - recentEntryDate).days
        results = str(recentEntryDate)
        
        # If weight has changed by greater then 2 kg a day since last entry, then send notification
        if (dateDelta > 0):
            if abs(value - recentEntry)/dateDelta >= 2:
                with conn.cursor() as cur:
                    try:
                        compatibleDate = todayDate.replace('/', '')
                        cur.execute("INSERT INTO notificationHistoryTable (patientID, dateOfSending, notiTitle, notiDesc) VALUES ({0}, {1}, {2}, {3})".format(patientID, compatibleDate, "'Substantial Weight Change'", "'Consult your doctor'"))
                    except Exception as e:
                        return str(e)
                print("Substantial weight change, consult your doctor")
    
    # Execute SQL code on the database, in this case append or update todays entry with the triggering events input value
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE patientDataTable SET {0} = JSON_SET({0}, '$.\"{1}\"', {2}) WHERE patientID = {3};".format(coloumn, todayDate, value, patientID))
        except Exception as e:
            return str(e)
            
    conn.commit()
    
    # Return success 
    return {
        'statusCode': 200,
        #'body': results
        'body': "Added {0}: {1} to {2} coloumn of patient {3}".format(todayDate, value, coloumn, patientID)
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