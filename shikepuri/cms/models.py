from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    """ファイル"""
    name = models.CharField('ファイル名', max_length=255)
    author = models.ForeignKey(User)
    page = models.IntegerField('ページ数', blank=True, default=0)  # 未使用
    pdf = models.FileField()  # これが機能しているのか不明。単にviews.file_saveでidと同じ名前でMEDIAに保存されているだけかも。

    SUBJECT_CHOICES = (
        ('基礎科目', (
            ('EN', '英語'),
            ('DE', 'ドイツ語'),
            ('FR', 'フランス語'),
            ('ZH', '中国語'),
            ('ES', 'スペイン語'),
            ('JH', '情報'),
            ('SU', '身体運動・健康科学実習'),
            ('SK', '社会科学'),
            ('ZB', '人文科学'),
            ('HH', '方法基礎'),
            ('KZ', '基礎実験'),
            ('MK', '数理科学'),
            ('BK', '物質科学'),
            ('BI', '生命科学'),
        )
        ),
        ('総合科目A', (
            ('SH', '科学史'),
            ('HB', '表象文化論'),
        )
        ),
        ('総合科目B', (
            ('JL', '日本語上級'),
        )
        ),
    )

    category_list = ['基礎科目',
                     '総合科目A',
                     '総合科目B'
                     ]

    subject_list = [
        ['EN',
         'DE',
         'FR',
         'ZH',
         'ES',
         'JH',
         'SU',
         'SK',
         'ZB',
         'HH',
         'KZ',
         'MK',
         'BK',
         'BI'],
        ['SH',
         'HB'],
        ['JL']
    ]

    subject_name_list = [
        ['英語',
         'ドイツ語',
         'フランス語',
         '中国語',
         'スペイン語',
         '情報',
         '身体運動・健康科学実習',
         '社会科学',
         '人文科学',
         '方法基礎',
         '基礎実験',
         '数理科学',
         '物質科学',
         '生命科学'],
        ['科学史',
         '表象文化論'],
        ['日本語上級']
    ]

    category = models.CharField('カテゴリ', max_length=255, default="未選択")

    subject = models.CharField('科目名', max_length=3,
                               choices=SUBJECT_CHOICES,
                               default="未選択")

    class_name = models.CharField('授業名', max_length=255, default="未選択")
    teacher = models.CharField('担当教員名', max_length=255, default="未選択")

    def __str__(self):
        return self.name


class Comments(models.Model):
    """コメント一覧"""
    file = models.ForeignKey(File, verbose_name='コメント', related_name='comments')
    author = models.ForeignKey(User, null=True)
    comments = models.TextField('コメント', blank=True)

    def __str__(self):
        return self.comments


class Reply(models.Model):
    """コメント"""
    comments = models.ForeignKey(Comments, verbose_name='リプライ', related_name='reply')
    author = models.ForeignKey(User)
    reply = models.TextField('リプライ', blank=True)

    def __str__(self):
        return self.reply
