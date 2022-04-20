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
After joining, a significant benefit is becoming eligible for VA-backed mortgages to buy a house for your family.  The US Department of Veterans Affairs provides lender statistics dating back to 2015 comprising of over 8,000 records.  For the dashboard, we distill this into a couple points of interest:
* Who are the top lenders and how much are they lending on average?
* Which lenders are processing the most loans? Maybe I want to work with the lender with the most experience.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/va-lender.png">

If we want to dig further, we can view the dashboard which provides trends in mortgate amounts over time.  From here, we could also filter data to what is of interest.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/va-loan-dashboard.png">

Source: [US Department of Veterans Affairs site](https://www.benefits.va.gov/HOMELOANS/Lender_Statistics.asp).  2015-2021
Format: CSV

## VA Patient Wait Times
Access to care is vital and it can be confusing to determine when you are eligible for community care.  Part of the guidelines from the [Mission Act](https://www.va.gov/communitycare/docs/pubfiles/factsheets/va-fs_cc-eligibility.pdf) mention one criteria for being eligible for community care when an appointment cannot be made with the VA within 20 days.

Using the APIs provided by the VA, we can open up transparency on this data by providing an interactive Kibana map view showing the states with the longest wait times as well as displaying data for specific VA health facilities.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/va-wait-times.png">

Source: [VA Lighthouse API](https://developer.va.gov/)  
Format: REST API

## Patient Satisfaction
Just having access to care isn't enough. Satisfaction scores can be looked at from the perspective of the patient and the health facility.  This data is also available from the VA Lighthouse API.

This is a data point that you could look at in this Kibana Map view as you're [selecting your preferred VA facility](https://www.va.gov/healthbenefits/resources/publications/hbco/hbco_faq.asp#:~:text=You%20may%20select%20any%20VA,administrative%20eligibility%20and%20medical%20necessit.) and sketching out the most convenient driving routes.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/va-patient-satisfaction.png">

Source: [VA Lighthouse API](https://developer.va.gov/)  
Format: REST API

## Medicare Part D - Drug Costs
The reporting of drug costs from Medicare Part D provide some transparency on the cost of prescriptions you might need. Providing trend graphs help us see where prescription costs are rising and a map view helps us see how the cost of an average claim compares by state.

<img src="https://github.com/izmaxxsun/capstone/blob/main/screen_captures/drug-costs.png">

Source: [data.cms.gov](https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-geography-and-drug)  
Format: CSV

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
### Creating an Index
Approximate kNN search is currently an experimental feature, so the index mappings were created in Kibana > Dev Tools.  Run the following request to create the index:
```
PUT faq-knn-sbert
{
  "mappings": {
    "properties": {
      "sbert_encoding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "l2_norm"
      },
      "question": {
        "type": "text"
      },
      "answer": {
        "type": "text"
      },
      "source": {
        "type": "text"
      }
    }
  }
}
```

### Add FAQ data to the index
Run the "sbert_indexer.py" script

### Performing a Search
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
