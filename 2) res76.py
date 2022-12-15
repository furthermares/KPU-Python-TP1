import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('president-1976-2016.csv')
df.drop(df.columns[[2,3,4,5,6,7,9,12,13]],axis=1,inplace=True)

D=pd.DataFrame(df.loc[df['party'] == 'democrat'])
R=pd.DataFrame(df.loc[df['party'] == 'republican'])
DR = pd.merge(D, R, how='outer', on=['year', 'state'])
DR.drop(DR.columns[[2,4,5]],axis=1,inplace=True)
DR.rename(columns={"candidatevotes_x": "Democrat",
                   "candidatevotes_y": "Republican",
                   "totalvotes_y":"total"},
          inplace=True)

DR.sort_values(by=['state','year'],inplace=True)
DR.set_index(['state','year'],inplace=True)

DR.dropna(inplace=True)
DR=DR.astype(int)

DR = DR[~DR.index.duplicated(keep='first')]

DR['D%']=100*DR.iloc[:,0]/DR.iloc[:,2]
DR['R%']=100*DR.iloc[:,1]/DR.iloc[:,2]
DR['D-R%']=DR.iloc[:,3]-DR.iloc[:,4]

def lookup(states):
    plt.figure()
    plt.title(states)
    sns.regplot(x=DR.loc[states].index,y=DR.loc[states]['D%']
                ).set(ylim=(0, 100), ylabel="")
    sns.regplot(x=DR.loc[states].index,y=DR.loc[states]['R%']
                ).set(ylim=(0, 100), ylabel="")

statelist=D['state'].unique()

def lookupALL():
    for st in statelist:
        lookup(st)
        #plt.savefig("2) "+st)