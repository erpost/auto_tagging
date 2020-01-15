import boto3
import os


def get_profiles():
    credentials = os.path.expanduser('~/.aws/access_keys/credentials')
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = credentials
    session_profiles = boto3.session.Session().available_profiles
    aws_profiles = []

    for session_profile in session_profiles:
        aws_profiles.append(session_profile)

    return aws_profiles


def get_regions(aws_profile):
    boto3.setup_default_session(profile_name=aws_profile, region_name='us-east-1')
    client = boto3.client('ec2')
    aws_regions = []
    response = client.describe_regions()

    for region in response['Regions']:
        aws_regions.append(region['RegionName'])

    return aws_regions


def get_ec2(aws_profile, aws_region):
    boto3.setup_default_session(profile_name=aws_profile, region_name=aws_region)
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        state = instance.state['Name']
        if state != 'terminated':

            # Pull CloudID
            cloud_id = instance.id

            # Pull DeviceFQDN - Private
            try:
                priv_dns = instance.private_dns_name
            except AttributeError:
                priv_dns = 'None'

            # Pull DeviceFQDN - Public
            try:
                pub_dns = instance.public_dns_name
            except AttributeError:
                pub_dns = 'None'

            # Pull Device Category (Hardcoded)
            device_cat = 'Cloud'

            # Pull DeviceType (Hardcoded)
            device_type = 'IaaS'

            # Pull DeviceMake (Hardcoded)
            device_make = 'AWS'

            # Pull DeviceModel (Hardcoded)
            device_model = 'EC2'

            # Pull FacilityID
            facility_id = instance.placement['AvailabilityZone']

            # Pull IPAddress - Private
            priv_ip = instance.private_ip_address

            # Pull IPAddress - Public
            pub_ip = instance.public_ip_address

            # Pull IPAddressAgencyOwned
            interfaces = instance.network_interfaces_attribute
            for interface in interfaces:
                try:
                    ip_owner = interface['Association']['IpOwnerId']
                except KeyError:
                    ip_owner = 'N/A'

            # Pull InterfaceName
            interfaces = instance.network_interfaces
            for interface in interfaces:
                int_name = interface.id

            # Pull MACAddress
            interfaces = instance.network_interfaces_attribute
            for interface in interfaces:
                mac = interface['MacAddress']

                # Pull FacilityType (Hardcoded)
                facility_type = 'AWS'

    return cloud_id, priv_dns, pub_dns, device_cat, device_type, device_make, device_model, facility_id, priv_ip,\
           pub_ip, ip_owner, int_name, mac, facility_type


if __name__ == '__main__':
    profiles = get_profiles()
    regions = get_regions(profiles[0])
    print(regions)
    print(profiles)
    ec2s = get_ec2(profiles[0], 'us-east-1')
    print(ec2s)
