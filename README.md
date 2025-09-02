# Spotify Artist Momentum Tracker

This project is an end-to-end, serverless data platform built on AWS that ingests, processes, and analyzes Spotify artist data to track performance metrics and correlate popularity trends with new music releases.

## Live Dashboard
https://us-east-1.quicksight.aws.amazon.com/sn/account/crich-quicksight/dashboards/a73096cb-162e-4a04-962c-736b152daae3
> **Note:** Due to AWS QuickSight's pricing for public dashboards, this dashboard is shared privately. Access can be granted upon request for a live demonstration.

---

## Architecture
The entire platform is automated and built on a serverless architecture, with all infrastructure managed as code using Terraform.

--put diagram here--

### Tech Stack
* **Cloud:** AWS (Lambda, S3, Glue, Athena, EventBridge, Step Functions, IAM)
* **Infrastructure as Code:** Terraform
* **Data Processing:** Python (Spotipy, Boto3), SQL
* **Data Storage:** S3 Data Lake (partitioned, JSON Lines & Parquet formats)
* **BI & Visualization:** Amazon QuickSight

---

## Key Features
* **Automated Data Pipelines:** Two separate, serverless Lambda functions run on automated schedules (daily for metrics, weekly for releases) using EventBridge.
* **Stateful Discography Tracking:** The weekly pipeline is stateful, comparing the current discography to the previous week's to identify and log only new releases.
* **Data Transformation at Scale:** An orchestrated ETL/ELT job using AWS Step Functions and Athena (with `CREATE TABLE AS SELECT`) transforms raw, partitioned data into a clean, analytics-ready table.
* **Interactive Analytics Dashboard:** A QuickSight dashboard that allows users to select an artist and view their follower trends over time, with visual cues marking the dates of new music releases.


## Showcase 

<img width="1040" height="802" alt="image" src="https://github.com/user-attachments/assets/1cafb109-8a76-4062-8fc1-70e54498524c" />

<img width="1042" height="804" alt="image" src="https://github.com/user-attachments/assets/1613df42-6064-4eb1-8031-5fbb569baa79" />


These are two artists that inspired me to create this project in the first place. They are smaller artists, but we can see from their most recent drops that they are growing rapidly in followers.
