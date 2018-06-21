import boto3
import paramiko
import time
import logging
import os

logging.basicConfig(format='[%(levelname)s %(asctime)s] %(message)s', level=logging.INFO)

class ChartyInstance(object):
    """
    Support the creation and installation of instances running the charty app.
    """

    # Use an instance type in AWS' free tier, otherwise fees will accrue
    EC2_INSTANCE_TYPE = 't2.micro'

    # AMI ID of recent Ubuntu 16.04 LTS
    AMI = 'ami-95a977ea'

    # SSH key pair
    KEY_NAME = 'ops_code_test'
    KEY_FILE_NAME = os.path.expanduser('~/{}.pem'.format(KEY_NAME))

    # Username of account on Ubuntu servers
    USERNAME = 'ubuntu'

    SSH_RETRY_DELAY_IN_SECS = 3
    SSH_MAX_RETRIES = 5

    # Location of Git hosting provider private key, locally and on instance
    GIT_SOURCE_PRIVATE_KEY_FILE_NAME = os.path.expanduser('~/.ssh/id_rsa')
    GIT_DESTINATION_PRIVATE_KEY_FILE_NAME = '.ssh/id_rsa'

    CHARTY_TCP_PORT = 8000
    SSH_TCP_PORT = 22
    CIDR_ANYWHERE = '0.0.0.0/0'

    def __init__(self):
        """
        Initialize.
        """
        self._session = boto3.Session()
        self._ec2 = self._session.resource('ec2')
        self._ec2_client = boto3.client('ec2')
        self._security_group_id = None
        self._instance = None
        self._ssh_client = None

    def __str__(self):
        """
        Return a string representation of an instance.
        """
        return self._instance.id

    def createKeyPair(self):
        """
        Create a key pair to be used for SSH sessions.
        """
        if not os.path.isfile(self.KEY_FILE_NAME):
            logging.warning("key file named '{}' does not exist; creating key pair named '{}' and saving to key file".format(self.KEY_FILE_NAME, self.KEY_NAME))
            key_pair = self._ec2.create_key_pair( KeyName=self.KEY_NAME, )
            with open(self.KEY_FILE_NAME, 'w') as key_file:
                key_file.write(key_pair.key_material)
                key_file.write("\n")
                key_file.close()
            os.chmod(self.KEY_FILE_NAME, 0o600)

    def createSecurityGroup(self):
        """
        Create a security group in the default VPC, and permission incoming access to SSH and the charty app.
        """
        vpcs_response = self._ec2_client.describe_vpcs()
        vpc_id = vpcs_response.get('Vpcs', [{}])[0].get('VpcId', '')

        security_group_response = self._ec2_client.create_security_group( GroupName='charty', Description='Charty', VpcId=vpc_id)
        security_group_id = security_group_response['GroupId']
        ingress_response = self._ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                { 'IpProtocol': 'tcp',
                  'FromPort': self.SSH_TCP_PORT,
                  'ToPort': self.SSH_TCP_PORT,
                  'IpRanges': [ { 'CidrIp': self.CIDR_ANYWHERE } ] },
                { 'IpProtocol': 'tcp',
                  'FromPort': self.CHARTY_TCP_PORT,
                  'ToPort': self.CHARTY_TCP_PORT,
                  'IpRanges': [ { 'CidrIp': self.CIDR_ANYWHERE } ] },
            ] )
        logging.info("created security group ID '{}' in VPC ID '{}'".format(security_group_id, vpc_id))

        self._security_group_id = security_group_id

    def create(self):
        """
        Create an EC2 instance.
        """
        # TODO:
        # Create an EC2 instance using EC2_INSTANCE_TYPE, AMI, and KEY_NAME, in the proper security group.
        # Wait until the instance is running, and ensure the public IP address attribute has been set.

        self._instance = instance

    def connectSSH(self):
        """
        Start an SSH session.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False
        retries_remaining = self.SSH_MAX_RETRIES
        while not connected and retries_remaining > 0:
            try:
                logging.info("connecting to {}@{} via SSH using key file named '{}'".format(self.USERNAME, self._instance.public_ip_address, self.KEY_FILE_NAME))
                client.connect(hostname=self._instance.public_ip_address, username=self.USERNAME,
                               pkey=paramiko.RSAKey.from_private_key_file(self.KEY_FILE_NAME))
                connected = True
            except paramiko.ssh_exception.NoValidConnectionsError, e:
                logging.warning('unable to connect; will retry in {} seconds'.format(self.SSH_RETRY_DELAY_IN_SECS))
                time.sleep(self.SSH_RETRY_DELAY_IN_SECS)
                retries_remaining -= 1
                pass
        if retries_remaining == 0:
            error_message = 'unable to connect after {} retries; aborting'.format(self.SSH_MAX_RETRIES)
            logging.critical(error_message)
            raise ValueError(error_message)

        self._ssh_client = client

    def putCredentials(self):
        """
        Install the Git hosting provider private key on the instance.
        """
        # TODO

    def runRemoteCommand(self, command):
        """
        Run a command via SSH.
        Return the command's standard output and error.
        """
        # TODO:
        # Log the command and run it on the instance.
        # If an error exit status, log and raise an error.

    def installCharty(self):
        """
        Install the charty app.
        """
        # TODO:
        # Clone the charty sources from the Git hosting provider repo into a directory named ~/Code/lib, and install the app.
        logging.info('charty is available at http://{}:{}/'.format(self._instance.public_ip_address, self.CHARTY_TCP_PORT))

    def disconnectSSH(self):
        """
        Close the SSH session.
        """
        self._ssh_client.close()

def main():
    chartyInstance = ChartyInstance()
    chartyInstance.createKeyPair()
    chartyInstance.createSecurityGroup()
    chartyInstance.create()
    chartyInstance.connectSSH()
    chartyInstance.putCredentials()
    chartyInstance.installCharty()
    chartyInstance.disconnectSSH()

main()
