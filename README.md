# Product Alerts

### Summary

This project is an effort to provide an easy interface to allow for setting up quick and easy email alerts for product deals on popular websites.  After scraping and alerting for multiple websites, I realized that there is a fairly common workflow for the process.  

### Typical Workflow

SearchSite -> Find all pages of result -> Find all Products on each page -> Parse Products -> DB Dump -> Alert

### The Goal

All you should really have to do in order to make an alerting system, then, is specify to the interface how to parse the html at each step of this process. We should be able to abstract away the overhead and make each new alerting system simply about writing one function for each of these steps to parse the html needed. 
