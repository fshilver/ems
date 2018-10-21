# Generated by Django 2.1.1 on 2018-10-21 09:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0005_equipmentapply_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentapply',
            name='apply_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='사용신청일'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmentapply',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '사용 신청 검토중'), (10, '사용 승인'), (20, '사용 거절'), (30, '사용 신청 취소')], default=0, verbose_name='상태'),
        ),
    ]