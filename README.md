# High Energy Physics paper tagger

This is the source code used to build the web app [High Energy Physics paper tagger](http://hep-th-classifier.s3-website.eu-west-2.amazonaws.com) hosted on AWS. The app collects the new papers published daily in the *hep-th* category on the arXiv and assigns a topic to each of them using machine learning techniques. The app is written in Python and uses Flask for the dynamic part of the website, and MySQL for facing the database where papers are stored.

The app is divided into three main parts,
- A short script accessing the daily RSS feed on the arXiv and storing the metadata of the papers into a SQL database (realized with AWS RDS). This short script can be uploaded as a zip file (together with relevant dependency) in AWS Lambda.
- A script accessing the papers in the database and classifying them with a pre-trained model. More information on the model are available [here](https://github.com/carlosparaciari/abstract-classification-embedding). The model is not provided in this repository and was uploaded on a private S3 bucket that the script can access. Since the dependencies of this script are rather large, we have to make a contained with docker, ship it to AWS ECR, and create a Lambda function from there.
- The website, with the static part hosted on a public S3 bucket, and the dynamic one running on an EC2 instance using Apache2 and Flask.

## Classification model

The model we use in this web app is a Convolutional Neural Network, taking as input the abstract and title of a paper. These texts have been cleaned using standard NLP techniques, and have been embedded in a real vector space using a word2vec model that we trained. More information on the model are available [here](https://github.com/carlosparaciari/abstract-classification-embedding).

Before settling with the above architecture, we have trained multiple models, with different pre-processing of the data, and we have selected the one with an accuracy significantly higher than the others (where we used McNemar's test for assessing the significance of an accuracy improvement).

In this [study](https://github.com/carlosparaciari/abstract-classification-supervised), we pre-processed the data using TF-IDF vectorization and used different models to classify the papers. The models we used include Random Forest, Gradient Boosting, Support Vector Machine with linear Kernel, Logistic Regression.

In this other [study](https://github.com/carlosparaciari/abstract-classification-embedding), we pre-processed the data using word2vec embedding and used two Neural Network architectures to classify the papers; a Convolutional Neural Network, and a Recursive Neural Network.

In addition to the above studies, we used unsupervised methods to cluster papers (published on the arXiv in the hep-th category) into different groups and gain a better understanding of which topics are generally covered in this category. The study can be found [here](https://github.com/carlosparaciari/abstract-clustering). Our results seem to indicate a good overlap between the labels we use to classify the papers and the topics published on the arXiv, as discovered using unsupervised techniques. For this study, we have used K-Means Clustering, Hierarchical Clustering, and Spectral Clustering.

Further information on the web app can be found on the about page of the website.