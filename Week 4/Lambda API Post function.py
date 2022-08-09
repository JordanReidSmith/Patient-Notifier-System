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
    
    # Return success 
    return {
        'statusCode': 200,
        'body': json.dumps("All good")
    }