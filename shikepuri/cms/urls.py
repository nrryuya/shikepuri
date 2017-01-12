from django.conf.urls import url
from cms import views

urlpatterns = [
    # ファイル
    url(r'^file/list/$', views.file_list, name='file_list'),   # 一覧
    url(r'^file/list/(?P<category>[\w\-]+)/$', views.file_list, name='file_list'),   # 一覧
    url(r'^file/list/(?P<category>[\w\-]+)/(?P<subject>[\w\-]+)/$',
        views.file_list, name='file_list'),   # 一覧
    url(r'^file/content/(?P<file_id>\d+)/$', views.file_content, name='file_content'),  # 中身
    url(r'^file/add/$', views.file_edit, name='file_add'),  # 登録
    url(r'^file/mod/(?P<file_id>\d+)/$', views.file_edit, name='file_mod'),  # 修正
    url(r'^file/del/(?P<file_id>\d+)/$', views.file_del, name='file_del'),   # 削除
    # コメント欄
    url(r'^comments/(?P<file_id>\d+)/$', views.CommentsList.as_view(), name='comments_list'),  # 一覧
    url(r'^comments/add/(?P<file_id>\d+)/$', views.comments_edit, name='comments_add'),        # 登録
    url(r'^comments/mod/(?P<file_id>\d+)/(?P<comments_id>\d+)/$',
        views.comments_edit, name='comments_mod'),  # 修正
    url(r'^comments/del/(?P<file_id>\d+)/(?P<comments_id>\d+)/$',
        views.comments_del, name='comments_del'),   # 削除
    # リプライ
    url(r'^replies/(?P<file_id>\d+)/(?P<comments_id>\d+)/$',
        views.reply_list, name='reply_list'),  # 一覧
    url(r'^replies/add/(?P<file_id>\d+)/(?P<comments_id>\d+)/$',
        views.reply_edit, name='reply_add'),
    url(r'^replies/mod/(?P<file_id>\d+)/(?P<comments_id>\d+)/(?P<reply_id>\d+)/$',
        views.reply_edit, name='reply_mod'),
    url(r'^replies/del/(?P<file_id>\d+)/(?P<comments_id>\d+)/(?P<reply_id>\d+)/$',
        views.reply_del, name='reply_del'),
]
