# job_offers_analyzer
Implementation of topic modeling (unsupervised learning) to cluster unlabeled data (job offers descriptions)

This is an application of unsupervised learning (a field of machine learning), which takes as input the description of job offers (in this particular case: jobs for electricians) and as output returns the categories or topics most commonly found in the job offers (e.g: construction, design, maintenance, etc).


The method applied to find the categories of the unlabeled data (job offers description) is called Latent Dirichlet Allocation, which is a probabilistic model that tries to find groups of words appearing together in the corpus of text. As a parameter, the user must specify the number of groups beforehand. This method is implemented inside a python machine learning library called scikit-learn.


Project has following files:

1. topics_job_offers.ipynb: This is a jupyter notebook with the implementation of topic modeling.
2. listaEmpleos_v2.py: This is a web scrapper to obtain the information of job offers from a website.
3. stopwords_esp.txt: Stopword in spanish language (language of job offers).
4. Electricista_2_20210107.xls: This file contains the job offers extracted from the web site. The jupyter notebook
imports this file and process the information to cluster and define topics.
