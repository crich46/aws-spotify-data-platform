# Spotify Artist Momentum Tracker

This project is an end-to-end, serverless data platform built on AWS that ingests, processes, and analyzes Spotify artist data to track performance metrics and correlate popularity trends with new music releases.

## Live Dashboard
https://us-east-1.quicksight.aws.amazon.com/sn/account/crich-quicksight/dashboards/a73096cb-162e-4a04-962c-736b152daae3
> **Note:** Due to AWS QuickSight's pricing for public dashboards, this dashboard is shared privately. Access can be granted upon request for a live demonstration.

---

## Architecture
The entire platform is automated and built on a serverless architecture, with all infrastructure managed as code using Terraform.

<img width="1125" height="691" alt="SpotifyArtistTracker drawio" src="https://github.com/user-attachments/assets/054d747c-5527-4c28-aa1c-98000ea6416b" />

### 1. Automated Data Ingestion
Two **AWS Lambda** functions run on separate, automated schedules managed by **Amazon EventBridge**. A daily function collects time-series performance metrics (followers, popularity), while a weekly function fetches full artist discographies to identify new releases. All raw data is written to an **Amazon S3** data lake in a partitioned, JSON Lines format. I use the JSON Lines format here because it makes it much quicker and easier to query later with SQL.

### 2. Data Cataloging & Transformation
Scheduled **AWS Glue Crawlers** run after the ingestion jobs to automatically scan the raw data and update the metadata tables in the **AWS Glue Data Catalog**. A daily **AWS Step Function** then orchestrates a series of **Amazon Athena** SQL queries to drop and recreate a final, processed analytics table. This transformation job joins the raw datasets, engineers key metrics like follower growth, and saves the result in the efficient, partitioned Parquet format.

### 3. Interactive Visualization
The final, processed table in Athena serves as the direct data source for an **Amazon QuickSight** dashboard. The dashboard uses a **SPICE** dataset with an automated daily refresh, allowing for fast, interactive analysis of artist momentum and the correlation between follower growth and new music releases.

---

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
