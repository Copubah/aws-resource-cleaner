# AWS Resource Cleaner
- This tool helps you automatically detect and clean idle or unused AWS resources.

## What It Does
- Stops EC2 instances with low CPU
- Deletes unattached EBS volumes
- Releases unused Elastic IPs
- Deletes unattached ENIs
- Stops idle RDS instances
- Reports idle Lambda functions
- Deletes idle ECS services

## Setup
1. Install dependencies
- pip install -r requirements.txt

2. Configure AWS credentials
- aws configure

3. Run the cleaner
- python run.py

## ⚠️ Use this tool with caution. It can stop or delete live resources.




