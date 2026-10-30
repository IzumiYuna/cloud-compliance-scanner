import boto3
from botocore.exceptions import ClientError

# Point Boto3 to your local LocalStack instance
LOCALSTACK_ENDPOINT = "http://localhost:4566"
REGION = "us-east-1"
CREDENTIALS = {"aws_access_key_id": "test", "aws_secret_access_key": "test"}

def audit_s3_buckets():
    print("\n[*] Auditing S3 Buckets for Public Access...")
    s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_ENDPOINT, region_name=REGION, **CREDENTIALS)
    
    try:
        response = s3_client.list_buckets()
        for bucket in response.get("Buckets", []):
            bucket_name = bucket["Name"]
            print(f" -> Checking bucket: {bucket_name}")
            
            # Check Public Access Block configuration
            try:
                pab = s3_client.get_public_access_block(Bucket=bucket_name)
                config = pab.get("PublicAccessBlockConfiguration", {})
                if not all(config.values()):
                    print(f"   [!] VULNERABILITY FOUND: S3 Bucket '{bucket_name}' has public access blocks disabled!")
            except ClientError:
                print(f"   [!] VULNERABILITY FOUND: S3 Bucket '{bucket_name}' has no public access block configured!")
                
    except Exception as e:
        print(f"   [-] Error listing S3 buckets: {e}")

def audit_security_groups():
    print("\n[*] Auditing Security Groups for Open Ingress Ports...")
    ec2_client = boto3.client("ec2", endpoint_url=LOCALSTACK_ENDPOINT, region_name=REGION, **CREDENTIALS)
    
    try:
        response = ec2_client.describe_security_groups()
        for sg in response.get("SecurityGroups", []):
            sg_name = sg.get("GroupName")
            sg_id = sg.get("GroupId")
            print(f" -> Checking Security Group: {sg_name} ({sg_id})")
            
            for rule in sg.get("IpPermissions", []):
                from_port = rule.get("FromPort", 0)
                to_port = rule.get("ToPort", 65535)
                
                for ip_range in rule.get("IpRanges", []):
                    cidr = ip_range.get("CidrIp")
                    if cidr == "0.0.0.0/0" and from_port <= 22 <= to_port:
                        print(f"   [!] VULNERABILITY FOUND: Security Group '{sg_name}' allows unrestricted access (0.0.0.0/0) on SSH port 22!")
                        
    except Exception as e:
        print(f"   [-] Error describing security groups: {e}")

if __name__ == "__main__":
    print("=== Starting Cloud Compliance & Security Audit ===")
    audit_s3_buckets()
    audit_security_groups()
    print("\n=== Audit Complete ===")
