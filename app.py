import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')
SLACK_QUEUE = os.getenv('SQS_NAME')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return jsonify(dict(os.environ))


@app.route("/users/<string:user_id>")
def get_user(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': { 'S': user_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S')
    })


@app.route("/users", methods=["POST"])
def create_user():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({'error': 'Please provider userId and name'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id },
            'name': {'S': name }
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name
    })

def generate_message_attributes(dict1):
    return {key: {'StringValue': value, 'DataType': 'String'} for (key, value) in dict1.items() if value != ''}

@app.route("/slack", methods=["POST"])
def handle_slack_message():
    # sqs = boto3.resource('sqs')
    SQS_CLIENT = boto3.client('sqs')
    # queue = sqs.get_queue_by_name(QueueName=SLACK_QUEUE)
    body = request.form.to_dict(flat=True)
    message_attributes = generate_message_attributes(body)

    # print(queue.send_message(MessageBody="test", MessageAttributes=body))
    print(SQS_CLIENT.send_message(
        QueueUrl=os.getenv('SQS_URL'),
        MessageBody='test',
        MessageAttributes=message_attributes
    ))

    return jsonify({
        'text': "Thanks, your request is being processed."
    })
