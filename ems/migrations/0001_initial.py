# Generated by Django 2.1.1 on 2018-10-04 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=50, verbose_name='시리얼넘버')),
                ('purchase_date', models.DateField(null=True, verbose_name='구입일자')),
                ('price', models.IntegerField(verbose_name='구입가격')),
                ('status', models.SmallIntegerField(choices=[(0, '사용 가능'), (20, '사용 중'), (10, '사용 승인 대기 중'), (11, '반납 승인 대기 중')], default=0, verbose_name='상태')),
                ('management_number', models.CharField(max_length=50, verbose_name='관리번호')),
                ('accessibility', models.CharField(choices=[(0, '개인용'), (1, '공용')], default=0, max_length=50, verbose_name='용도')),
                ('manufacturer', models.CharField(max_length=50, verbose_name='제조사')),
                ('model', models.CharField(max_length=50, verbose_name='모델')),
                ('purpose', models.TextField(verbose_name='사용용도')),
                ('check_in_duedate', models.DateField(null=True, verbose_name='반납예정일')),
                ('buying_shop', models.CharField(blank=True, max_length=50, null=True, verbose_name='구입처')),
                ('document', models.CharField(max_length=100, verbose_name='관련문서')),
                ('current_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_user', to=settings.AUTH_USER_MODEL, verbose_name='현재 사용자')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_out_date', models.DateField(null=True, verbose_name='반출일자')),
                ('purpose', models.CharField(max_length=50, null=True, verbose_name='용도')),
                ('check_in_duedate', models.DateField(null=True, verbose_name='반납예정일')),
                ('manager_confirm', models.CharField(max_length=20, null=True, verbose_name='반출자확인')),
                ('check_in_confirm', models.CharField(max_length=20, null=True, verbose_name='반납확인')),
                ('note', models.TextField(null=True, verbose_name='비고')),
                ('count', models.SmallIntegerField(null=True, verbose_name='Count')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ems.Equipment')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentRepairHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='일자')),
                ('reason', models.TextField(verbose_name='고장사유및내역')),
                ('result', models.CharField(max_length=100, verbose_name='처리결과')),
                ('cost', models.IntegerField(verbose_name='비용')),
                ('reference', models.CharField(blank=True, max_length=50, null=True, verbose_name='관련근거')),
                ('count', models.SmallIntegerField(verbose_name='Count')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ems.Equipment')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='담당자')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu', models.CharField(blank=True, max_length=50, null=True, verbose_name='CPU')),
                ('mem', models.CharField(blank=True, max_length=50, null=True, verbose_name='메모리')),
                ('hdd', models.CharField(blank=True, max_length=50, null=True, verbose_name='HDD')),
                ('nic', models.CharField(blank=True, max_length=50, null=True, verbose_name='네트워크')),
                ('graphic', models.CharField(blank=True, max_length=50, null=True, verbose_name='Graphic')),
                ('etc', models.CharField(blank=True, max_length=50, null=True, verbose_name='기타')),
                ('text', models.CharField(blank=True, max_length=50, null=True, verbose_name='텍스트')),
                ('change_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='변경날짜')),
                ('change_reason', models.CharField(blank=True, max_length=50, null=True, verbose_name='변경사유및내역')),
                ('cost', models.IntegerField(verbose_name='소요비용')),
                ('reference', models.CharField(blank=True, max_length=50, null=True, verbose_name='관련근거')),
                ('count', models.SmallIntegerField(verbose_name='Count')),
                ('change_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='change_user', to=settings.AUTH_USER_MODEL, verbose_name='담당')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ems.Equipment')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RepairStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='equipmenttype',
            unique_together={('id', 'label')},
        ),
        migrations.AddField(
            model_name='equipment',
            name='kind',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ems.EquipmentType', verbose_name='종류'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='purchase_manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_manager', to=settings.AUTH_USER_MODEL, verbose_name='구매담당자'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='purchase_request_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_request_user', to=settings.AUTH_USER_MODEL, verbose_name='구입요청자'),
        ),
        migrations.AlterUniqueTogether(
            name='equipment',
            unique_together={('serial_number', 'management_number')},
        ),
    ]
