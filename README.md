# Cryptocurrency Trade Monitoring Platform

## Table of Contents
- [Introduction](#introduction)
- [Project Architecture](#project-architecture)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Prerequisites](#prerequisites)

---

## Introduction

This project monitors cryptocurrency trade data in real-time using Apache Kafka, DynamoDB, and AWS services. It captures trade data, stores it in DynamoDB, triggers alerts using SNS, and performs analytics using Athena, while visualizing insights in QuickSight.

### Key Features:
- **Real-time Data Stream**: Capture and process live cryptocurrency trade data.
- **Data Persistence**: Store trade data in DynamoDB for historical reference.
- **Price Alerts**: Receive notifications via AWS SNS when the price drops below a predefined threshold.
- **Data Analytics**: Perform queries and analysis on stored data using AWS Athena.
- **Visualization**: Gain insights through dashboards and reports created in AWS QuickSight.

---

## Project Architecture

<img width="409" alt="Screenshot 2024-10-06 at 10 04 34 PM" src="https://github.com/user-attachments/assets/6d3a89a5-7241-40b1-b68e-ef6fd53c0c19">

## Features

**Real-time Crypto Trade Monitoring**: Continuously streams cryptocurrency trade data (e.g., BTC/USDT) through Apache Kafka.

**Automated Data Storage**: Stores trade data into DynamoDB for historical analysis.

**Threshold-based Alerts**: Sends alerts via AWS SNS when prices fall below a set threshold.

**Analytics with Athena**: Query trade data using AWS Athena for historical and trend analysis.

**Visualizations with QuickSight**: Generate insightful reports and dashboards on trade data using AWS QuickSight.


## Setup Instructions

Follow these instructions to set up and run the cryptocurrency trade monitoring platform on your local machine.

## Prerequisites

Before you begin, ensure you have met the following requirements:

•**Docker** installed on your system for running Kafka.

•**AWS Account** with access to DynamoDB, SNS, Athena, and QuickSight services.

•**Python 3.x** installed.

•AWS CLI configured on your machine.



	1.	Set up Kafka using Docker by running the following commands:
     docker-compose up -d

   
