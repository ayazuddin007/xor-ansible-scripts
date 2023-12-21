from kubernetes.client.rest import ApiException
from kubernetes import client, config
import sys,time
import boto3


def createR53record():
    privateId = findHostedZoneId()
    privateEntry(privateId)

# to retrieve private zone id
def findHostedZoneId():
    try:
        response = r_client.list_hosted_zones()
        for i in response['HostedZones'] :
            if i['Name'] == sys.argv[2]+'.' and i['Config']['PrivateZone'] == True:
                privateId=i['Id'].split("/", -1)[2]
                # print('private Zone Id : {}' .format(privateId))

    except ApiException as e:
        print('Found exception')
    return privateId

# to make entry in private zone
def privateEntry(zone_id):
    services = {'ifcs-messaging-activemq': 'ifcs-activemq','ifcs-transauth-server-jpos': 'ifcs-transauth'}
    for service,alias in services.items():
        try:
            api_response = api_instance.read_namespaced_service_status(service, sys.argv[3]+"-"+sys.argv[1])
        # print(api_response.status.load_balancer.ingress[0].hostname)
        # print(alias)
        except:
            continue
        response = r_client.list_resource_record_sets(
            HostedZoneId=zone_id
        )
        # check if entry already exists 
        if any (i['Name'] == alias+'.'+sys.argv[1]+'.'+sys.argv[2]+'.' and i['ResourceRecords'][0]['Value'] == api_response.status.load_balancer.ingress[0].hostname for i in response['ResourceRecordSets']) :
            print('CNAME record for '+alias+' already exists')
        else:
            res = r_client.change_resource_record_sets(
                ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': {
                                    'Name': alias+'.'+sys.argv[1]+'.'+sys.argv[2],
                                    'ResourceRecords': [
                                        {
                                            'Value': api_response.status.load_balancer.ingress[0].hostname,
                                        },
                                    ],
                                    'Type': 'CNAME',
                                    'TTL': 300
                                },
                            }
                        ]
                    },
                    HostedZoneId=zone_id
                )
            print('CNAME record for '+alias+ 'created' )


if __name__ == "__main__":
    r_client = boto3.client('route53')
    config.load_kube_config()
    api_instance = client.CoreV1Api()
    time.sleep(7)
    createR53record()

#sys.argv[1]=environmentSubDomain sys.argv[2]=envBaseDomain sys.argv[3]=clientName
