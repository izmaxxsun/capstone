# Capstone - Journeys of Veterans

## Summary
The hardest part of the journey these days isn't about getting data, it's now about unifying it and assembling it in a digestable way from the perspective of an actual end user.  In this project, we walk through the particular perspective of a veteran using the **Journeys of Veterans Map** prepared by the Veterans Experience Office.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/journeys-of-veterans.png">

This framework is integrated into the VA Welcome Kit and helps break down into segments the experiences and broad set of shared moments that many Veterans will encounter.  Using Elastic, we augment a subset of sections with data visualizations generated from processing various data sources and formats to aid the service member or Veteran in making informed, data-based decsions using a cohesive storyline.

In addition, this project implements a practical use case for Natural Language Processing and advancements in search capabilities (i.e. approximate kNN search) to help the user find answers to frequently asked questions.

## Walking Through the Journey
Information is organized according to the journey map above using [Canvas](https://www.elastic.co/guide/en/kibana/current/canvas.html) which is one of Elastic's data visualization and presentation tools.  To access it, log into Kibana and navigate to Canvas.

## Basic Pay
There are many reasons to join the Armed Services...duty to the country, protecting freedom across the world, gaining experience like any other.  Those are difficult to quantify but we do have hard data on pay and part of your financial health is being able to pay your bills.

This page provides a sampling of annual pay of different pay grades for Enlisted and Commissioned personnel. Each data point is presented from live data using [Elasticsearch SQL](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-overview.html) which provides a familiar experience for analysts versed in SQL. From there, if the user wants to dig further they can explore the linked dashboard which shows information such as pay progression with years of experience and compare different pay grades. 

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/basic-pay-enlisted.png">
<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/basic-pay-dashboard.png">

Source: [DOD Military Compensation site](https://militarypay.defense.gov/Pay/Basic-Pay/Active-Duty-Pay/)
Format: PDF (the CSV conversion can be found in the "source_data" folder)

## Housing
In addition to money to pay the bills, having a roof over your head is also important to your health. Getting this data indexed into Elasticsearch required an [ingest pipeline](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html) in order to associate each record with state (e.g. Florida, Texas) and geolocation information so it could be displayed using [Kibana Maps](https://www.elastic.co/guide/en/kibana/current/maps.html).

The end result is an interactive map where users can see housing allowances per state and the ability to filter based on their pay grade and years of experience.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/housing-allowance.png">

Source: [DefenseTravel Management site](https://www.defensetravel.dod.mil/site/bah.cfm)
Format: ASCII 

## VA Loans
After joining, a significant benefit is becoming eligible for VA-backed mortgages to buy a house for your family.    

This information was parsed from CSV files provided on the [US Department of Veterans Affairs site](https://www.benefits.va.gov/HOMELOANS/Lender_Statistics.asp).  Multiple years of data were indexed and an "update by query" approach was used to add a timestamp to analyze trends.

## VA Patient Wait Times
This information is sourced directly from the [VA Lighthouse API](https://developer.va.gov/).  Python script was used to make the API call and denormalize the response for storage into Elasticsearch.  Coordinates provided from API were used to store the location as a geopoint for Maps visualization.

## Patient Satisfaction
TBD - can be processed in same pattern as the Patient Wait Times

## Medicare Part D - Drug Costs
This information is sourced from the [data.cms.gov](https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-geography-and-drug) datasets. It contains information on prescription drugs prescribed by individual physicians and other health care providers and paid for under the Medicare Part D Prescription Drug Program.

## Open Payments
TBD - this is a huge dataset showing payments made to physicians...potentially could use ML on this

## Enhanced Medical FAQ Using Approximate kNN Search
The idea behind this to make it save user's time from browsing through FAQs by allowing them to simply ask their question and have the system find relevant information for them.  This leverages Natural Language Processing to find semantic similarities between the question you're interested in and all the FAQ questions that have been processed and stored in Elasticsearch. 

<p align="center"><img src="https://github.com/izmaxxsun/capstone/blob/main/beyondtext.gif"></p>
<p align="center">Source: elastic.co</p>

This implementation uses SentenceTransformers which is a Python-based framework that uses PyTorch and Transformers.  The BERT-based training model it uses is available on the Hugging Faces repository.  The general approach is described below:
<br clear="both" />

1. Collected FAQ information from Walter Reed website
2. Generate dense vector representation of the questions using SentenceTransformer and store in Elasticsearch index
3. When query is submitted, it is encoded using Sentence Transformers before being sent to the "kNN search" endpoint
4. This returns a ranked list of results using similarity calculation (configurable)

In this example, the user types in "my knee hurts" and the search finds results based on the semantic meaning returning a top result of "Can you treat my pain?".

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/sbert-search.png">


# Details
## Environment Setup
This demo was created using a Google Cloud compute instance (e2-medium) which uses a Debian "Buster" OS release.  
```
# Upgrade pip to at least version 22.0.4
pip install --upgrade pip

# Configure Git
sudo apt update
sudo apt install git
git config --global user.name "izmaxxsun"
git config --global user.email "isra.sunhachawi@elastic.co"

# Configure SSH key for Github
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub
# Copy this SSH key into your Github Settings > SSH and GPG Keys page
ssh-add -K ~/.ssh/id_rsa
git clone <forked_repository_SSH_info>

# Install Python virtual environment
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate
```

## Enhanced FAQ Search

### Step-by-step
1) Activate the virtual environment
```
source env/bin/activate
```
2) Install Sentence Transformers
```
pip install -U sentence-transformers
```
3) Install Elasticsearch client
```
pip install elasticsearch
```
4) Start asking questions!
```
python sbert_query.py
```
