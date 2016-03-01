#encoding:utf8
import os
import sys
from django.db import models

# Create your models here.
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)

from config import tablename


class CacheTable(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    path = models.CharField(max_length=64, null=False, default="")
    info = models.TextField(null=True) # used to save request info
    data = models.TextField(null=False, blank=False) # used to save response valid data
    # resp.content['data'], not resp.content with type {"code": 0, 'msg': "", 'data': none}
    insert_time=models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        db_table = tablename

