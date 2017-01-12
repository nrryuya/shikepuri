from django.forms import ModelForm
from django import forms
from cms.models import File, Comments, Reply


class FileForm(ModelForm):
    """ファイルのフォーム"""

    pdf = forms.FileField()

    class Meta:
        model = File
        fields = ('name', 'subject', 'class_name', 'teacher', )


class CommentsForm(ModelForm):
    """コメント欄のフォーム"""
    class Meta:
        model = Comments
        fields = ('comments', )


class ReplyForm(ModelForm):
    """リプライのフォーム"""
    class Meta:
        model = Reply
        fields = ('reply', )
