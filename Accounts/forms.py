from django import forms
from .models import SOA


class SOAForm(forms.ModelForm):   
    class Meta:
        model = SOA

        fields = ['id','Branch','WES_REF_NO','PONo','POIssuedby', 'ClientName','ClientGroup','Shipname', 'POAmount', 'InvoiceNo', 'InvoiceDate', 'Duedate','Freight', 'Invoiceamount', 'SgdValue', 'GstScope', 'currency1', 'Invamtcreditnote', 'standardrated', 'GstPaid', 'paymentstatus', 'newstatus', 'transactioncode', 'areceiveddate', 'a2ndpaymentReceiveddate', 'receivedamount', 'receivedamountCurrency', 'dc', 'discountcurrency', 'Invcurrency', 'outstandingBalance', 'supt','Dispute','DisputeReason']
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['id']:
                field.required = False   