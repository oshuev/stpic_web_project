#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from models import Question
from models import Answer

from django.shortcuts import get_object_or_404

class AskForm(forms.Form):
    title = forms.CharField(max_length=256)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        # if not title:
            # raise forms.ValidationError(u'The title field is empty', code=12)
        return title

    def save(self):
        self.cleaned_data["author_id"] = 1
        question = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError(u'The text field is empty', code=12)
        return text

    def save(self):
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        self.cleaned_data["author_id"] = 1
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer