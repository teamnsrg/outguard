# Abstract

In-browser cryptojacking is a form of resource abuse that leverages end-users’ machines to mine cryptocurrency without obtaining the users’ consent. In this paper, we design, implement, and evaluate
Outguard, an automated cryptojacking detection system. We construct a large ground-truth dataset, extract several features using an instrumented web browser, and ultimately build an SVM classification model.
Outguard achieves a 97.9% TPR and 1.1% FPR and is reasonably
tolerant to adversarial evasions. We utilized Outguard in the wild
by deploying it across the Alexa Top 1M websites and found 6,302
cryptojacking sites, of which 3,600 are new detections that were absent from the training data. These cryptojacking sites paint a broad picture of the cryptojacking ecosystem, with particular emphasis on
the prevalence of cryptojacking websites and the shared infrastructure that provides clues to the operators behind the cryptojacking phenomenon.


# Modules and Related Source Code

To create a labeled dataset of cryptojacking websites, we build a nodejs module on top of Wappalyzer -- a library identification module. 
The nodejs module can identify different types of cryptojacking libraries. The corresponding data is located in js_fingerprint path. Make sure the latest version of Nodejs. 

```
 node driver_engine.js http://bbc.com
```
The collected cryptojacking websites were then visited by the customized instrumented browser to record the interaction of the libraries with browser resources and train the automatic model. 



# Citation 
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
