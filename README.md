<h1 align='center'>
  Qiana
</h1>

<br><br>


<p align=center>
 <img src="readme-lib\qiana-logo.png" alt="Logo" width="30%"/>
</p>

<br><br>


Nowadays, chatbot systems, which assist a variety of industries including business, banking, medicine, and education, are the most in-demand technology. With the help of this system, individuals can speak to robots in a human-like manner. Machines or systems may now understand human natural language and respond appropriately—or even produce responses in that language. These chatbot systems are designed using a variety of technologies that are readily available. The most advanced technique for aiding the system's interpretation and production of human language is known as natural language processing. In this study, a chatbot system that automates the ordering of food is proposed. The system, which uses natural language processing in its design, can communicate with customers, give them the necessary meal information, and collect food orders. A Deep Neural Network is created and tunned to its ideal configuration for the classification task. The created DNN model has improved accuracy and offers precise classification, enabling the system to interact with users in a conversational manner and carry out the task of taking food orders.

<br><br>

Let's have a chat with [Qiana](https://qiana.shohrab.com)


<br><br><br><br>


**Table of content**

---

[1. Architecture](#1-architecture)
  - [1.1. Natural Language Processing Unit](#11-natural-language-processing-unit)
    - [1.1.1. Word Tokenization](#111-word-tokenization)
    - [1.1.2. Parts-Of-Speech Tagging](#112-parts-of-speech-tagging)
    - [1.1.3. Lemmatization](#113-lemmatization)
    - [1.1.4. Word Vectorization](#114-word-vectorization)
  - [1.2. Machine Learning Unit](#12-machine-learning-unit)
    - [1.2.1. Learning Curve Evaluation](#121-learning-curve-evaluation)
    - [1.2.2. Confusion Matrix Evaluation](#122-confusion-matrix-evaluation)
    - [1.2.3. Classification Report Evaluation](#123-classification-report-evaluation)
  - [1.3. Response Generation Unit](#13-response-generation-unit)



<br><br><br><br>


# 1. Architecture

Processing textual data is the purpose of a chatbot system. However, the fundamental issue here is that the textual data is unstructured. The textual unstructured data must first be formatted before it can be processed to extract useful information. Natural language processing, which processes textual input and transforms it into a structured format, is used in this study to accomplish this objective. Following that, the machine learning unit can use this structured data to process them further. Intents will be categorized from the unstructured data by this machine learning unit, which was trained using processed text data.When the machine learning model has classified the intent, the response handling unit will generate a response.

The [Natural Language Processing Unit](#11-natural-language-processing-unit) , [Machine Learning Unit](#12-machine-learning-unit), and [Response Generation Unit](#13-response-generation-unit) are the three fundamental units of the chatbot system's architecture. The chatbot's architecture is depicted in the figure.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\Architecture.png" alt="Logo" width="80%"/>
</p>

<br>


> Figure: Architecture


<br><br>
<br><br>



## 1.1. Natural Language Processing Unit

The intention of the Natural Language Processing Unit is to strategically process unstructured text material so that it can be converted to structured format. The message from the client is the data that this unit receives. This message is available in the unstructured form. It will be processed by the NLP unit and transformed into structured data. The image demonstrates how NLP works in its most basic form.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\NLP_unit.png" alt="Logo" width="70%"/>
</p>


<br>

> Figure: Basic Block Diagram of NLP Unit


<br><br>


The pipeline for natural language processing (NLP) includes a variety of phases. Word tokenization, POS tagging, lemmatization, and BOW-based word vectorization are implemented in this research for the NLP unit. The NLP unit's architecture is shown in the figure.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\NLP_Architecture.png" alt="Logo" width="60%"/>
</p>


<br>

> Figure: Architecture of NLP Unit

<br><br><br>

### 1.1.1. Word Tokenization

Tokenizing each word in a sentence is done by the word tokenization unit. Separating each word in a sentence is what this unit is trying to accomplish. This unit tokenizes every word that is received from the client and stores it in an array so that it may be processed in the following unit.


<br><br><br>


### 1.1.2. Parts-Of-Speech Tagging

This unit's goal is to label a word's parts of speech (POS). This unit takes a list of words from the previous unit and tags the words with their appropriate parts of speech. This operation returns an array with a tuple of each member representing a word and its POS.

 
<br><br><br>


### 1.1.3. Lemmatization

Each word in this unit is lemmatized. The purpose of this section is to reduce a word to its lemma, or base word. Different words are changed using this transformation to the same lemma or root word. The origin of the words"am," "are," and "was," for instance, is "be".Language processing is more accurate when a word is converted to its lemma.

 
<br><br><br>


### 1.1.4. Word Vectorization

The objective of this unit is to convert textual data to numerical data; however, the difficulty is retaining the textual data's information in the numerical data. There are numerous methods for converting these textual data to numeric data without compromising any information. The bag-of-word (BOW) technique is utilized in this investigation. The initial step in the BOW technique is the creation of a list of words called the BOW-List, which contains every single unique word from every sentence in the dataset. This BOW list can be sorted alphabetically as required.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\vectorchart.png" alt="Logo" width="60%"/>
</p>

<br>

> Figure: Word Vectorization using Bag-Of-Word Technique 


<br><br>


The figure provides a demonstration of the Bag-Of-Word technique for word vectorization. The BOW-List, which contains all the unique words, is displayed in the top row. The text data is then encoded using an index; if a word matches one on the BOW-list, the entity's value will be 1, else it will be 0. In this study, the frequency of occurrence is stored rather than 1 for each occurrence to increase efficiency. These generate an array of numerical values. In order to do intent classification, this vector is subsequently exported as a data matrix that can be used in the machine learning unit.





<br><br><br><br><br>



## 1.2. Machine Learning Unit

Using the data matrix created in the prior NLP unit, the objective of this machine learning unit is to categorize intents. The raw, unstructured client messages are converted into a structured form by the data matrix, which is an array vector. Based on the structured data, the ML unit predicts the purpose. The figure 36 displays the fundamental operating concept.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\ML_unit.png" alt="Logo" width="70%"/>
</p>

<br>

> Figure: Basic Block Diagram of the ML Unit


<br><br>


Deep Neural Network (DNN) is implemented in the ML unit of this study. The DNN includes five hidden layers, each of which contains a distinct number of neurons. After performing hyperparameter-tuning for all the hyperparameters, some optimal configurations of the parameters are found. The tunned value of the hyperparameters that is used for the DNN design are given in the below table.


<br><br>


**Table: Compiling parameters of the Deep Neural Network**

|  Parameter  Name  | Value |
| :---------------: | :---: |
|     Optimizer     | Adam  |
|  Learning  Rate   | 0.001 |
|    Batch  Size    |  40   |
| Number  of Epochs |  130  |


<br><br>


**Table: Design parameters of the Deep Neural Network**

|      **Layer**       | **Number  of Neurons** | **Activation  Function** | **Drop  Out** |
| :------------------: | :--------------------: | :----------------------: | :-----------: |
|     Input  Layer     |          185           |           tanh           |     0.30      |
| First  Hidden Layer  |          130           |           tanh           |     0.55      |
| Second  Hidden Layer |          245           |           tanh           |     0.15      |
| Third Hidden  Layer  |          160           |           tanh           |     0.40      |
| Fourth  Hidden Layer |           88           |           tanh           |     0.45      |
| Fifth  Hidden Layer  |          175           |           tanh           |     0.30      |
|    Output  Layer     |           22           |         softmax          |    **--**     |



<br><br><br><br>



### 1.2.1. Learning Curve Evaluation

The configuration of the Deep Neural Network is accomplished by utilizing hyperparameter tuning for optimization. The Natural Language Processing Unit generated a data matrix with a total of 334 sets of data, each of which contains 185 features that will be utilized to train the DNN model. This data matrix has been segmented into train and test data at a ratio of 75:15. The learning curve of the training cycle is illustrated below.


<br><br>

<p align=center>
 <img src="readme-lib\results\loss_curve.png" alt="Logo" width="70%"/>
</p>

<br>

> Figure: Learning Curve of Training Cycle 

<br><br>



The curve becomes flat after 40 epochs and stays that way till the training is finished before 100 epochs. The curves do not separate into any gaps. The learning curve demonstrates that the model has an optimal fit.


<br><br><br><br>


### 1.2.2. Confusion Matrix Evaluation

The Confusion Matrix of the training cycle is illustrated in the below figure.

<br><br>

<p align=center>
 <img src="readme-lib\results\confusion_matrix.png" alt="Logo" width="80%"/>
</p>

<br>

> Figure: Confusion Matrix of the Training Cycle 

<br><br>



Only the True Positive and True Negative values are present in the entire class. None of the classes have any False values recorded. The classification report shows that the model is accurate and error-free in its classification


<br><br><br><br>


### 1.2.3. Classification Report Evaluation

The Classification Report includes details on the F1-Score, Accuracy, Precision, and Recall. These metrics give an indication of the model's categorization performance. The classification report's conclusions are depicted in the table below.

<br><br>

**Table: Findings of the Classification Report Analysis**

| Evaluation Metric | Value (%) | Decision |
| :---------------: | :-------: | :------: |
|     Accuracy      |   99.33   |  Ideal   |
|     Precision     |   98.67   |  Ideal   |
|      Recall       |   98.67   |  Ideal   |
|     F1-Score      |   98.00   |  Ideal   |





<br><br><br><br><br>





## 1.3. Response Generation Unit

This unit's objective is to generate responses depending on the purpose that the ML unit has predicted. This system functions essentially as an expert system, with experts mostly defining the replies. The Deep Neural Network model that was created can categorize a total of 22 intents. These 22 intents' responses have previously been specified. Some of these intents call for database queries in order to generate responses. The intended response can be of two types, Rule Based Response and Task Based Response, depending on the necessity of the database query. The basic working principle of this unit is illustrated in the below figure.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\Response-Generation-Unit.png" alt="Logo" width="70%"/>
</p>

<br>

> Figure: Basic Block Diagram of Response Generation Unit 

<br><br>



A series of If-This-Then-That rules is used in rule-based responses. For instance, if this intent is found, then provide that response. To complete the Task Based Response, a database search is necessary for more details. With these extra details, the response is finished and sent to the client. The below figure 39 illustrates the architecture of the Response Generation Unit.


<br><br>

<p align=center>
 <img src="readme-lib\architecture\RGU-Architecture.png" alt="Logo" width="60%"/>
</p>

<br>

> Figure: Architecture of Response Generation Unit

<br><br><br>





* **Rule Based Response Generation (Static):** This response generation is active if the intent has a response type that is rule-based. The relevant IF-THIS-THEN-THAT rule base is queried in this response generation in order to derive the necessary response. When a dynamic response is not necessary, this form of answer is used. For instance, if the customer greets, the response is the greetings response, which is usually always the same.

<br><br>

* **Task Based Response Generation (Dynamic):** This response generation triggers if the intent has a task-based response type. When a dynamic response is necessary, this response generation is used. For instance, if a consumer requests information about a food item's price, the system must search the database to find the item's price before producing a response containing the requested information. The system must extract the keywords from the customer's query in order to generate the response. For instance, the food's brand name,serving size, etc.


<br><br><br><br><br><br>




---
<br><br>

Let's have a chat: [Qiana](https://qiana.shohrab.com)

<br><br><br><br>
