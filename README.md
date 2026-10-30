Markdown
  Cloud Compliance & Security Scanner

An automated DevSecOps portfolio project designed to spin up intentionally vulnerable cloud infrastructure and programmatically audit it for compliance misconfigurations.

 Project Overview
In modern cloud environments, security misconfigurations (such as public S3 buckets or open administrative ports) are leading causes of data breaches. This project demonstrates an end-to-end security pipeline:
1. Infrastructure as Code (IaC): Deploys cloud resources with intentional security flaws using Terraform.
2. Local Cloud Emulation: Simulates AWS locally using LocalStack (Community Edition).
3. Automated Compliance Audit:** A custom Python script leveraging `boto3` to inspect live resources and flag security violations.

---

 Architecture & Tech Stack
* Cloud Emulator: LocalStack (v3.8.0) via Docker Compose
* Provisioning Tool: Terraform
* Audit Script: Python 3 (`boto3`, `botocore`)
* Audited Resources:
  * Amazon S3: Scans for public access block misconfigurations.
  * Amazon EC2 Security Groups: Detects unrestricted inbound traffic (`0.0.0.0/0`) on sensitive ports (e.g., SSH port 22).

---

 Getting Started & Local Setup

 Prerequisites
* Docker & Docker Compose
* Terraform
* Python 3 & Boto3

 1. Clone the Repository
```bash
git clone [https://github.com/IzumiYuna/cloud-compliance-scanner.git](https://github.com/IzumiYuna/cloud-compliance-scanner.git)
cd cloud-compliance-scanner
2. Start LocalStack
Bash
sudo docker compose up -d
3. Deploy Vulnerable Infrastructure
Bash
cd terraform
terraform init
terraform apply -auto-approve
cd ..
4. Run the Compliance Audit Script
Bash

python3 scanner.py

 Sample Audit Output
When executed against the misconfigured infrastructure, the Python scanner successfully catches and flags the vulnerabilities:

Plaintext
=== Starting Cloud Compliance & Security Audit ===

[*] Auditing S3 Buckets for Public Access...
 -> Checking bucket: my-unsafe-company-bucket-12345
   [!] VULNERABILITY FOUND: S3 Bucket 'my-unsafe-company-bucket-12345' has public access blocks disabled!

[*] Auditing Security Groups for Open Ingress Ports...
 -> Checking Security Group: unsafe_sg (sg-3da37a9a0b54fd309)
   [!] VULNERABILITY FOUND: Security Group 'unsafe_sg' allows unrestricted access (0.0.0.0/0) on SSH port 22!

=== Audit Complete ===
 Future Enhancements
Export audit findings into structured JSON / HTML reports.

Integrate static analysis tools like Checkov into the workflow.

Add GitHub Actions CI/CD pipeline automation.
