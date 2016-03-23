#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from models import Question
from models import Answer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class AskForm(forms.Form):
    title = forms.CharField(max_length=256)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AskForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        # if not title:
            # raise forms.ValidationError(u'The title field is empty', code=12)
        return title

    def save(self):
        self.cleaned_data["author"] = self._user
        return Question.objects.create(**self.cleaned_data)
        # question = Question(**self.cleaned_data)
        # question.save()
        # return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_question(self):
        question = self.cleaned_data['question']
        if question == 0:
            raise forms.ValidationError(u'Answer need question', code = 12)
        return question

    def clean_text(self):
        text = self.cleaned_data['text']
        if text.strip() == '':
            raise forms.ValidationError(u'The text field is empty', code=12)
        return text

    def save(self):
        self.cleaned_data['author'] = self._user
        self.cleaned_data['question'] = get_object_or_404(Question, pk=self.cleaned_data['question'])
        return Answer.objects.create(**self.cleaned_data)
        # self.cleaned_data["author_id"] = 1
        # answer = Answer(**self.cleaned_data)
        # answer.save()
        # return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=64)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 64:
            raise forms.ValidationError('Username is too long', code='Long_name')
        return username

    def save(self):
        return User.objects.create_user(**self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 64:
            raise forms.ValidationError('Username is too long', code='Long_name')
        return username