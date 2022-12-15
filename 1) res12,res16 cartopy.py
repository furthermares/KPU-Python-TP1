import pandas as pd
import matplotlib.pyplot as plt

#2012 United States presidential election votes Dataset
df = pd.read_html('https://en.wikipedia.org/wiki/2012_United_States_presidential_election#Results_by_state')
res12=pd.DataFrame(df[21])
res12.index_col=0
res12.replace('–', 0, inplace=True)
for k in range(1,14,3):
   res12.iloc[:,k] = pd.to_numeric(res12.iloc[:,k], errors='coerce')
   res12.iloc[:,k+2] = pd.to_numeric(res12.iloc[:,k+2], errors='coerce')
res12.iloc[:,0]=res12.iloc[:,0].str.replace('★','')
res12.iloc[30,0]=res12.iloc[30,0].replace('[115]','')
res12.iloc[32,0]=res12.iloc[32,0].replace('[116]','')
res12.iloc[35,0]=res12.iloc[35,0].replace('[117]','')
res12.iloc[49,0]=res12.iloc[49,0].replace('[118]','')
res12.rename(columns={res12.columns[0][0]:res12.columns[0][1]}, inplace=True)

#2016 United States presidential election votes Dataset
"""
ValueError: invalid literal for int() with base 10: '{{{vp_count}}}'
df = pd.read_html('https://en.wikipedia.org/wiki/2016_United_States_presidential_election#Results_by_state')
"""
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


#Votes between Barack Obama and Mitt Romney
DR12 = pd.DataFrame(res12.iloc[:, [0,1,4,18]])
DR12.columns=DR12.columns.droplevel(1)

DR12['D%']=DR12.iloc[:,1]/DR12.iloc[:,3]
DR12['R%']=DR12.iloc[:,2]/DR12.iloc[:,3]
DR12['D-R%']=DR12.iloc[:,4]-DR12.iloc[:,5]

#Votes between Donald Trump and Hilary Clinton
DR16 = pd.DataFrame(res16.iloc[:, [0,1,4,21]])
DR16.columns=DR16.columns.droplevel(1)
DR16.drop([20,21,30,31,32], inplace=True)
DR16.reset_index(drop=True, inplace=True)

DR16['D%']=DR16.iloc[:,1]/DR16.iloc[:,3]
DR16['R%']=DR16.iloc[:,2]/DR16.iloc[:,3]
DR16['D-R%']=DR16.iloc[:,4]-DR16.iloc[:,5]

#joining DR12,DR16
DR=pd.concat([DR12,DR16],axis=1)
DR['12-16 diff']=DR.iloc[:,6]-DR.iloc[:,13]

#conditional bar graph coloring
colors_DR12 = []
for index, row in DR12.iterrows():
    if row['D-R%']>0:
        colors_DR12.append('b')
    else:
        colors_DR12.append('r')
        
colors_DR16 = []
for index, row in DR16.iterrows():
    if row['D-R%'] > 0:
        colors_DR16.append('b')
    else:
        colors_DR16.append('r')
        
colors_DR=[]
for i in range(len(colors_DR12)):
    if colors_DR12[i] == colors_DR16[i]:
        colors_DR.append(colors_DR16[i])
    else:
        if colors_DR12[i] > colors_DR16[i]:
            colors_DR.append('c')
        else:
            colors_DR.append('m')

#plt
plt.figure(figsize=(10,10))
plt.suptitle("Political party votes in U.S. states in 2012, 2016",
             fontsize=16)

plt.subplot(3,1,1)
plt.xticks([])
plt.ylabel("2012")
plt.bar(DR12['State/District'],DR12['D-R%'], color=colors_DR12)

plt.subplot(3,1,2)
plt.xticks([])
plt.ylabel("2016")
plt.bar(DR12['State/District'],DR16['D-R%'], color=colors_DR16)

plt.subplot(3,1,3)
plt.xticks(rotation=90)
plt.ylabel("2012-2016")

plt.bar(DR['State/District'],DR['12-16 diff'], color=colors_DR)

#plt.savefig("1) res12,res16")