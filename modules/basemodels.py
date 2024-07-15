# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This module contains the main classes
that will be employed by all GeneSys modules in order to manipulate
machine learning algorythms

It requires the following packages:
    -> scikitlearn
    -> imblearn
    -> numpy
    -> pandas
    -> probaly BLAST
"""

# import math
# from src import utils as ut
from abc import abstractmethod

import numpy as np
import pandas as pd

"""
Import Packages and import functions for modeling
"""
# from sklearn.linear_model import LogisticRegression as skLogisticRegression
# from sklearn.naive_bayes import GaussianNB
# from sklearn.ensemble import RandomForestClassifier as skRandomForestClassifier
# from sklearn.neural_network import MLPClassifier as skMLPClassifier
# from sklearn.svm import SVC

from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score,roc_curve, precision_recall_curve, auc

from imblearn.pipeline import Pipeline

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
#from sklearn.model_selection import GridSearchCV

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class ModelSelection():
    """This class performs different techniques to the data such as: splitting data,
    over-sampling and under-sampling, normalization, computes confusion matrix and AUC, etc.,
    to the data in order to improve Machine Learning algorithm's performance.
    
    :param data: The data to apply Machine Learning methods. Defaults to None.
        If it is not specified, user must provide the 'source' and 'target' values.
    :type data: DataFrame
    :param source: The features that describe the samples. Defaults to None.
        If it is noy specified, user must provide 'data' value. 
        Otherwise, if it is different to None, 'target' values must be provided.
    :type source: DataFrame
    :param target: The labels to be predicted. Defaults to None.
        If it is noy specified, user must provide 'data' value. 
        Otherwise, if it is different to None, 'source' values must be provided.
    :type target: Series
    :param X_train: All the observations that will be used to train the model.
        Defaults to None. Only can be updated after use 'get_train_test_sample' method.
    :type X_train: DataFrame
    :param Y_train: The dependent variable wich need to be predicted by the model.
        Defaults to None. Only can be updated after use 'get_train_test_sample' method.
    :type Y_train: Series
    :param X_test:  The remaining portion of the independent  variables which 
        will not be used in the training phase and will be used
        to make predictions to test the accuracy of the model.
        Defaults to None. Only can be updated after use 'get_train_test_sample' method.
    :type X_test: DataFrame
    :param Y_test: The labels of the test data. These labels will be used to test 
        the accuracy between actual and predicted categories. Defaults to None.
        Only can be updated after use 'get_train_test_sample' method.
    :type Y_test:  Series
    """
    
    """Constructor method
    """  
    def __init__(self, data = None, source = None, target = None):  
        
        self.data = data 
        self.source = source
        self.target = target
        self.X_train = None
        self.Y_train = None
        self.X_test = None
        self.Y_test = None
        
    """
    GET
    """
        
    def get_data(self):
        """Returns a DataFrame with the data to apply Machine Learning methods.
        
        :return: The data to apply Machine Learning methods.
        :rtype: DataFrame
        """
        return self.data
    
    def get_source(self):
        """Returns a DataFrame with the attributes used to describe each example.
        
        :return: The features that describe the samples.
        :rtype: DataFrame
        """
        return self.source
    
    def get_target(self):
        """Returns a Series object with the labels to be predicted.
        
        :return: The labels to be predicted.
        :rtype: Series
        """
        return self.target
    
    def get_X_train(self):
        """Returns a DataFrame with all the observations that will be used to
        train the model.
        
        :return: All independent variables used to train the model.
        :rtype: DataFrame
        """
        return self.X_train
    
    def get_Y_train(self):
        """Returns a Series object with the dependent variables which need to be
        predicted by the model.
        
        :return: The dependent variable wich need to be predicted by the model.
        :rtype: Series
        """
        return self.Y_train
    
    def get_X_test(self):
        """Returns a DataFrame with the remaining portion of the independent 
        variables which will not be used in the training phase and will be used
        to make predictions to test the accuracy of the model.
        
        :return: Remaining observations to test the accuracy of the model.
        :rtype: DataFrame
        """
        return self.X_test
    
    def get_Y_test(self):
        """Returns a Series object with the labels of the test data. These labels
        will be used to test the accuracy between actual and predicted categories.
        
        :return: The labels to test the accuracy of the model.
        :rtype: Series
        """
        return self.Y_test
    

    """
    SET
    """
    
    def set_data(self, data):
        """Set the data to apply Machine Learning methods.
        
        :param data: The data to apply Machine Learning methods.
        :type data: DataFrame 
        """
        self.data = data
        
    def set_source(self, source):
        """Set the features that describe the samples.
        
        :param source:  The features that describe the samples.
        :type source: DatFrame 
        """
        self.source = source
        
    def set_target(self, target):
        """Set the labels to be predicted.
        
        :param target: The labels to be predicted.
        :type target: Series 
        """
        self.target = target
        
    def set_X_train(self, x_train):
        """Set the independent variables used to train the model.
        
        :param x_train: All independent variables used to train the model.
        :type x_train: DataFrame 
        """
        self.X_train = x_train
        
    def set_Y_train(self, y_train):
        """Set the dependent variable wich need to be predicted by the model.
        
        :param y_train: The dependent variables wich need to be predicted by the model.
        :type y_train: Series 
        """
        self.Y_train = y_train
        
    def set_X_test(self, x_test):
        """Set the remaining observations to test the accuracy of the model.
        
        :param x_test: Remaining observations to test the accuracy of the model.
        :type x_test: DataFrame 
        """
        self.X_test = x_test
        
    def set_Y_test(self, y_test):
        """Set the labels to test the accuracy of the model.
        
        :param y_test: The labels to test the accuracy of the model.
        :type y_test: str 
        """
        self.Y_test = y_test


    def split_data(self):   
        """Split input data into sources (samples) and target (labels).
        Target data will be the last column of the data.

        """
        x, y = self.get_data().iloc[:,:-1], self.get_data().iloc[:,-1]   
        
        self.set_source(x)
        self.set_target(y)     
    

    def get_train_test_sample(self, test_size = 0.2, resample = False, shuffle = True):
        """Split the data into random train and test subsets.
        If 'resample' is 'True', Smote and Underasmpler techniques will be also applied
        to resample imbalanced data.
        
        :param test_size: If float, should be between 0.0 and 1.0 and represent 
            the proportion of the dataset to include in the test split. 
            If int, represents the absolute number of test samples. 
            If None, the value is set to the complement of the train size. 
            Defaults to '0.2'.
        :type test_size: float, int or None
        :param resample: If 'True', data will be resampled, 'False' will not modify 
            the data. Defaults to 'False'.
        :type resample: bool
        :param shuffle: Whether or not to shuffle the data before splitting.
            Dafaults to 'True'.
        :type shuffle: bool
        """
        
        if resample == True:
            self.over_under_sample(o_samp_str = 0.5, u_samp_str = 0.8)
                                                                                                                                                                                                                                                                                                                                                                                       
        X_train, X_test, Y_train, Y_test = train_test_split(self.get_source(), self.get_target(), test_size = test_size, shuffle = shuffle)
        
        self.set_X_train(X_train)
        self.set_X_test(X_test)
        self.set_Y_train(Y_train)
        self.set_Y_test(Y_test)



    def apply_smote(self, sampling_strategy = "auto", random_state = None, k_neighbors = 5, n_jobs = None):
        """Applies SMOTE (Synthetic Minority Over-sampling Technique) to perform
        over-sampling.
        
        For more information, see imbalanced learn documentation:
        https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html
        
        :param sampling_strategy: Sampling information to resample the data set.
            Defaults to 'auto'.
        :type sampling_strategy: float, str, dict or callable
        :param random_state: Control the randomization of the algorithm. Defaults to None.
        :type random_state: int, RandomState instance or None
        :param k_neighbors: Number of neighbours to used to construct synthethic samples.
            Defaults to '5'.
        :type k_neighbors: int or Object
        :param n_jobs: Number of CPU cores used during the cross-validation loop. Defaults to None.
        :type n_jobs: int
        """
        
        over = SMOTE(sampling_strategy = sampling_strategy, random_state = random_state, k_neighbors = k_neighbors, n_jobs = n_jobs)
        
        X_res, Y_res = over.fit_resample(self.get_source(), self.get_target())
        self.set_source(X_res)
        self.set_target(Y_res)  



    def apply_undersampler(self, sampling_strategy = "auto", random_state = None, replacement = False):
        """Applies RandomUnderSampler  to perform random under-sampling.
        The method under-sample the majority class(es) by randomly picking samples 
        with or without replacement.
        
        For more information, see imbalanced learn documentation:
        https://imbalanced-learn.org/stable/references/generated/imblearn.under_sampling.RandomUnderSampler.html
        
        :param sampling_strategy: Sampling information to resample the data set.
            Defaults to 'auto'.
        :type sampling_strategy: float, str, dict or callable
        :param random_state: Control the randomization of the algorithm. Defaults to None.
        :type random_state: int, RandomState instance or None
        :param replacement: Whether the sample is with or without replacement. Defaults to False.
        :type replacement: bool
        """
        
        under = RandomUnderSampler(sampling_strategy = sampling_strategy, random_state = random_state, replacement = replacement)

        X_res, Y_res = under.fit_resample(self.get_source(), self.get_target())
        self.set_source(X_res)
        self.set_target(Y_res) 
    
    
    def over_under_sample(self, o_samp_str = "auto", u_samp_str = "auto", o_random_st = None, u_random_st = None):
        """Combines over and under sample to avoid over-fitting or missing too much information.
        Both techniques will be combines by using Pipeline from imblearn, that provides a pipeline
        by applying a list of transformations, and resamples, with a final estimator.
        
        :param o_samp_str: For SMOTE, sampling information to resample the data set.
            Defaults to 'auto'.
        :type o_samp_str: float, str, dict or callable
        :param u_samp_str: For UnderSampler, sampling information to resample the data set.
            Defaults to 'auto'.
        :type u_samp_str: float, str, dict or callable
        :param o_random_st: For SMOTE, control the randomization of the algorithm. 
            Defaults to None.
        :type o_random_st: int, RandomState instance or None
        :param u_random_st: For UnderSampler, control the randomization of the algorithm. 
            Defaults to None.
        :type u_random_st: int, RandomState instance or None
        """
        
        over = SMOTE(sampling_strategy = o_samp_str)
        
        under = RandomUnderSampler(sampling_strategy = u_samp_str)
        
        steps = [('o', over), ('u', under)]
        pipeline = Pipeline(steps)
        
        X_res, Y_res = pipeline.fit_resample(self.get_source(), self.get_target()) 
        
        self.set_source(X_res)
        self.set_target(Y_res) 



    def standarize(self):
        """Normalize the data standarizing features by removing the man ands scaling to unit variance.
        With it, the mean will be 0 and the standard deviation will be 1, following the equation:
        X_stand = (x - mean(x)) / standard deviation(x)
        
        For more information, see:
        https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html     
        """
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        scaler = StandardScaler()
        
        # Fit only to the training data
        scaler.fit(self.get_X_train())
        
        # Now apply the transformations to the data:
        X_train = scaler.transform(self.get_X_train())
        X_test = scaler.transform(self.get_X_test())     
           
        self.set_X_train(X_train)
        self.set_X_test(X_test)
    
 
    def get_predictions(self, probabilities, threshold=0.5):    
        """Get prediction values.
        
        :param probabilities: list of probabilities of the X data that represent a percentage of its result
        :type probabilities: list 
        :param threshold: a limit to indicates when the classification will be 0 or 1
        :type threshold: float

        :return: a predicted values by probabilities
        :rtype: list
        """

        predict_res = np.where(probabilities <= threshold, 0, 1)
     
        return predict_res 
        
    def predict_proba(self, model):
        """Predcit probabilities for a given model
        
        :param model: Model to predict a given value
        :type model: object
        :return: predicted values
        :rtype: array
        """

        return model.get_model().predict_proba(self.get_X_test())[:,1]
 

    def confusion_matrix(self, Y_pred, labels = None, sample_weight = None):
        """Compute confusion matrix to evaluate the accuracy of a classification.
        By definition, a confusion matrix C is such that Cij is equal to the number
        of observations known to be in group i and predicted to be in group j.
        
        For more information, see scikit learn documentation:
        https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
            
        :param Y_pred: Estimated targets as returned by a classifier.
        :type Y_pred: array of shape n_samples
        :param labels: List of labels to index the matrix. Defaults to None.
        :type labels: array of shape n_classes or None
        :param sample_weight: Sample weights. Defaults to None.
        :type sample_weight: array of shape n_samples or None

        :return: Confusion matrix whose i-th row and j-th column entry indicates 
            the number of samples with true label being i-th class and 
            predicted label being j-th class.
        :rtype: ndarray
        """
        
        return(confusion_matrix(self.get_Y_test(), Y_pred, sample_weight = sample_weight))
    
           
    def calc_auc(self, predictions, curve = "roc"):
        """AUC stands for "Area under the ROC Curve". That is, AUC measures the entire
        two-dimensional area underneath the entire ROC curve from (0,0) to (1,1)
        The Precission-Recall AUC is just like the ROC AUC. in that it summarizes the curve with a range
        of threshold values as a single score.
        
        :param predictions: Target scores, can either be probability estimates 
            of the positive class, or non-thresholded measure of decisions.
        :type predictions: ndarray of shape n_samples
        :param curve: If 'roc', computes Receiver Operatic Characteristic (ROC) curve,
            if 'precision-recall', computes Precision-Recall curve.
        :type curve: str

        :return: Returns the Area Under the Curve (AUC)
        :rtype: float
        """

        # https://machinelearningmastery.com/roc-curves-and-precision-recall-curves-for-imbalanced-classification/#:~:text=The%20Precision%2DRecall%20AUC%20is,a%20model%20with%20perfect%20skill.
        auc_score = -1
        
        if curve == "roc":
        
            fpr, tpr, _ = roc_curve(self.get_Y_test(), predictions)
            auc_score = auc(fpr, tpr)  
            
        elif curve == "precision-recall":
            
            precision, recall, _ = precision_recall_curve(self.get_Y_test(), predictions)
            auc_score = auc(recall, precision)    
            
        else:
            print("Invalid state of curve passed.")
        
        return auc_score 


    def cross_validation(self, model, n_splits = 10, n_jobs = None):
        """Computes K-fold Corss-Validation and evaluate the metric(s) by using
        StratifiedKFold and cross_validate from scikit-learn
        
        StratifiedKFold:
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
        cross_validate:
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html   
        
        :param model: Machine Learning algorithm to apply cross-validation.
        :type model: 
        :param n_splits: Number of folds. Must be at least 2. Defaults to 10.
        :type n_splits: int
        :param n_jobs: Number of jobs to run in parallel. Training the estimator
            and computing the score are parallelized over the cross-validation splits.
            Defaults to None
        :type n_jobs: int

        :return: The function will return a dictionary containing the metrics "accuracy",
            "precision", "recall", and "f1" for boith training and validation sets.
        :rtype: dict
        """

        # Indices obtained according to the number of partitions for the cross validation
        # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedKFold.html
        cv = StratifiedKFold(n_splits = n_splits , shuffle = True, random_state = 1)
        
        scores = ['accuracy', 'precision', 'recall', 'f1']
        
        results = cross_validate(estimator = model,
                                 X = self.get_source(),
                                 y = self.get_target(),
                                 cv = cv,
                                 scoring = scores,
                                 return_train_score = True)
        
        return {"Training Accuracy scores": results['train_accuracy'],
                "Mean Training Accuracy": results['train_accuracy'].mean()*100,
                
                "Training Precision scores": results['train_precision'],
                "Mean Training Precision": results['train_precision'].mean(),
                
                "Training Recall scores": results['train_recall'],
                "Mean Training Recall": results['train_recall'].mean(),
                
                "Training F1 scores": results['train_f1'],
                "Mean Training F1 Score": results['train_f1'].mean(),
                
                "Validation Accuracy scores": results['test_accuracy'],
                "Mean Validation Accuracy": results['test_accuracy'].mean()*100,
                
                "Validation Precision scores": results['test_precision'],
                "Mean Validation Precision": results['test_precision'].mean(),
                
                "Validation Recall scores": results['test_recall'],
                "Mean Validation Recall": results['test_recall'].mean(),
                
                "Validation F1 scores": results['test_f1'],
                "Mean Validation F1 Score": results['test_f1'].mean()
                }

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class Model():
    """This is a conceptual class representation of a model that can be used
    with Machine Learning algorithms.
    
    :param name: Name of the model.
    :type name: str
    :param model: Model to work with.
    :type model: object
    """
        
    def __init__(self, name, model = None):  
        self.name = name
        self.model = model
        
    def get_name(self):
        """Returns a string with the name of the model.
        
        :return: The name of the model.
        :rtype: str
        """
        return self.name

    def get_model(self):
        """Returns the model to work with.
        
        :return: The model to work with.
        :rtype: object
        """
        return self.model

        
    def set_name(self, name):
        """Set the name of the model.
        
        :param name: The name of the model.
        :type name: str 
        """
        self.name = name
        
    def set_model(self, model):
        """Set the model to work with.
        
        :param model: The model to work with.
        :type model: object
        """
        self.model = model

    def fit(self, X_train, Y_train):
        """Fit (train) the model.
       
        :param X_train: All independent variables used to train the model.
        :type X_train: DataFrame
        :param Y_train: The dependent variables wich need to be predicted by the model.
        :type Y_train: Series
        """
        
        (self.get_model()).fit(X_train, Y_train)
              
    def predict(self, X_test):
        """ Given an unlabeled observations X, returns the predicted labels Y.
       
        :param X_test: Remaining observations to test the accuracy of the model.
        :type X_test: DataFrame
        :return: Returns the predicted labels Y.
        :rtype: Series
        """
        return (self.get_model()).predict(X_test.values)
    
    @abstractmethod 
    def get_metrics(self, Y_true, Y_pred, y_pred_proba=None):    
        raise NotImplementedError("Must override get_metrics")
    
##############################################################################
##############################################################################
##############################################################################
##############################################################################
            
class ScikitLearnModel(Model):
    """This is a conceptual class representation of a model that is provided by
    the Scikit-learn library.

    :param name: Name of the model.
    :type name: str
    :param model: Model to work with.
    :type model: object
    """
    
    def __init__(self, name, model = None):
        # Call the __init__ function of the father class
        super().__init__(name, model)

        
    @abstractmethod 
    def hyperparameter_tuning(X_train, Y_train):
        raise NotImplementedError("Must override hyperparameter_tuning")
    

    def get_metrics(self, Y_true, Y_pred, y_pred_proba=None): 
        """Computes the metrics "accuracy", "precision", "recall", "specifity" and "f1" 
        for a specified model and returns a Dataframe with all the information.
       
        :param Y_true: Ground truth (correct) target values.
        :type Y_true: array
        :param Y_pred: Estimated targets as returned by a classifier.
        :type Y_pred: array
        :return: Returns a DataFrame with all the metrics.
        :rtype: DataFrame
        """
        
        cv_scores = []  

        cm = confusion_matrix(Y_true,Y_pred)

        # Precision indicates the proportion of positive indentifications that are actually correct
        precision = precision_score(Y_true, Y_pred)
        
        # Recall (Sensivity) indicates the proportion of actual positives that were identified correctly
        recall = recall_score(Y_true, Y_pred)
        
        # Specificity indicates the proportion of actual negatives, which got predicted as the negative
        specificity = cm[0,0] / (cm[0,0] + cm[0,1])  
        
        # F1-Score is the weighted average of Precision and Recall, taking both false positives and
        # false negatives into account
        f1 = f1_score(Y_true, Y_pred)  
        
        # Accuracy ratio of correctly  predicted observation to the total observations
        accuracy = accuracy_score(Y_true, Y_pred)
    
        cv_scores.append([self.get_name(), precision, recall, specificity, f1, accuracy])    
        results_df = pd.DataFrame(cv_scores, columns=['model_name', 'precision', 'recall', 'specificity', 'f1', 'accuracy'])
    
        return results_df
     