import json
import pymysql
import boto3

def lambda_handler(event, context):
    creds = get_secret()
    # Attempt connection to MySQL server
    try:
        conn = pymysql.connect(host=creds['host'], user=creds['username'], passwd=creds['password'], db="test_schema", connect_timeout=5)
    except pymysql.MySQLError as e:
        # If connection failed, report back exception and end execution
        return {
        'statusCode': 69,
        'body': json.dumps(str(e))
    }
    
    results = []
    # Execute SQL select command and print all results
    with conn.cursor() as cur:
        #cur.execute(event['key1']);
        try:
            cur.execute("select * from " + event['tableName']);
        except:
            cur.execute("select * from regions");
        for row in cur:
            #print(row)
            results.append(row)
    conn.commit()
    
    # Return success 
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
    
def get_secret():
    # Secret manager reference
    secret_name = "Jordan-RDS-Cred"
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