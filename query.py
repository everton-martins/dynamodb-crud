import boto3, json, sys, decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



TABLE_NAME='AUDIT_LOG'
GSI_NAME='timestamp-index'
GSI_FIELD_NAME='timestamp'
QUERY_PARAMETER=1549567956336
PK_FIELD='requestId'
SK_FIELD='timestamp'


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

##GET ITEM
try:
    response = table.query(IndexName=GSI_NAME,KeyConditionExpression=Key(GSI_FIELD_NAME).eq(QUERY_PARAMETER))
	
except ClientError as e:
    sys.exit(1, e.response['Error']['Message'] )
else:
    item = response['Items'][0]
    print("GetItem succeeded:")
    print(json.dumps(item, indent=4, cls=DecimalEncoder))
