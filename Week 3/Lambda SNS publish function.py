import json
import boto3

#sns_wrapper.publish_message(topic, "Hello! This message is mobile friendly.", {mobile_key: friendly})

def lambda_handler(event, context):
    
    client = boto3.client("sns")
    response = client.publish(TopicArn = "arn:aws:sns:ap-southeast-2:931299814805:Jordan-test-topic", Message=event['key1'])
            
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
