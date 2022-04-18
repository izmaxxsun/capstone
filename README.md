# capstone

## Summary
Utilize open data to walk through Journeys of Veterans story (https://www.blogs.va.gov/VAntage/wp-content/uploads/2020/02/Veteran-Journey-Map.pdf).

## Enhanced Medical FAQ Using Approximate kNN Search
<img align="left" width="100" height="100" src="https://aeiljuispo.cloudimg.io/v7/https://s3.amazonaws.com/moonup/production/uploads/1609621322398-5eff4688ff69163f6f59e66c.png?w=200&h=200&f=face">
The idea behind this to make it save user's time from browsing through FAQs by allowing them to simply ask their question and have the system find relevant information for them.  This leverages Natural Language Processing to find semantic similarities between the question you're interested in and all the FAQ questions that have been processed and stored in Elasticsearch. 
<br />
<br />

This implementation uses SentenceTransformers which is a Python-based framework that uses PyTorch and Transformers.  The BERT-based training model it uses is available on the Hugging Faces repository.  The general approach is described below:

<br clear="both" />


1. Collected FAQ information from Walter Reed website
2. Generate dense vector representation of the questions using SentenceTransformer and store in Elasticsearch index
3. When query is submitted, it is encoded using Sentence Transformers before being sent to the "kNN search" endpoint
4. This returns a ranked list of results using similarity calculation (configurable)

This is currently running on AWS EC2 instance because I had trouble installing data science packages on Apple M1.

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
