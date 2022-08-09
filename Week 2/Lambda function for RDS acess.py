import json
import pymysql

def lambda_handler(event, context):
    # Attempt connection to MySQL server
    try:
        conn = pymysql.connect(host="jordan-sample-lambda-database.c0ls2h2typle.ap-southeast-2.rds.amazonaws.com", user="admin", passwd="LkE205Sl2I", db="test_schema", connect_timeout=5)
    except pymysql.MySQLError as e:
        # If connection failed, report back exception and end execution
        return {
        'statusCode': 69,
        'body': json.dumps(str(e))
    }
    
    # Execute SQL select command and print all results
    with conn.cursor() as cur:
        cur.execute(event['key1']);
        for row in cur:
            print(row)
    conn.commit()
    
    # Return success 
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }