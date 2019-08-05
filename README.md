
# Outguard 
Outguard is a module to detect in-browser cryptojacking operations. 

## Abstract

In-browser cryptojacking is a form of resource abuse that leverages end-users’ machines to mine cryptocurrency without obtaining the users’ consent. In this paper, we design, implement, and evaluate
Outguard, an automated cryptojacking detection system. We construct a large ground-truth dataset, extract several features using an instrumented web browser, and ultimately build an SVM classification model.
Outguard achieves a 97.9% TPR and 1.1% FPR and is reasonably
tolerant to adversarial evasions. We utilized Outguard in the wild
by deploying it across the Alexa Top 1M websites and found 6,302
cryptojacking sites, of which 3,600 are new detections that were absent from the training data. These cryptojacking sites paint a broad picture of the cryptojacking ecosystem, with particular emphasis on
the prevalence of cryptojacking websites and the shared infrastructure that provides clues to the operators behind the cryptojacking phenomenon.


## Modules and Related Source Code

To create a labeled dataset of cryptojacking websites, we build a nodejs module on top of Wappalyzer -- a library identification module. 
The nodejs module can identify different types of cryptojacking libraries. The corresponding data is located in js_fingerprint path. Make sure the latest version of Nodejs. 

```
 node driver_engine.js http://seriesfree.to
```
The nodejs module labeled seriesfree.to as an instance of CoinHive mining website. After running such a simple source code 
scanning at scale, we visited each crypomining website using the  customized instrumented browser to record the interaction of the libraries with browser resources and train the automatic model. The instrumented browser is using devtool protocol.   
The outputs of the instrumented browser are two 
files: (1) files which contain the networking traffic of the website, and (2) a devtool trace file which contains the 
cpu profiling trace after loading the javascript code of a given website. 
Similar to the standard devtool api, you need to run the code on port 9222 to enable the module to interact with the debugging protocol. 

For visualization purposes, you can also simply load the trace file using ```chrome://tracing```. 

## Feature Extraction 
To extract features used in Outguard, ```parsing_module.py``` should be called in the ```parser``` folder. 
While it is not recommended to upload large files directly to the repo, some examples are
located at ```outguard/parser/tracing``` folder. 

``` 
$ python parser_module.py -d trace -o myoutput.csv 

``` 

## Classification

If you have done all the privious steps right, the rest is simple. A code sample is provided on how the training and testing should work. 
```outguard_classifier.py```basically receives the training data as well as unlabeled datasets in csv formats, and print out the 
classification results for the unlabled set. 


## Citation 
```
@misc{kharraz:2019:cryptojacking,
 AUTHOR = {Amin Kharraz and Zane Ma and Paul Murley and Charles Lever and Joshua Mason and Andrew Miller and Manos Antonakakis and Michael Bailey },
 TITLE = {{Outguard: Detecting In-Browser Covert Cryptocurrency Mining in the Wild}},
 BOOKTITLE = {The Proceedings of the 2019 World Wide Web Conference ({WWW} '19)},
 ADDRESS = {San Francisco, CA},
 MONTH = {May},
 DAY = {13--17},
 YEAR = {2019},
}
```
## Contacts
Please send an email to kharraz@illinois.edu if you have any questions. 
