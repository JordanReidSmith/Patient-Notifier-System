import requests

x = requests.get("https://ha5xzicekb.execute-api.ap-southeast-2.amazonaws.com/First-Deployment?table_name=region")


#x = requests.post("https://lv1vhxh4g9.execute-api.ap-southeast-2.amazonaws.com/First-Deployment?table_name=region&region_id=7&region_name=Mars")


#x = requests.post("https://lv1vhxh4g9.execute-api.ap-southeast-2.amazonaws.com/First-Deployment?table_name=employees&employee_id=420&first_name=Jordan&last_name=Reid_Smith&email=coolkidemail&phone_number=6942069&hire_date=2022-08-03&job_id=4&salary=69000.00&manager_id=NULL&department_id=9")
print(str(x.text))