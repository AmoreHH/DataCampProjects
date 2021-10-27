#!/usr/bin/env python
# coding: utf-8

# ## Project Description
# The Nobel Prize is perhaps the world's most well known scientific award. Every year it is given to scientists and scholars in chemistry, literature, physics, medicine, economics, and peace. The first Nobel Prize was handed out in 1901, and at that time the prize was Eurocentric and male-focused, but nowadays it's not biased in any way. Surely, right?
# 
# Well, let's find out! What characteristics do the prize winners have? Which country gets it most often? And has anybody gotten it twice? It's up to you to figure this out.
# 
# The dataset used in this project is from The Nobel Foundation on Kaggle.
# 
# ## Guided Project
# In this project, you will use your data manipulation and visualization skills to explore patterns and trends over 100 years worth of Nobel Prize winners.
# 
# ### This project comes from Datacamp Guide and only for practice 
# https://app.datacamp.com/learn/projects/nobel-winners/guided/Python
# 
# ### 說明：
# 資料來源為kaggle而解題步驟則是參考DataCamp的Project, 因為資料集有一些不同，所以做了一些調整以符合資料集需求。  

# In[51]:


# Import libraries
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# # 1. Import Dataset from Kaggle
# 
# https://www.kaggle.com/nobelfoundation/nobel-laureates

# In[52]:


nobel = pd.read_csv('nobel.csv')
nobel.head(6)


# ## 2. Who gets the Nobel Prize?

# In[53]:


# Display the number of (possibly shared) Nobel Prizes handed out between 1901 and 2016
display(len(nobel.Prize))

# Display the number of prizes won by male and female recipients.
display(nobel['Sex'].value_counts())

# Display the number of prizes won by the top 10 nationalities.
nobel['Birth Country'].value_counts().head(10)


# ## 3. USA dominance? 

# In[54]:


# Calculating the proportion of USA born winners per decade
nobel['usa_born_winner'] = np.where(nobel['Birth Country']=="United States of America", True, False)

nobel['decade'] = (np.floor(nobel['Year']/10)*10).astype('int64')

prop_usa_winners = nobel.groupby('decade', as_index=False)['usa_born_winner'].mean() 

# Display the proportions of USA born winners per decade
display(prop_usa_winners)


# ## 4. Visualized USA dominance 

# In[55]:


# Setting the plotting theme
sns.set()

# setting the size of all plots.
plt.rcParams['figure.figsize'] = [11, 7]

# Plotting USA born winners 
ax = sns.lineplot(data=prop_usa_winners, x='decade', y='usa_born_winner')


# Adding %-formatting to the y-axis
from matplotlib.ticker import PercentFormatter
ax.yaxis.set_major_formatter(PercentFormatter())


# ## 5. What is the gender of a typical Nobel Prize winner?

# In[56]:


# Calculating the proportion of female laureates per decade
nobel['female_winner']= np.where(nobel['Sex']=="Female", True, False)
prop_female_winners =nobel.groupby(['decade','Category'], as_index=False)['female_winner'].mean() 

# Plotting USA born winners with % winners on the y-axis
ax=sns.lineplot(data=prop_female_winners, x='decade', y='female_winner', hue='Category')

ax.yaxis.set_major_formatter(PercentFormatter())


# ## 6. The first woman to win the Nobel Prize

# In[57]:


# Picking out the first woman to win a Nobel Prize
nobel_woman=nobel[nobel.Sex == 'Female'].nsmallest(1, 'Year')
nobel_woman


# ## 7. Repeat laureates
# 
# 找出哪些學者得過不只一次諾貝爾獎
# 

# In[58]:


# Selecting the laureates that have received 2 or more prizes.
nobel.groupby('Full Name').filter(lambda x: len(x) >1)


# ## 8. How old are you when you get the prize?

# In[86]:


# Converting birth_date from String to datetime
nobel['birth_year'] = nobel['Birth Date'].str[0:4].apply(pd.to_numeric)


# 這個資料檔如果單純的使用 nobel['birth_date'] = pd.to_datetime(nobel['Birth Date']) 的話，
# 會一直報錯：ParserError: month must be in 1..12: 1898-00-00
# 
# 考慮題目只是需要轉出birth_year, 所以用str截取前四個字，再轉為數字格式

# In[87]:


# Calculating the age of Nobel Prize winners
nobel['age'] = nobel['Year'] - nobel['birth_year']


# In[88]:


# Plotting the age of Nobel Prize winners
sns.lmplot(data=nobel, x='Year', y='age', lowess=True, aspect=2, line_kws={'color' : 'black'})


# ## 9. Age differences between prize categories

# In[89]:


# Same plot as above, but separate plots for each type of Nobel Prize
sns.lmplot(data=nobel, x='Year', y='age', row='Category', lowess=True, aspect=2, line_kws={'color' : 'black'})


# ## 10. Oldest and youngest winners
# 截至2016年為止，諾貝爾獎史上年紀最長與最年輕的得主的資訊

# In[119]:


# The oldest winner of a Nobel Prize as of 2016
print("The oldest winner of a Nobel Prize as of 2016")
display(nobel.nlargest(1, 'age'))
print('\n')
print("The youngest winner of a Nobel Prize as of 2016")
# The youngest winner of a Nobel Prize as of 2016
display(nobel.nsmallest(1, 'age'))


# ## 11. The youngest winners! 
# 截至2016年為止，諾貝爾獎史上最年輕的得主的名字

# In[120]:


# The name of the youngest winner of the Nobel Prize as of 2016
youngest_winner = nobel.nsmallest(1, 'age')
youngest_winner['Full Name'].apply(lambda x: x.split()[0])


# In[ ]:




