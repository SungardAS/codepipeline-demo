import sys
import os
import requests
import json
import boto3

code_pipeline = boto3.client('codepipeline')


# def ascii_encode_dict(data):
#     ascii_encode = lambda x: x.encode('ascii')
#     return dict(map(ascii_encode, pair) for pair in data.items())


def send_post(event, context):
  """Notify Slack of CodePipeline event
  Args:
    event: The CodePipeline json input
    context: lambda execution context
  """
  jobId = event['CodePipeline.job']['id']

  #Get userparameters string and decode as json
  user_parameters = event['CodePipeline.job']['data']['actionConfiguration']['configuration']['UserParameters']

  # decoded_parameters = json.loads(user_parameters, object_hook=ascii_encode_dict)
  decoded_parameters = json.loads(user_parameters)
  print(decoded_parameters)

  webhook = decoded_parameters['webhooks']
  message = decoded_parameters['message']

  #Slack webhook post
  try:
    response = requests.post(webhook, headers={"Content-Type": "application/json"}, data=json.dumps({"text": message}))
    print response.text
    response.raise_for_status()
    code_pipeline.put_job_success_result(jobId=jobId)
  except requests.ConnectionError:
  	code_pipeline.put_job_failure_result(jobId=jobId)

