# -*- coding: utf-8 -*-

from django import forms

class SensorSearchForm(forms.Form):

    sen_nombre = forms.CharField(required=False)
    sen_marca = forms.CharField(required=False)
