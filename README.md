# AWS Resource Cleaner
- This tool helps you automatically detect and clean idle or unused AWS resources.

## What It Does
## This tool safely detects and optionally stops or deletes unused cloud resources
- Stops EC2 instances with low CPU
- Deletes unattached EBS volumes
- Releases unused Elastic IPs
- Deletes unattached ENIs
- Stops idle RDS instances
- Reports idle Lambda functions
- Deletes idle ECS services


## Features

- `dry_run=True` by default to avoid accidental changes
- Logs to both console and `cleaner.log` file
- Simple structure for local use, cron automation, or GitHub Actions
- Modular Python design for easy extension



##  Getting Started
- git clone https://github.com/Copubah/aws-resource-cleaner.git
- cd aws-resource-cleaner
- python3 -m venv venv
- source venv/bin/activate


## Setup
1. Install dependencies
- pip install -r requirements.txt

2. Configure AWS credentials
- aws configure

3. Run the cleaner(Safe mode)
- python run.py


## Run the Script
- To perform actual cleanup, edit run.py and set: 
- dry_run = False

## ⚠️ Use this tool with caution. It can stop or delete live resources.


## Automation
- You can automate the script with:
- Cron on Linux/macOS (e.g. daily midnight run)
- GitHub Actions 

## Security
- Make sure you use limited-permission AWS credentials and never hardcode secrets. Use IAM roles or environment variables with AWS CLI configuration.


## License
- MIT License. See LICENSE for details.


👤 Author
Charles Opuba
GitHub: @Copubah




