#!/usr/bin/env python3
import boto3
import csv

def create_table(ddb_table_name,partition_key):
    dynamodb = boto3.resource('dynamodb')
    try:
        table = dynamodb.create_table(TableName=ddb_table_name,
                                        KeySchema=[{'AttributeName': partition_key, 'KeyType': 'HASH'}],
                                        AttributeDefinitions=[{'AttributeName': partition_key, 'AttributeType': 'S'}],
                                        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10}
                                    )
        return table
    except Exception as err:
        print("{0} Table could not be created".format(table_name))
        print("Error message {0}".format(err))

def insert_items(ddb_table_name,filename):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(ddb_table_name)
    
    with open(filename) as theFile:
        reader = csv.DictReader(theFile)
        for line in reader:
            item = {}
            for key in line.keys():
                item[key] = line[key]
            table.put_item(Item=item)

def update_item(ddb_table_name,pk,pk_value,attr,attr_value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(ddb_table_name)
    
    response = table.update_item(
        Key={
            pk: pk_value
        },
        UpdateExpression="set #a=:a",
        ExpressionAttributeNames={ '#a': attr },
        ExpressionAttributeValues={ ':a': attr_value },
        ReturnValues="UPDATED_NEW"
    )
    return response
        
def delete_table(ddb_table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(ddb_table_name)
    table.delete()

if __name__ == '__main__':
    # CREATE TABLE
    infections_table = create_table("infections", "PatientId")
    
    # INSERT ITEMS
    insert_items("infections","infections.csv")
    
    # UPDATE ITEMS
    update_item('infections','PatientId','1','PatientReportUrl','https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord1.txt')
    update_item('infections','PatientId','2','PatientReportUrl','https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord2.txt')
    update_item('infections','PatientId','3','PatientReportUrl','https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord3.txt')
    
    #DELETE TABLE
    # delete_table('infections')