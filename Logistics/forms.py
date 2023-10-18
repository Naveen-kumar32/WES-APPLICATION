from django import forms
from .models import DHL,CommercialInvoice,DoDnNumber,WesNewSg,CommercialPacl,InvoiceNumber,DoNumber,Proforma


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

        fields = ['ID','DO_DN_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE','Remarks']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False

# class packinglistForm(forms.ModelForm):   
#     class Meta:
#         model = PackingList

#         fields = ['ID','PACKING_LIST_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE','REMARKS']
  


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             if field_name not in ['ID']:
#                 field.required = False     

class wesnewsgForm(forms.ModelForm):   
    class Meta:
        model = WesNewSg

        fields = ['ID','INVOICE_NUMBER','DATE','VESSEL_NAME','WES_NUMBER', 'PO_NUMBER','INCHARGE','INVOICE_TYPE','SIGNED_DN','Remarks']
  


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

class invoicenumberForm(forms.ModelForm):   
    class Meta:
        model = InvoiceNumber

        fields = ['ID','INVOICE_NUMBER','DATE','VESSEL_NAME','WES_NUMBER','PO_NUMBER','INCHARGE','REMARK']
  


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


class proformaForm(forms.ModelForm):   
    class Meta:
        model = Proforma

        fields = ['ID','PROFORMA_INVOICE_NUMBER','DATE','VESSEL_NAME','WES_NUMBER','PO_NUMBER','INCHARGE','STATUS','REMARK']
  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['ID']:
                field.required = False
