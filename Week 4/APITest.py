import requests

#x = requests.get("https://82jxgqb1kb.execute-api.ap-southeast-2.amazonaws.com/Initial-Testing?tableName=employees")
x = requests.post("https://82jxgqb1kb.execute-api.ap-southeast-2.amazonaws.com/Initial-Testing?employee_id=420&first_name=Jordan&last_name=Reid_Smith&email=coolkidemail&phone_number=6942069&hire_date=2022-08-03&job_id=4&salary=69000.00&manager_id=NULL&department_id=9")
print(str(x.text))