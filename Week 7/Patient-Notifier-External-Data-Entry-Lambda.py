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
    print(patientID)
    coloumn = event["entryType"]
    value = event["entryValue"]
    
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
    entryDates = list(entries)
    latestEntryDate = datetime.datetime.strptime(entryDates[0], '%d//%m//%Y').date()
    for date in entryDates:
        if datetime.datetime.strptime(date, '%d//%m//%Y').date() > latestEntryDate:
            latestEntryDate = datetime.datetime.strptime(date, '%d//%m//%Y').date()
    
    latestEntry = entries[latestEntryDate.strftime("%d//%m//%Y")]
    
    # Process information for notifications
    if coloumn == 'weights':
        # Calculate the days between now and last entry
        dateDelta = (today - latestEntryDate).days
        
        # If weight has changed by greater then 2 kg a day since last entry, then send notification
        if (dateDelta > 0):
            if abs(value - latestEntry)/dateDelta >= 2:
                with conn.cursor() as cur:
                    email = ''
                    try:
                        compatibleDate = todayDate.replace('/', '')
                        cur.execute("INSERT INTO notificationHistoryTable (patientID, dateOfSending, notiTitle, notiDesc) VALUES ({0}, {1}, {2}, {3})".format(patientID, compatibleDate, "'Substantial Weight Change'", "'A change to your weight this drastic could indicate an underlying problem or cause serious complications, please consult your doctor'"))
                        cur.execute("SELECT email FROM patientDataTable WHERE patientID = {0};".format(patientID))
                        email = cur.fetchone()[0]
                        cur.execute("UPDATE loginTable SET unreadNotis = unreadNotis + 1 WHERE patientID = {0};".format(patientID))
                        send_notification(email , "Substantial weight change", "A change to your weight this drastic could indicate an underlying problem or cause serious complications, please consult your doctor");
                    except Exception as e:
                        return str(e)

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
    
def send_notification(target, title, description):
    SENDER = "Patient Notifier System <patient.notifier.system.dev@gmail.com>"
    
    AWS_REGION = "ap-southeast-2"
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    target,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': description,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': description,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': title,
                },
            },
            Source=SENDER,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
    return True
    
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