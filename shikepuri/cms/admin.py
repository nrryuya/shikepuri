from django.contrib import admin
from cms.models import File, Comments


# admin.site.register(File)
# admin.site.register(Comments)

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'page', 'pdf')  # 一覧に出したい項目
    list_display_links = ('id', 'name', 'pdf')  # 修正リンクでクリックできる項目


admin.site.register(File, FileAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'comments',)
    list_display_links = ('id', 'comments',)


admin.site.register(Comments, CommentsAdmin)
