# NEAR REAL TIME ROAD TRAFFIC EVENT DETECTION USING TWITTER AND SPARK


## TEAM MEMBERS:
1. Akshaya Ramaswamy (AXR170131)
2. Aswin Krishna Gunasekaran (AXK175831)
3. Sai Spandan Gogineni (SXG175130)
4. Sankalp Rath (SXR173830)
5. Sivagurunanthan Velayutham (SXV176330)

## OVERVIEW:

* Gather tweets using twitter search API, pre-process tweets and extract important features to build a model using spark MLlib.
* Stream tweets using twitter streaming API and push data into kafka topic using a kafka producer after applying partial filters.
* Read from kafka topic using kafka consumer.
* Perform tokenization, stopword removal etc. to pre-process the data. 
* Extract machine readable features using bag of words approach and predict instances with the model.
* Tweets are indexed to elasticsearch after classification
Constructed a traffic heat map by reading the coordinates data from elasticsearch.

## TECHNOLOGIES USED:

* TWEEPY
* KAFKA
* ELASTICSEARCH
* GOOGLE MAP’S API
* SPARK STREAMING
* SPARK MLIB
* NLTK


## ARCHITECTURE:

![](https://github.com/SivagurunathanV/Traffic-Detection-from-Twitter-using-Spark/blob/master/docs/arch.png)


## RESULTS:

![](https://github.com/SivagurunathanV/Traffic-Detection-from-Twitter-using-Spark/blob/master/docs/result.png)
