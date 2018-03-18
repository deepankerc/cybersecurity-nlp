# Cybersecurity Strategy Analysis

This is an independently developed application to be submitted to the UN's Unite Ideas [CyberSecurityNLP initiative](https://cybersecuritynlp.uniteideas.spigit.com/Page/Home). The initiative is a collaborative project of [Unite Ideas](https://www.uniteideas.spigit.com/Page/Home), the Digital Blue Helmets, Fordham University, and Northeastern University.

## Overview

The goal of this project is to build a tool that expedites the review of national cybersecurity strategy documents. From the [project website](https://www.uniteideas.spigit.com/Page/Home):

> Analyzing strategy documents is a difficult task which requires human knowledge held by specialists in public policymaking, cybersecurity, legal, human resources, and other domains. It also involves lengthy manual reviewing and highlighting of documents in different formats. Let's expedite this effort.

The relevant documents to be analyzed are [here](https://www.itu.int/en/ITU-D/Cybersecurity/Pages/National-Strategies-repository.aspx) and examples of human analyst summaries are [here](https://www.itu.int/en/ITU-D/Cybersecurity/Pages/Country_Profiles.aspx). The documents are unstructured PDFs with varying formats.

## Getting Started

### Downloading Documents

Metadata on all of the appropriate documents is provided in the CSV [here](https://github.com/llefebure/cybersecurity-nlp/blob/master/cybersecurity_nlp/data/document_key.csv). To fetch the documents according to this metadata, simply run the command below:

```
./download_documents.sh
```

If you find an error in the metadata, feel free to edit the CSV directly. If you'd like to completely annotate the documents yourself, simply delete that CSV before running the above command. The script will prompt you to validate the metadata associated with each document and create the CSV for you.

### Text Processing

Text extraction, tokenization, annotation, and all other backend processing tasks are done in Python and documented [here](https://github.com/llefebure/cybersecurity-nlp/blob/master/cybersecurity_nlp/README.md). A static JSON file is produced and served by the frontend.

### Web App

The frontend is built on [Vue.js](https://vuejs.org/) and [Quasar](http://quasar-framework.org/). Instructions for running this are [here](https://github.com/llefebure/cybersecurity-nlp/blob/master/app/README.md).
