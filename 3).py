import pandas as pd
import csv
import matplotlib.pyplot as plt

#read country_facts.csv
cDR = pd.read_csv('country_facts.csv')
cDR = cDR[cDR.isnull().any(axis=1)]
cDR.drop(cDR.columns[[0,2]],axis=1,inplace=True)
cDR0 = cDR.iloc[0]
cDR.drop(0, inplace=True)
cDR.reset_index(drop=True,inplace=True)

#read country_facts_dictionary.csv
dict={}
for line in csv.reader(open('country_facts_dictionary.csv')):
    dict[line[0]]=line[1]

#checking p or np
#after np there are average values. we also don't count them as np
#cDR[1:].sum()/cDR0[1:]

dict_p=[]
dict_np=[]

DR_pcheck = cDR[1:].sum()/cDR0[1:]

for index,value in DR_pcheck.items():
    if 0.98 <= value <= 1.02:
        dict_p.append(index)
    else:
        dict_np.append(index)
dict_np.pop(-1)

#REDUNTANT pcheck
"""
for key,value in dict.items():
    if "percent" in value:
        dict_p.append(key)
    else:
        dict_np.append(key)  
        
dict_np.pop(0)
dict_np.remove('POP815213')
dict_np.remove('HSG445213')
"""

#get DR16
res16 = pd.read_csv('res16.csv',header=[0,1])
res16=res16.drop(57)
res16=res16.drop(columns=['Sources'])

res16.replace('–', 0, inplace=True)
for k in range(1,17,3):
   res16.iloc[:,k] = res16.iloc[:,k].str.replace(',', '')
   res16.iloc[:,k] = pd.to_numeric(res16.iloc[:,k], errors='coerce')
   res16.iloc[:,k+2] = pd.to_numeric(res16.iloc[:,k+2], errors='coerce')
res16.iloc[:,21] = res16.iloc[:,21].str.replace(',', '')
res16.iloc[:,21] = pd.to_numeric(res16.iloc[:,21])

DR16 = pd.DataFrame(res16.iloc[:, [0,1,4,21]])
DR16.columns=DR16.columns.droplevel(1)
DR16.drop([20,21,30,31,32], inplace=True)
DR16.reset_index(drop=True, inplace=True)

DR16['D%']=DR16.iloc[:,1]/DR16.iloc[:,3]
DR16['R%']=DR16.iloc[:,2]/DR16.iloc[:,3]
DR16['D-R%']=DR16.iloc[:,4]-DR16.iloc[:,5]

#cDR
cDR['DR']=DR16['D-R%']
cDR0['DR']=DR16.iloc[-1,-1]

#separate D and R
cDRs_listR = []
cDRs_listD = []
for index, row in cDR.iterrows():
    if row['DR']>0:
        cDRs_listD.append(row)
    else:
        cDRs_listR.append(row)
cDRsD=pd.DataFrame(cDRs_listD)
cDRsR=pd.DataFrame(cDRs_listR)

#categorizing data by D/R, p/np
cDRsDp=[]
cDRsDnp=[]
cDRsRp=[]
cDRsRnp=[]
for str in dict_p:
   cDRsDp.append(100*cDRsD[str].sum()/cDR0[str])
   cDRsRp.append(100*cDRsR[str].sum()/cDR0[str])
for str in dict_np:
   cDRsDnp.append(100*cDRsD[str].sum()/(cDR0[str]*cDR0.size))
   cDRsRnp.append(100*cDRsR[str].sum()/(cDR0[str]*cDR0.size))

#plt

plt.figure(0)
plt.axhline(50,color='gray',linestyle="-")
plt.title('Demographic split by political party leanings')
plt.xticks(rotation=90)
plt.bar(dict_p,cDRsDp)
plt.bar(dict_p,cDRsRp,bottom=cDRsDp)

plt.figure(1,figsize=(10,8))
plt.xticks(rotation=90)
plt.bar(dict_np,cDRsDnp)
plt.bar(dict_np,cDRsRnp,bottom=cDRsDnp)

#np discrepancy analysis
#for str in dict_np:
    #print(cDRsD[str].mean()-cDRsR[str].mean())

flag_log=False
def log_switch():
    global flag_log
    flag_log = not flag_log
   
colors=[]
def lookup(la):
    colors.clear()
    i=0
    dict_temp=dict
    plt.title(la, fontsize=14)
    plt.xticks(rotation=90)
    for str in dict:
        if(la in str):
            if(cDRsD[str].mean()>cDRsR[str].mean()):
                colors.append('b')
            else:
                colors.append('r')
    for str in dict_temp:
        if(la in str):
            plt.bar(str,cDRsD[str].mean()-cDRsR[str].mean(),
                    color=colors[i],log=flag_log)
            i+=1