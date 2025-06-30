import boto3
from datetime import datetime, timedelta

IDLE_DAYS = 7
LOW_CPU_THRESHOLD = 5  # percent

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
lambda_client = boto3.client('lambda')
ecs = boto3.client('ecs')


def stop_idle_ec2(dry_run=True):
    print("\n[EC2] Checking for idle instances...")
    reservations = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])['Reservations']

    for res in reservations:
        for instance in res['Instances']:
            instance_id = instance['InstanceId']
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.utcnow() - timedelta(days=IDLE_DAYS),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )
            data = metrics.get('Datapoints', [])
            avg = sum(d['Average'] for d in data) / len(data) if data else 0
            if avg < LOW_CPU_THRESHOLD:
                print(f"Idle EC2 instance {instance_id} (Avg CPU: {avg:.2f}%)")
                if dry_run:
                    print(f"[Dry run] Would stop instance: {instance_id}")
                else:
                    ec2.stop_instances(InstanceIds=[instance_id])


def delete_unused_volumes(dry_run=True):
    print("\n[EBS] Deleting unattached volumes...")
    volumes = ec2.describe_volumes(Filters=[
        {'Name': 'status', 'Values': ['available']}
    ])['Volumes']
    for v in volumes:
        print(f"Unattached volume: {v['VolumeId']}")
        if dry_run:
            print(f"[Dry run] Would delete volume: {v['VolumeId']}")
        else:
            ec2.delete_volume(VolumeId=v['VolumeId'])


def delete_unused_elastic_ips(dry_run=True):
    print("\n[Elastic IP] Releasing unused IPs...")
    addresses = ec2.describe_addresses()['Addresses']
    for addr in addresses:
        if 'InstanceId' not in addr:
            print(f"Unused Elastic IP: {addr['PublicIp']}")
            if dry_run:
                print(f"[Dry run] Would release Elastic IP: {addr['PublicIp']}")
            else:
                ec2.release_address(AllocationId=addr['AllocationId'])


def delete_unattached_enis(dry_run=True):
    print("\n[ENI] Deleting unattached network interfaces...")
    enis = ec2.describe_network_interfaces(Filters=[
        {'Name': 'status', 'Values': ['available']}
    ])['NetworkInterfaces']
    for eni in enis:
        print(f"Unattached ENI: {eni['NetworkInterfaceId']}")
        if dry_run:
            print(f"[Dry run] Would delete ENI: {eni['NetworkInterfaceId']}")
        else:
            ec2.delete_network_interface(NetworkInterfaceId=eni['NetworkInterfaceId'])


def stop_idle_rds(dry_run=True):
    print("\n[RDS] Checking for idle RDS instances...")
    dbs = rds.describe_db_instances()['DBInstances']
    for db in dbs:
        db_id = db['DBInstanceIdentifier']
        if db['DBInstanceStatus'] == 'available':
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': db_id}],
                StartTime=datetime.utcnow() - timedelta(days=IDLE_DAYS),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )
            data = metrics.get('Datapoints', [])
            avg = sum(d['Average'] for d in data) / len(data) if data else 0
            if avg < LOW_CPU_THRESHOLD:
                print(f"Idle RDS instance {db_id} (Avg CPU: {avg:.2f}%)")
                if dry_run:
                    print(f"[Dry run] Would stop RDS instance: {db_id}")
                else:
                    rds.stop_db_instance(DBInstanceIdentifier=db_id)


def report_idle_lambdas():
    print("\n[Lambda] Reporting idle functions (no invocations)...")
    funcs = lambda_client.list_functions()['Functions']
    for fn in funcs:
        fn_name = fn['FunctionName']
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName='Invocations',
            Dimensions=[{'Name': 'FunctionName', 'Value': fn_name}],
            StartTime=datetime.utcnow() - timedelta(days=IDLE_DAYS),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=['Sum']
        )
        data = metrics.get('Datapoints', [])
        total = sum(d['Sum'] for d in data) if data else 0
        if total == 0:
            print(f"Idle Lambda function: {fn_name} (No invocations in last {IDLE_DAYS} days)")


def stop_idle_ecs_services(dry_run=True):
    print("\n[ECS] Stopping unused services...")
    clusters = ecs.list_clusters()['clusterArns']
    for cluster in clusters:
        services = ecs.list_services(cluster=cluster)['serviceArns']
        for svc in services:
            desc = ecs.describe_services(cluster=cluster, services=[svc])['services'][0]
            if desc['desiredCount'] == 0 and desc['runningCount'] == 0:
                print(f"Idle ECS service: {svc}")
                if dry_run:
                    print(f"[Dry run] Would delete ECS service: {svc}")
                else:
                    ecs.delete_service(cluster=cluster, service=svc, force=True)
