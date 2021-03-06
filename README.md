### Background
E-Commerce is a fast-growing and highly competitive space. Businesses need to continue testing and iterating to improve business operations, stand out from the competition and ensure that it is moving in the right direction.

Ecommerce analytics is the process of accumulating data from all of the areas that have an impact on your store. You should then use this data so that you can comprehend shifts in customer behavior and online shopping trends.

Ultimately, you can make more intelligent decisions by basing them on data, which should result in more online sales being made.

Ecommerce analytics can include a wide range of metrics relating to the full customer journey, such as discovery, acquisition, conversion, retention and advocacy.

### Welcome to Analytics Dashboard
The repository has code for a web application that tracks multiple metrics that can help the businesses to measure their performance against objectives and the overall health. 

The application is divided into:

1. Key Performance Indicators (KPIs) e.g., Monthly Revenue, Monthly Growth Rate, Average Order Count.

2. Customer Retention / Churn Rate.

3. Visualize Customer Journey through Sankey Diagram.

4. Customer Segmentation using RFM (Recency – Frequency – Monetary Value) Clustering.

5. Customer Acquisition Cost

6. Market Basket Optimization

7. Customer Funnel Analysis

8. Animated Bubble Plot

### Data Description
The data is from [Olist](https://olist.com/en-us/), the largest department store in Brazilian marketplaces

Olist connects small businesses from all over Brazil to channels without hassle and with a single contract. Those merchants are able to sell their products through the Olist Store and ship them directly to the customers using Olist logistics partners.

The [dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil. Its features allow viewing an order from multiple dimensions: from order status, price, payment and freight performance to customer location, geolocation, product attributes and finally reviews written by customers.

![Order Data Schema](https://github.com/piushvaish/ecommerce-analytics/blob/main/olist_images/olist_data_schema.png)

Marketing funnel dataset from sellers that filled-in requests of contact to 
    sell their products on Olist Store. 
    The dataset has information of 8k Marketing Qualified Leads (MQLs) that 
    requested contact between Jun. 1st 2017 and Jun 1st 2018. 
    They were randomly sampled from the total of MQLs. 
    Its features allow viewing a sales process from multiple dimensions: 
    lead category, catalog size, behaviour profile, etc. 
 ![Marketing Funnel Schema](https://github.com/piushvaish/ecommerce-analytics/blob/main/olist_images/olist_marketing_dataset_schema.png)
 
 ### Technologies Used
#### Streamlit
Streamlit is an open-source framework for the rapid development of interactive, highly interactive, and fast machine learning and data science web applications. It is extremely well designed and easy to use. 

#### Docker 
The company Docker makes a product (also called Docker) that enables users to create, run and manage containers. 

LXD and LXC are less famous alternatives to Docker’s containers, while Docker is by far the most popular. Docker helps you build, deploy, and run applications by using containers. 

An application is packaged in a container with all of its parts, including libraries and other dependencies, and distributed as a single package. 

The Dockerfile, which is really just a set of instructions, is used to create a docker image. Container orchestration is the whole process of managing hundreds and thousands of containers.

#### Amazon Web Services (AWS)
Cloud computing can be accessed through Amazon Web Services (AWS). AWS offers over 175 services from data centers around the world. AWS has two services for container orchestration:

Amazon Elastic Container Service (ECS) is Amazon’s proprietary container orchestration platform. 

The concept behind ECS is similar to Kubernetes (both are orchestration platforms). ECS is AWS-native, so it can only be used on AWS infrastructure.


Amazon Elastic Kubernetes Service (Amazon EKS) uses Kubernetes, a publicly available open-source project for deployment on many cloud providers. 

EKS makes it easy to start, run, and scale Kubernetes applications on-premises or in the AWS cloud. AWS is an easy way to run EKS clusters fully managed.

There are many differences between EKS and ECS in terms of pricing, compatibility, and security, though the purpose of both is to orchestrate containerized applications. No one solution is best. The choice depends on the use case.

#### AWS Fargate — AWS Serverless Architecture for running containers
Building your web application with Fargate is easy. It makes use of AWS Elastic Container Service and Amazon Elastic Kubernetes Service to use a serverless compute engine. 

It minimizes the need for constant server provisioning and management, lets you buy a specific amount of resources accordingly for each application, and ensures increased security through application isolation by design. 

It eliminates the need to select instances and scale cluster capacity since Fargate allocates the right amount of computing. 

Using containers will save you from over-provisioning and paying for additional servers.


### Build a Docker image
```
docker build -t streamlitapp:latest .
```
### Create a container
```
docker run -p 8501:8501 streamlitapp:latest
```
We can access the application on your desktop by visiting http://localhost:8501/

### Overview of Tasks to Deploy Web Application
* Build a cross-platform web app that incorporates online prediction functionality
* Create a Dockerfile
* Build and push a Docker image on Amazon Elastic Container Registry
* Create and execute a task to deploy the app using AWS Fargate’s serverless infrastructure.

