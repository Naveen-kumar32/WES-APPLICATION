from django.db import models


class DHL(models.Model):
  
  id = models.IntegerField(primary_key=True)
  WES_Ref = models.CharField(max_length=100)
  PO_NO = models.CharField(max_length=100)
  Client_Name = models.CharField(max_length=100)
  Ship_name = models.CharField(max_length=100)
  Client_Invoice_No = models.CharField(max_length=100)
  INVOICE_DATE = models.CharField(max_length=100)
  Client_Frieght_Cost = models.CharField(max_length=100)
  Client_Freight_Currency = models.CharField(max_length=100)
  Client_Freight_Cost_in_SGD = models.CharField(max_length=100)
  DHL_Invoice_number = models.CharField(max_length=100)
  AWB_NUMBER = models.CharField(max_length=100)
  AMOUNT_INR = models.CharField(max_length=100)
  DHL_AMOUNT_SGD = models.CharField(max_length=100)
  DHL_DUTY_TAX = models.CharField(max_length=100)
  Invoice_date2 = models.CharField(max_length=100)
  Due_Date = models.CharField(max_length=100)
  Status = models.CharField(max_length=100)
  Paid_date = models.CharField(max_length=100)
  Transaction_number = models.CharField(max_length=100)
  From_Country = models.CharField(max_length=100)
  To_Country = models.CharField(max_length=100)
  Weight_Kg = models.CharField(max_length=100)
  Dimension_Volume = models.CharField(max_length=100)
  Dimension_CM = models.CharField(max_length=100)
  Profit_and_Loss = models.CharField(max_length=100)
  Remarks = models.CharField(max_length=100)
  
    
  def __str__(self):
        return str(self.id)
  class Meta:
        managed = True
        db_table = 'dhl'  

class CommercialInvoice(models.Model):
  
  ID = models.IntegerField(primary_key=True)
  COMMERCIAL_NUMBER = models.CharField(max_length=100)
  PACKING_LIST_NUMBER = models.CharField(max_length=100)
  DATE = models.CharField(max_length=100)
  VESSEL_NAME = models.CharField(max_length=100)
  WES_NUMBER = models.CharField(max_length=100)
  PO_NUMBER = models.CharField(max_length=100)
  INCHARGE = models.CharField(max_length=100)
  Remarks = models.CharField(max_length=100)
  
    
  def __str__(self):
        return str(self.ID)
  class Meta:
        managed = True
        db_table = 'commercial_invoice'

class DoDnNumber(models.Model):
  
  ID = models.IntegerField(primary_key=True)
  DO_DN_NUMBER = models.CharField(max_length=100)
  DATE = models.CharField(max_length=100)
  VESSEL_NAME = models.CharField(max_length=100)
  WES_NUMBER = models.CharField(max_length=100)
  PO_NUMBER = models.CharField(max_length=100)
  INCHARGE = models.CharField(max_length=100)
  REMARK = models.CharField(max_length=100)
  
    
  def __str__(self):
        return str(self.id)
  class Meta:
        managed = True
        db_table = 'do_dn_number'  

class CommercialPacl(models.Model):
  
  ID = models.IntegerField(primary_key=True)
  COMMERCIAL_NUMBER = models.CharField(max_length=100)
  PACL_NUMBER = models.CharField(max_length=100)
  DATE = models.CharField(max_length=100)
  VESSEL_NAME = models.CharField(max_length=100)
  WES_NUMBER = models.CharField(max_length=100)
  PO_NUMBER = models.CharField(max_length=100)
  INCHARGE = models.CharField(max_length=100)
  
    
  def __str__(self):
        return str(self.ID)
  class Meta:
        managed = True
        db_table = 'commercial_pacl'        

class DoNumber(models.Model):
  
  ID = models.IntegerField(primary_key=True)
  DO_NUMBER = models.CharField(max_length=100)
  DATE = models.CharField(max_length=100)
  VESSEL_NAME = models.CharField(max_length=100)
  WES_NUMBER = models.CharField(max_length=100)
  PO_NUMBER = models.CharField(max_length=100)
  INCHARGE = models.CharField(max_length=100)

  
    
  def __str__(self):
        return str(self.ID)
  class Meta:
        managed = True
        db_table = 'do_number'                

class Ordertracking(models.Model):
  
  ID = models.IntegerField(primary_key=True)
  Branch = models.CharField(max_length=100)
  WES_NO = models.CharField(max_length=100)
  PO_NO = models.CharField(max_length=100)
  PO_Date = models.CharField(max_length=100)
  Client_Name = models.CharField(max_length=100)
  Vessel_Name = models.CharField(max_length=100)
  Supplier_Name = models.CharField(max_length=100)
  Forwarder_name = models.CharField(max_length=100)
  AWB_NO = models.CharField(max_length=100)
  Status = models.CharField(max_length=100)
  Status_Date = models.CharField(max_length=100)
  InCharger = models.CharField(max_length=100)
  Dolibar = models.CharField(max_length=100)
  Remarks = models.CharField(max_length=100)
  
    
  def _str_(self):
        return str(self.ID)
  class Meta:
        managed = True
        db_table = 'order_tracking'      
