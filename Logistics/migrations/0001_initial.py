# Generated by Django 4.2.2 on 2023-10-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DHL',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('WES_Ref', models.CharField(max_length=100)),
                ('PO_NO', models.CharField(max_length=100)),
                ('Client_Name', models.CharField(max_length=100)),
                ('Ship_name', models.CharField(max_length=100)),
                ('Client_Invoice_No', models.CharField(max_length=100)),
                ('INVOICE_DATE', models.CharField(max_length=100)),
                ('Client_Frieght_Cost', models.CharField(max_length=100)),
                ('Client_Freight_Currency', models.CharField(max_length=100)),
                ('Client_Freight_Cost_in_SGD', models.CharField(max_length=100)),
                ('DHL_Invoice_number', models.CharField(max_length=100)),
                ('AWB_NUMBER', models.CharField(max_length=100)),
                ('AMOUNT_INR', models.CharField(max_length=100)),
                ('DHL_AMOUNT_SGD', models.CharField(max_length=100)),
                ('DHL_DUTY_TAX', models.CharField(max_length=100)),
                ('Invoice_date2', models.CharField(max_length=100)),
                ('Due_Date', models.CharField(max_length=100)),
                ('Status', models.CharField(max_length=100)),
                ('Paid_date', models.CharField(max_length=100)),
                ('Transaction_number', models.CharField(max_length=100)),
                ('From_Country', models.CharField(max_length=100)),
                ('To_Country', models.CharField(max_length=100)),
                ('Weight_Kg', models.CharField(max_length=100)),
                ('Dimension_Volume', models.CharField(max_length=100)),
                ('Dimension_CM', models.CharField(max_length=100)),
                ('Profit_and_Loss', models.CharField(max_length=100)),
                ('Remarks', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'dhl',
                'managed': True,
            },
        ),
    ]
