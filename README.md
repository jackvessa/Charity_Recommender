# Charity Recommender System

One Paragraph of project description goes here

# Table of Contents
- [Project Motivation](#Project-Motivation)
- [Overview of the Data](#Overview-of-the-Data)
- [Exploratory Data Analysis](#Exploratory-Data-Analysis)
- [Data Pipeline](#Data-Pipeline)
- [Model Selection](#Model-Selection)
- [Deep Learning](#Deep-Learning)
- [Emotional Analysis](#Emotional-Analysis)
- [Wordclouds](#WordClouds)
- [Conclusion and Next Steps](#Conclusion-and-Next-Steps)

# Project Motivation
- Build a recommendation system to recommend charities to users based on donation history
- Recommend local charities (same zip, county, or state) to users based on a given category

# Goal:
-  

# Overview of the Data

## First Dataset - IRS:
The first dataset comes from the [IRS](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) website and contains information about all charitable organizations in the United States

- Original Data Set
  * 1,719,673 charities (rows)
  * 28 features for each charity (columns)
- Data Cleaning:
  * Keep charities that offer fully tax deductible donations and have an NTEE Category Code
  * Translate NTEE code into category column
  * Keep essential column features
- Cleaned Data Set
 * 992,318 charities (rows)
 * 10 features for each charity (columns)

Preview of IRS Data Set

| EIN | NAME | STATE |INCOME_CD | ZIP_FIVE	 | NTEE_Major_Category	 |  County |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|10130427	|BRIDGTON HOSPITAL	|ME	|9	|04009	|Health - General and Rehabilitative	|Cumberland County|
|10024645	|BANGOR SYMPHONY ORCHESTRA	|ME	|6	|04402	|Arts, Culture and Humanities	|Penobscot County|
|10015091	|HANOVER SOCCER CLUB INC	|NJ	|4	|07927	|Recreation, Sports, Leisure, Athletics	|Morris County|



## Second Dataset - Kaggle:
The second dataset comes from [Kaggle](https://www.kaggle.com/katyjqian/charity-navigator-scores-expenses-dataset) and contains information about charities rated by [CharityNavigator.org](https://www.charitynavigator.org/) : 

- Original Data Set
  * 8,400 charities (rows)
  * 20 features for each charity (columns)
- Data Cleaning:
  * Keep all charities
  * Keep essential column features
  * Create "corpus" column that contains information about charity category, description, motto, and state
- Cleaned Data Set
 * 8,400 charities (rows)
 * 8 features for each charity (columns)

- Shows the frequency of each personality type in the population

| - | type | posts |
|:---:|:---:|:---:|
| 0 | INFJ | 'http://www.youtube.com/watch?v=qsXHcwe3krw|||...'|
| 1 | ENTP | 'I'm finding the lack of me in these posts ver..' |
| 2 | INTP | 'Good one _____ https://www.youtube.com/wat...' |
| 3 | INTJ | 'Dear INTP, I enjoyed our conversation the o... '|
| 4 | ENTJ | 'You're fired.|||That's another silly misconce... '|

<a href="#Charity Recommender System">Back to top</a>


# Exploratory Data Analysis


Performing EDA on our data set revealed a few things. They are summarized by the graphs below:

|Data Unbalanced|Questions per post|
|:---:|:---:|
|![](img/unbalanced.png)|![](img/questionspp.png)|

|Links per post|Words per post|
|:---:|:---:|
|![](img/linkspp.png)|![](img/wordspp.png)|

For further EDA please look at the summary [here](ExploratoryDataAnalysis.md)

<a href="#Charity Recommender System">Back to top</a>


# Data Pipeline

<!-- #region -->
Let's create a data pipeline, it will aim to do the following:
- Standardize the text to ASCII
- Remove weblinks
- Tokenize the words
- Use a stemmer on the words
- Remove HTML decoding
- Remove punctuation
- Remove stopwords

The code to do this can be found [here](src/personality.py)

![](img/Pipeline.png)

<a href="#Charity Recommender System">Back to top</a>
<!-- #endregion -->

# Model Selection


The Charity Navigator Dataset contains 11 categories. Recommending one of these categories at random would result in the same category  getting recommended 9.09% of the time. The goal for the recommendation model is to improve this score to above 50%.
The code for this can be found [here](src/Charity_Navigator_LDA_Similarity.ipynb)

We will use Latent Dirichlet Allocation:
-                   - Accuracy = 30.00%
-                   - Accuracy = 40.00%
-                   - Accuracy = 50.00%
-                   - Accuracy = 60.00%
-                   - Accuracy = 70.00%

<a href="#Charity Recommender System">Back to top</a>




# Deployment

Web Application Deployed on an Amazon EC2 Instance

## Built With

* [Python](https://www.python.org/) - Coding Language for Machine Learning Application
* [Gensim](https://radimrehurek.com/gensim/index.html) - Used for Latent Dirichlet Allocation - Topic Modeling
* [Flask](http://flask.palletsprojects.com/en/1.1.x/) - Framework for Creating the Web Application


## Author

* **Jack Vessa** 

## Acknowledgments

* Thank you to those that support charitable organizations and help to make our world a better place
