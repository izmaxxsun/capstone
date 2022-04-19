# capstone

## Summary
The hardest part of the journey these days isn't about getting data, it's now about unifying it and assembling it in a digestable way from the perspective of an actual end user.  In this project, we walk through the particular perspective of a veteran using the **Journeys of Veterans Map** prepared by the Veterans Experience Office.

This framework is integrated into the VA Welcome Kit and helps break down into segments the experiences and broad set of shared moments that many Veterans will encounter.  Using Elastic, we augment a subset of sections with data visualizations generated from processing various data sources and formats to aid the service member or Veteran in making informed, data-based decsions using a cohesive storyline.

In addition, this project implements a practical use case for Natural Language Processing and advancements in search capabilities (i.e. approximate kNN search) to help the user find answers to frequently asked questions.

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

## Basic Pay
Not entirely related to the VA but this is an important part of understanding future prospects. This information was parsed from PDF files provided on the [DOD Military Compensation site](https://militarypay.defense.gov/Pay/Basic-Pay/Active-Duty-Pay/). 

Visualizations:
- Dashboard shows line graph of pay rate against years of experience for each pay grade

Currently only includes latest available data (2022) for Enlisted service members. 
TODO: Can add information for commissioned officers and other years.

## Housing
This information was parsed from ASCII files provided on the [DefenseTravel Management site](https://www.defensetravel.dod.mil/site/bah.cfm).  It required multiple enrichment processors to generate a geo-point location which could be used for a Maps visualization.

## VA Loans
This information was parsed from CSV files provided on the [US Department of Veterans Affairs site](https://www.benefits.va.gov/HOMELOANS/Lender_Statistics.asp).  Multiple years of data were indexed and an "update by query" approach was used to add a timestamp to analyze trends.

## VA Patient Wait Times
This information is sourced directly from the [VA Lighthouse API](https://developer.va.gov/).  Python script was used to make the API call and denormalize the response for storage into Elasticsearch.  Coordinates provided from API were used to store the location as a geopoint for Maps visualization.

## Patient Satisfaction
TBD - can be processed in same pattern as the Patient Wait Times

## Medicare Part D - Drug Costs
This information is sourced from the [data.cms.gov](https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-geography-and-drug) datasets. It contains information on prescription drugs prescribed by individual physicians and other health care providers and paid for under the Medicare Part D Prescription Drug Program.

## Open Payments
TBD - this is a huge dataset showing payments made to physicians...potentially could use ML on this

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
