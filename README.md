# capstone

## Summary
Utilize open data to walk through Journeys of Veterans story (https://www.blogs.va.gov/VAntage/wp-content/uploads/2020/02/Veteran-Journey-Map.pdf).

## FAQ Search Using Approximate kNN
Uses SentenceTransformers which makes use of BERT sentence embeddings.  This framework is based on PyTorch and Transformers.

1) Collected FAQ information from Walter Reed website
2) Generate dense vector representation of the questions using SentenceTransformer and store in Elasticsearch index
3) When query is submitted, it is encoded using Sentence Transformers before being sent to the "kNN search" endpoint
4) This returns a ranked list of results using similarity calculation (configurable)

This is currently running on AWS EC2 instance because I had trouble installing data science packages on Apple M1.

## Basic Pay
This information was parsed from PDF files provided on the [DOD Military Compensation site](https://militarypay.defense.gov/Pay/Basic-Pay/Active-Duty-Pay/). 

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
