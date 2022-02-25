# Simple-Google-Page-Speed-Checker
A simple script for checking  core web vitals and page speed data on a batch of URLs
<br>
<br>
This script was designed to be a simple but comprehensive page speed and core web vitals checker. 
<br>
<br>
## How to Make it Work
<br>
Additions required to make the script run:
<br>
<br>
* An API Key from Google Developer Console
<br>
* A .txt file entitled 'speed-urls.txt' in the folder where the script is located. 
This file should contain all URLs that require checking, one line per URL. 
<br>
<br>

## Results
<br>
The script produces six excel files for the results.
<br>
<br>
* Origin data for mobile
<br>
* Origin data for desktop
<br>
* Field data for mobile
<br>
* Field data for desktop
<br>
* Lab data for mobile
<br>
<br>

## Further Information
<br>
* **Origin data** refers to the average core web vitals performace across the website. The script will automatically find all domains within the .txt file and acquire their origin data. Included are the overall results as well as core metrics: 'Overall Score', 'FCP Percentile', 'FCP Category', 'LCP Percentile', 'LCP Category', 'FID Percentile', 'FID Category', 'CLS Percentile', 'CLS Category'. Percentile refers to numeric score, and Category refers to classification.
<br><br>
* **Field data** refers to core web vitals metrics. Included are the overall results as well as core metrics: 'Overall Score', 'FCP Percentile', 'FCP Category', 'LCP Percentile', 'LCP Category', 'FID Percentile', 'FID Category', 'CLS Percentile', 'CLS Category'. Percentile refers to numeric score, and Category refers to classification.
<br><br>
* **Lab data** refers to the original data supplied by the Google Page Speed Tool. Included are the overall scores as well as the core metrics which contribute to that score: 'Score', 'FCP', 'Speed Index', 'LCP', 'Interactive', 'TBT', 'CLS'.

