from cms.models import File, Comments, Reply
from cms.forms import FileForm, CommentsForm, ReplyForm

from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.template.context_processors import csrf

import sys
import os


@login_required
def file_list(request, category=None, subject=None):
    """ファイルの一覧"""
    if subject is None:
        if category is None:
            files = File.objects.all().order_by('id')
        else:
            files = File.objects.filter(category=category).order_by('id')
    elif not category is None:
        files = File.objects.filter(category=category, subject=subject).order_by('id')

    subject_name = get_subject_name(File.subject_list, File.subject_name_list, subject)
    return render(request,
                  'cms/file_list.html',     # 使用するテンプレート
                  {'files': files, 'category': category, 'subject': subject, 'subject_name': subject_name, 'category_list': File.category_list, 'subject_list': File.subject_list, 'subject_name_list': File.subject_name_list})         # テンプレートに渡すデータ


def get_subject_name(subject_list, subject_name_list, subject):
    n = len(subject_list)
    for i in range(n):
        if subject in subject_list[i]:
            k = subject_list[i].index(subject)
            return subject_name_list[i][k]


@login_required
def file_content(request, file_id):
    """ファイルの中身"""

    file = get_object_or_404(File, pk=file_id)
    comments = file.comments.all().order_by('id')   # ファイルの子供の、コメント欄を読む

    # コメントidの最大の数と同じ要素数をもつリスト
    last_comments = Comments.objects.all().order_by("-id")[0]
    n = last_comments.id + 1
    replies = n * [0]
    for comment in comments:
        replies[comment.id] = []
        replies[comment.id].append(comment.reply.all().order_by('id'))

    return render(request,
                  'cms/file_content.html',     # 使用するテンプレート
                  {'file': file, 'comments': comments, 'replies': replies})  # テンプレートに渡すデータ


@login_required
def file_edit(request, file_id=None):
    """ファイルの編集"""
    if file_id:   # file_id が指定されている (修正時)
        file = get_object_or_404(File, pk=file_id)
    else:         # file_id が指定されていない (追加時)
        file = File()

    if request.method == 'POST':
        # # csrf
        # c = {}
        # c.update(csrf(request))
        # return render_to_response('cms/file_edit.html', c)

        form = FileForm(request.POST, request.FILES, instance=file)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            file = form.save(commit=False)
            file.author = request.user
            file.category = find_parent(
                # File.category_list, File.subject_list, form.cleaned_data['subject'])
                File.category_list, File.subject_list, file.subject)
            file.save()
            file_save(request.FILES['pdf'], file.id)
            return redirect('cms:file_list')
    else:    # GET の時
        form = FileForm(instance=file)  # file インスタンスからフォームを作成

    return render(request, 'cms/file_edit.html', dict(form=form, file_id=file_id))


# @login_required←これをつけると'InMemoryUploadedFile' object has no attribute 'user'になる
def file_save(file, id):
    """pdfファイルの保存"""
    os.mkdir(os.path.join(settings.MEDIA_ROOT, str(id)))
    path = os.path.join(settings.MEDIA_ROOT, str(id), str(
        id) + ".pdf")  # media/files/(id)/(id).pdfとして保存される
    destination = open(path, 'wb')  # バイナリモードで書き込みのファイル操作
    for chunk in file.chunks():  # メモリに配慮し chunk
        destination.write(chunk)
    destination.close()


# 科目名（DEなど）からカテゴリ（基礎科目など）を取得するためのメソッド
def find_parent(pl, cl, child):
    n = len(pl)
    for i in range(n):
        if child in cl[i]:
            return pl[i]
            break
        if i == n:
            return None


@login_required
def file_del(request, file_id):
    """ファイルの削除"""
    file = get_object_or_404(File, pk=file_id)
    file.delete()
    return redirect('cms:file_list')


@method_decorator(login_required, name='dispatch')
class CommentsList(ListView):
    """コメント欄の一覧"""
    context_object_name = 'comments'
    template_name = 'cms/comments_list.html'
    paginate_by = 2  # １ページは最大2件ずつでページングする

    def get(self, request, *args, **kwargs):
        file = get_object_or_404(File, pk=kwargs['file_id'])  # 親のファイルを読む
        comments = file.comments.all().order_by('id')   # ファイルの子供の、コメント欄を読む
        self.object_list = comments

        context = self.get_context_data(object_list=self.object_list, file=file)
        return self.render_to_response(context)


@login_required
def comments_edit(request, file_id, comments_id=None):
    """コメント欄の編集"""
    file = get_object_or_404(File, pk=file_id)  # 親の書籍を読む
    if comments_id:   # comments_id が指定されている (修正時)
        comments = get_object_or_404(Comments, pk=comments_id)
    else:               # comments_id が指定されていない (追加時)
        comments = Comments()

    if request.method == 'POST':
        form = CommentsForm(request.POST, instance=comments)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            comments = form.save(commit=False)
            comments.author = request.user
            comments.file = file  # このコメント欄の、親の書籍をセット
            comments.save()
            return redirect('cms:file_content', file_id=file_id)

    else:    # GET の時
        form = CommentsForm(instance=comments)  # comments インスタンスからフォームを作成

    return render(request,
                  'cms/comments_edit.html',
                  dict(form=form, file_id=file_id, comments_id=comments_id))


@login_required
def comments_del(request, file_id, comments_id):
    """コメント欄の削除"""
    comments = get_object_or_404(Comments, pk=comments_id)
    comments.delete()
    return redirect('cms:comments_list', file_id=file_id)


@login_required
def reply_list(request, file_id, comments_id):
    """リプライ一覧"""

    file = get_object_or_404(File, pk=file_id)
    comments = get_object_or_404(Comments, pk=comments_id)
    replies = comments.reply.all().order_by('id')   # ファイルの子供の、コメント欄を読む

    return render(request,
                  'cms/reply_list.html',     # 使用するテンプレート
                  {'file': file, 'comments': comments, 'replies': replies})  # テンプレートに渡すデータ


# reply_listを呼び出す時に、file_idとcomments_idの両方をfile_contentで渡すのを忘れていた
# 下記のメソッドのように、commentsというインスタンスとしてではなく、comments_idという変数で渡している場合は、templatesでもそう呼び出す
@login_required
def reply_edit(request, file_id, comments_id, reply_id=None):
    """コメント欄の編集"""
    file = get_object_or_404(File, pk=file_id)
    comments = get_object_or_404(Comments, pk=comments_id)  # 親の書籍を読む
    if reply_id:   # comments_id が指定されている (修正時)
        reply = get_object_or_404(Reply, pk=reply_id)
    else:               # comments_id が指定されていない (追加時)
        reply = Reply()

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comments = comments  # このコメント欄の、親の書籍をセット
            reply.save()
            return redirect('cms:file_content', file_id=file_id)
    else:    # GET の時
        form = ReplyForm(instance=reply)  # comments インスタンスからフォームを作成

    return render(request,
                  'cms/reply_edit.html',
                  dict(form=form, file_id=file_id, comments_id=comments_id, reply_id=reply_id))


@login_required
def reply_del(request, file_id, comments_id, reply_id):
    """コメント欄の削除"""
    reply = get_object_or_404(Reply, pk=reply_id)
    reply.delete()
    return redirect('cms:reply_list', file_id=file_id, comments_id=comments.id)
