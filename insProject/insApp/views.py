from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
#from .forms import *
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
ListView,DetailView,
CreateView,DeleteView,
UpdateView)
from . import models
from .forms import *
from django.core.files.storage import FileSystemStorage
#from topicApp.Topicfun import Topic
#from ckdApp.funckd import ckd
#from sklearn.tree import export_graphviz #plot tree
#from sklearn.metrics import roc_curve, auc #for model evaluation
#from sklearn.metrics import classification_report #for model evaluation
##from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(df2.drop('classification_yes', 1), df2['classification_yes'], test_size = .2, random_state=10)

import time
import pandas as pd
import numpy as np
#from sklearn.preprocessing import StandardScaler
#from sklearn.feature_selection import SelectKBest
#from sklearn.feature_selection import chi2
#from sklearn.model_selection import train_test_split
#from sklearn.decomposition import PCA
#from sklearn.feature_selection import RFE
#from sklearn.linear_model import LogisticRegression
import pickle
import matplotlib.pyplot as plt
#import eli5 #for purmutation importance
#from eli5.sklearn import PermutationImportance
#import shap #for SHAP values
#from pdpbox import pdp, info_plots #for partial plots
np.random.seed(123) #ensure reproduc
class dataUploadView(View):
    form_class = insForm
    success_url = reverse_lazy('success')
    template_name = 'create.html'
    failure_url= reverse_lazy('fail')
    filenot_url= reverse_lazy('filenot')
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    def post(self, request, *args, **kwargs):
        #print('inside post')
        form = self.form_class(request.POST, request.FILES)
        #print('inside form')
        if form.is_valid():
            form.save()
            a=request.POST.get('age')
            b=request.POST.get('bmi')
            c=request.POST.get('children')
            sm=request.POST.get('sex_male')
            sy=request.POST.get('smoker_yes')
            import pandas as pd
            dataset=pd.read_csv("insurance_pre.csv")
            dataset
            dataset=pd.get_dummies(dataset,drop_first=True)
            dataset
            dataset.columns
            independent=dataset[['age', 'bmi', 'children','sex_male', 'smoker_yes']]
            independent
            dependent=dataset[["charges"]]
            dependent
            from sklearn.model_selection import train_test_split
            x_train,x_test,y_train,y_test= train_test_split(independent,dependent,test_size=0.30,random_state=0)
            from sklearn.ensemble import RandomForestRegressor
            regressor=RandomForestRegressor(criterion="absolute_error",n_estimators=100,random_state=0,max_features="log2")
            regressor.fit(x_train,y_train)
            y_pred=regressor.predict(x_test)
            from sklearn.metrics import r2_score
            r_score=r2_score(y_test,y_pred)
            r_score

            data = np.array([a,b,c,sm,sy])
            out=regressor.predict(data.reshape(1,-1))

            return render(request, "succ_msg.html", {'a':a,'b':b,'c':c,'sm':sm,'sy':sy,'out':out})
        else:
            return redirect(self.failure_url)
