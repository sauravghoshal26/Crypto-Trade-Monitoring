# Cryptocurrency Trade Monitoring Platform

## Table of Contents
- [Introduction](#introduction)
- [Project Architecture](#project-architecture)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Kafka Setup](#kafka-setup)
- [AWS Setup](#aws-setup)
- [Usage](#usage)
- [Alerts](#alerts)
- [Analytics and Visualization](#analytics-and-visualization)
- [Integrating AWS Athena](#integrating-aws-athena)
- [Integrating AWS QuickSight](#integrating-aws-quicksight)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

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


