
# coding: utf-8

# In[143]:


class Income:
    
    def __init__(self,fullName,pan,annualCtc):
        self.fullName = fullName
        self.pan = pan
        self.annualCtc = annualCtc
        self.basic = annualCtc * 0.4
        self.hra = annualCtc * 0.3
        self.coveyanceAllowance = annualCtc * 0.02
        self.medicalAllowance = annualCtc * 0.02
        self.statutoryAllowance = annualCtc * 0.01
        self.otherAllowance = annualCtc * 0.25
        self.employeePf = self.basic * 0.12
        self.additionalIncome = 0
        self.interestEarned = 0
        self.tax_pct_additionalIncome = 10
        
    def updateAdditionalIncome(self,income):
        self.additionalIncome = self.additionalIncome + income
    
    def updateInterestEarned(self,interest):
        self.interestEarned = self.interestEarned + interest
        
        
        


# In[129]:


from enum import Enum

class Section(Enum):
    SECTION_80C = '80C'
    SECTION_80D = '80D'
    SECTION_80G = '80G'

class Section_Limit(Enum):
    SECTION_80C_ALL = 150000
    SECTION_80D_SELF = 25000
    SECTION_80D_PARENTAL = 50000


# In[130]:


class Deduction:
    
    def __init__(self,section,name,amount):
        self.section = section
        self.name = name
        self.amount = amount
            


# In[147]:


class IncomeTax:
          
    def __init__(self,fullName,pan,actualCtc):
        self.income = Income(fullName,pan,actualCtc)
        self.totalDeductionAmount = 0
        self.totalDeduction = {}
        self.totalTaxableIncome = 0
        self.totalTax = 0
        self.deductionList = []
    
    def updateAdditionalIncome(self,income):
        self.income.updateAdditionalIncome(income)
    
    def addDeduction(self,section,name,amount):
        self.deduction = Deduction(section,name,amount)
        self.deductionList.append(self.deduction)
    
    def calculateTotalDeductionAmount(self):
        self.calculateDeductionAmountBySection();
        
        for x in self.totalDeduction.items():
            if x[0] == Section.SECTION_80C.name :                
                self.totalDeductionAmount += Section_Limit.SECTION_80C_ALL.value if x[1] >= Section_Limit.SECTION_80C_ALL.value else x[1]
            elif x[0] == Section.SECTION_80D.name+"_SELF" :
                self.totalDeductionAmount += Section_Limit.SECTION_80D_SELF.value if x[1] >= Section_Limit.SECTION_80D_SELF.value else x[1]
            elif x[0] == Section.SECTION_80D.name+"_PARENTAL" :
                self.totalDeductionAmount += Section_Limit.SECTION_80D_PARENTAL.value if x[1] >= Section_Limit.SECTION_80D_PARENTAL.value else x[1]
            elif x[0] == Section.SECTION_80G.name:
                self.totalDeductionAmount += x[1]
                 
    def calculateDeductionAmountBySection(self):
        for x in self.deductionList:
            if x.section == Section.SECTION_80C.name :
                if x.section in self.totalDeduction.keys():
                    amount = x.amount + self.totalDeduction(x.section)
                    self.totalDeduction.update({x.section , amount})
                else:
                    self.totalDeduction[x.section]=x.amount
                    
            elif (x.section == Section.SECTION_80D.name) and (x.name.upper() == 'SELF'):
                key = x.section+'_'+x.name.upper()
                if key in self.totalDeduction.keys():
                    amount = x.amount + self.totalDeduction(key)
                    self.totalDeduction.update({key , amount})
                else:
                    self.totalDeduction[key]=x.amount
                    
            elif x.section == Section.SECTION_80D.name and x.name.upper() == 'PARENTAL':
                key = x.section+'_'+x.name.upper()
                if key in self.totalDeduction.keys():
                    amount = x.amount + self.totalDeduction(key)
                    self.totalDeduction.update({key , amount})
                else:
                    self.totalDeduction[key]=x.amount
                       
    def calculateTaxableIncome(self):
        self.totalTaxableIncome = (self.income.annualCtc + self.income.additionalIncome + self.income.interestEarned) - self.totalDeductionAmount
        
    def calculateHra(self):
        return 1
        
    def calculateTax(self):
        
        self.calculateTotalDeductionAmount()
        self.calculateTaxableIncome()
        print("Name ",self.income.fullName)
        print("PAN ",self.income.pan)
        print("Actual income ",(self.income.annualCtc + self.income.additionalIncome + self.income.interestEarned))
        print("Deductions ",self.totalDeduction)
        print("Total deduction amount",self.totalDeductionAmount)
        print("Total taxable Income ",self.totalTaxableIncome)
        
        #self.totalTaxableIncome = self.totalTaxableIncome - 40000
        
        amount_slab1 = 250000 if self.totalTaxableIncome >= 500000 else self.totalTaxableIncome 
        amount_slab2 = 500000 if self.totalTaxableIncome >= 1000000 else (self.totalTaxableIncome - 500000)
        amount_slab3 = (self.totalTaxableIncome - 1000000) if self.totalTaxableIncome >= 1000000 else 0        
              
        slab1_tax_amount = amount_slab1 * 0.05
        slab2_tax_amount = amount_slab2 * 0.2
        slab3_tax_amount = amount_slab3 * 0.3
        
        print("Slab 1 tax amount ",slab1_tax_amount)
        print("Slab 2 tax amount ",slab2_tax_amount)
        print("Slab 3 tax amount ",slab3_tax_amount)
        
        cess = (slab1_tax_amount+slab2_tax_amount+slab3_tax_amount) * 0.04
        print("CESS ",cess)
        
        self.totalTax = slab1_tax_amount + slab2_tax_amount + slab3_tax_amount + cess
        print("Total tax ",self.totalTax)
        return self.totalTax


# In[148]:


incometax = IncomeTax("Aditya","AXEPK3969K",700000)
incometax.addDeduction(Section.SECTION_80C.name,'PPF',180000)
incometax.addDeduction(Section.SECTION_80D.name,'SELF',5000)
incometax.addDeduction(Section.SECTION_80D.name,'PARENTAL',7000)

incometax.updateAdditionalIncome(6000)

incometax.calculateTax()

