#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# # Web scrapping using python ( and Beautiful Soup) 

# In[79]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[80]:


from urllib.request import urlopen 
from bs4 import BeautifulSoup


# In[81]:


url="http://www.hubertiming.com/results/2017GPTR10K"
html= urlopen(url)


# In[82]:


soup= BeautifulSoup(html,'lxml')
type(soup)


# In[83]:


title =soup.title 
print (title)


# In[84]:


text=soup.get_text()
print(soup.text)


# In[85]:


soup.find_all('a')


# In[86]:


all_links=soup.find_all("a")
for link in all_links:
    print(link.get("href"))


# In[87]:


# printing the first 10 rows  for sanity  check
rows = soup.find_all('tr')
print(rows[:10])


# In[88]:


for row in rows :
    row_td = row.find_all('td')
print(row_td)
type(row_td)


# In[89]:


str_cells  = str(row_td)
cleantext = BeautifulSoup( str_cells, "lxml").get_text()
print(cleantext)


# In[100]:


import re
list_rows =[]
for row in rows:
    cells = row.find_all('td')
    str_cells =str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean,' ', str_cells))
    list_rows.append(clean2)
print(clean2)
type(clean2)


# In[101]:


df=pd.DataFrame(list_rows)
df.head(10)


# In[115]:


df1 =df[0].str.split(',',expand=True)
df1.head(10)


# In[116]:


df1[0]=df1[0].str.strip('[')
df1.head(10)


# In[118]:


col_labels = soup.find_all('th')
print(col_labels)


# In[120]:


all_header =[]
col_str = str(col_labels)
cleantext2 =BeautifulSoup(col_str ,"lxml").get_text()
all_header.append(cleantext2)
print(all_header)


# In[121]:


df2=pd.DataFrame(all_header)
df2.head()


# In[122]:


df3 =df2[0].str.split(',' ,expand=True )
df3.head()


# In[123]:


frames=[df3,df1]
df4=pd.concat(frames)
df4.head(10)


# In[124]:


df5=df4.rename(columns=df4.iloc[0])
df5.head()


# In[125]:


df5.info()


# In[126]:


df5.shape


# In[128]:


df6=df5.dropna(axis=0 ,how='any')


# In[130]:


df7=df6.drop(df6.index[0])
df7.head()


# In[134]:


df7.rename(columns={'[Place':'place'},inplace=True )

df7.head()


# In[136]:


df7.rename(columns={' Team]': 'Team'},inplace=True)
df7


# In[139]:


df7[' Name']=df7[' Name'].str.replace('\r\n\r\n','')


# In[147]:


df7['Team']=df7['Team'].str.replace('\n \r\n','')


# In[149]:


df7['Team']=df7['Team'].str.replace('\r\n','')

df7.head()


# In[150]:


df7['Team'] =df7['Team'].str.strip(']')
df7.head()


# In[173]:


time_list =df7[' Time'].tolist()
time_mins = []
for i in time_list:
    parts = i.split(':')
    if len(parts) == 3:
        h, m, s = parts
        math = (int(h)*3600 + int(m)*60 + int(s))/60
    elif len(parts) == 2:
        m, s = parts
        math = (int(m)*60 + int(s))/60
    else:
        print(f"Unexpected time format: {i}")
        continue
    time_mins.append(math)



# In[187]:


import pandas as pd

# Assuming 'array' is your array
series = pd.Series(time_mins)
counts = series.value_counts()
print(counts)


# In[174]:


df7.head(10)


# In[180]:


top_null_time_rows = df7[df7[' Time'].isnull()].head(5)
top_null_time_rows[' Time']



# In[176]:


df7[' Time']


# In[177]:


col_labels = soup.find_all('th')


# In[181]:


all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
print(all_header)


# In[182]:


df2 = pd.DataFrame(all_header)
df2.head()


# In[185]:


df7[' Time'].value_counts()


# In[188]:


df7['Runner_mins'] = time_mins
df7.head()



# In[189]:


df7.describe(include=[np.number])


# In[191]:


from pylab import rcParams
rcParams['figure.figsize'] =15,5


# In[198]:


df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])


# In[199]:


x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()



# In[204]:


df7.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[225]:


f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
print(f_fuko)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[241]:


g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)


# In[ ]:





# In[250]:


data = np.random.randn(1000)
 
# Plotting a basic histogram
plt.hist(df7['Runner_mins'], bins=30, color='skyblue', edgecolor='black')
 
# Adding labels and title
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Basic Histogram')
 
# Display the plot
plt.show()


# In[ ]:





# In[252]:


x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})
plt.show()


# In[257]:


f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']==' M']['Runner_mins']
sns.barplot(f_fuko, kde=True,  edgecolor= 'black', label='Female')
sns.barplot(m_fuko, kde=True,  edgecolor= 'black', label='Male')
plt.legend()


# In[258]:


df7.boxplot(column='Runner_mins', by=' Gender')
plt.ylabel('Chip Time')
plt.suptitle("")


# In[ ]:




