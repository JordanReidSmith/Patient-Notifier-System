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
    
    table = event['table_name']
    
    if table == "employees":
        employeeInsert(event, conn)
    elif table == "region":
        regionInsert(event, conn)
    
    # Return success 
    return {
        'statusCode': 200,
        'body': json.dumps("All good")
    }
    
def regionInsert(event, conn):
    regionId = event['region_id']
    regionName = event['region_name']
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO regions(region_id, region_name) VALUES ({0},'{1}');".format(regionId, regionName))
        except Exception as e:
            return str(e)
        for row in cur:
            results.append(row)
    conn.commit()
    
def employeeInsert(event, conn):
    employee_id = event['employee_id']
    first_name = event['first_name']
    last_name = event['last_name']
    email = event['email']
    phone_number = event['phone_number']
    hire_date = event['hire_date']
    job_id = event['job_id']
    salary = event['salary']
    manager_id = event['manager_id']
    department_id = event['department_id']

    with conn.cursor() as cur:
        try:
            #cur.execute("select * from " + event['tableName']);
            cur.execute("INSERT INTO employees(employee_id,first_name,last_name,email,phone_number,hire_date,job_id,salary,manager_id,department_id) VALUES ({0},'{1}','{2}','{3}','{4}','{5}',{6},{7},{8},{9});".format(employee_id, first_name, last_name, email, phone_number, hire_date, job_id, salary, manager_id, department_id))
        except Exception as e:
            return str(e)
        for row in cur:
            results.append(row)
    conn.commit()
    
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