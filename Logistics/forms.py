from django import forms
from .models import DHL,CommercialInvoice,DoDnNumber,CommercialPacl,DoNumber,Ordertracking

# from django.core.validators import RegexValidator
# from django.contrib.admin import widgets

class DHLForm(forms.ModelForm):   
    class Meta:
        model = DHL

        fields = ['id'	,'WES_Ref',	'PO_NO'	,'Client_Name'	,'Ship_name',	'Client_Invoice_No'	,'INVOICE_DATE',	'Client_Frieght_Cost'	,'Client_Freight_Currency'	,'Client_Freight_Cost_in_SGD'	,'DHL_Invoice_number'	,'AWB_NUMBER'	,'AMOUNT_INR'	,'DHL_AMOUNT_SGD',	'DHL_DUTY_TAX'	,'Invoice_date2',	'Due_Date'	,'Status',	'Paid_date',	'Transaction_number'	,'From_Country'	, 'To_Country',	'Weight_Kg','Dimension_Volume', 'Dimension_CM' ,'Profit_and_Loss'	,'Remarks']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['id']:
                field.required = False
                
class commercialinvoiceForm(forms.ModelForm):   
    class Meta:
        model = CommercialInvoice

        fields = ['ID','COMMERCIAL_NUMBER','PACKING_LIST_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE','Remarks']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False

class dodnnumberForm(forms.ModelForm):   
    class Meta:
        model = DoDnNumber

        fields = ['ID','DO_DN_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE','REMARK']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False

class commercialpaclForm(forms.ModelForm):   
    class Meta:
        model = CommercialPacl

        fields = ['ID','COMMERCIAL_NUMBER','PACL_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False


class donumberForm(forms.ModelForm):   
    class Meta:
        model = DoNumber

        fields = ['ID','DO_NUMBER','DATE','VESSEL_NAME','WES_NUMBER','PO_NUMBER','INCHARGE']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False



class OrdertrackingForm(forms.ModelForm):   
    class Meta:
        model = Ordertracking

        fields = ['ID','Branch','WES_NO','PO_NO','PO_Date', 'Client_Name','Vessel_Name','Supplier_Name','Forwarder_name','AWB_NO','Status','Status_Date','InCharger','Dolibar','Remarks']
 
    Branch = forms.CharField(required=False)
    WES_NO = forms.CharField(required=False)
    PO_NO = forms.CharField(required=False)
    PO_Date = forms.CharField(required=False)
    Client_Name = forms.CharField(required=False)
    Vessel_Name = forms.CharField(required=False)
    Supplier_Name = forms.CharField(required=False)
    Forwarder_name = forms.CharField(required=False)
    AWB_NO = forms.CharField(required=False)
    Status = forms.CharField(required=False)
    Status_Date = forms.CharField(required=False)
    InCharger = forms.CharField(required=False)
    Dolibar = forms.CharField(required=False)
    Remarks = forms.CharField(required=False)

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required=False      


