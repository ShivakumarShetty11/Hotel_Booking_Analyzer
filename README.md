# Hotel Booking Analyzer 🏨

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![PySpark](https://img.shields.io/badge/PySpark-3.3%2B-orange.svg)](https://spark.apache.org/)
[![Hadoop](https://img.shields.io/badge/Hadoop-3.2%2B-yellow.svg)](https://hadoop.apache.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)


A distributed big data analytics project that leverages Apache Spark and Hadoop ecosystem to analyze large-scale hotel booking datasets. This project demonstrates enterprise-grade data processing capabilities, handling massive datasets efficiently through PySpark's distributed computing framework while accessing data stored in Hadoop Distributed File System (HDFS).

## ✨ Project Overview

This repository showcases a complete big data pipeline for hotel booking analysis, featuring:

- **Distributed Data Processing**: PySpark for handling large-scale datasets across cluster nodes
- **Hadoop Integration**: Direct data access from HDFS for enterprise data storage
- **Scalable Analytics**: Machine learning on distributed datasets using Spark MLlib
- **Real-time Processing**: Streaming analytics capabilities for live booking data
- **Enterprise Architecture**: Production-ready big data solution design

## 🏗️ Big Data Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Hadoop HDFS   │    │   Apache Spark   │    │   PySpark App   │
│                 │    │                  │    │                 │
│ • Data Storage  │────│ • Cluster Mgmt   │────│ • Analysis Code │
│ • Replication   │    │ • Job Scheduling │    │ • ML Models     │
│ • Fault Tolerance│   │ • Memory Mgmt    │    │ • Visualizations│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Spark MLlib    │    │   Results       │
│                 │    │                  │    │                 │
│ • Hotel Systems │    │ • Classification │    │ • Dashboards    │
│ • Booking APIs  │    │ • Clustering     │    │ • Reports       │
│ • External Data │    │ • Regression     │    │ • Predictions   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🗂️ Repository Structure

```
Hotel_Booking_Analyzer/
├── app (1).py          # PySpark web application with Spark context
├── main.ipynb          # Primary analysis notebook with PySpark
├── model.ipynb         # Spark MLlib models and distributed ML
├── spark_config/       # Spark configuration files
├── hdfs_utils/         # Hadoop utilities and data access
├── requirements.txt    # Python and PySpark dependencies
└── README.md          # This file
```


