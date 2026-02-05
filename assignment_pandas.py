#!/usr/bin/env python
# coding: utf-8

# ## Датасет собран из базы данных переписи 1994 года и содержит данные о доходах.
# ### Информация о данных:
# * age: continuous.
# * workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
# * fnlwgt: continuous.
# * education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, * Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
# * education-num: continuous.
# * marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
# * occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
# * relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
# * race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
# * sex: Female, Male.
# * capital-gain: continuous.
# * capital-loss: continuous.
# * hours-per-week: continuous.
# * native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
# * salary: >50K,<=50K
# 
# ## Проведите анализ данных при помощи Pandas выполнив поставленные задачи.
# #### 

# In[1]:


import pandas as pd


# In[2]:


# загружаем датасет
df = pd.read_csv("./data/adult.data.csv")
df.head()


# **1. Посчитайте, сколько мужчин и женщин (признак *sex*) представлено в этом датасете**

# In[7]:


# your code
males = (df['sex']=='Male').sum()
females= (df['sex'] == 'Female').sum()

print(f"Males: {males}\nFemales: {females}")


# **2. Каков средний возраст мужчин (признак *age*) по всему датасету?**

# In[3]:


# your code
average_age_man = df[df["sex"] == 'Male']['age'].mean()
average_age_man


# **3. Какова доля граждан Соединенных Штатов (признак *native-country*)?**

# In[11]:


# your code
use_proportion = (df['native-country'] == 'United-States').mean()
use_proportion


# **4-5. Рассчитайте среднее значение и среднеквадратичное отклонение возраста тех, кто получает более 50K в год (признак *salary*) и тех, кто получает менее 50K в год**

# In[16]:


# your code
more_50_k = df[df['salary'] == '>50K']['age'].agg(['mean','std'])
less_or_eq_50_k = df[df['salary'] == '<=50K']['age'].agg(['mean', 'std'])
print(f"More then 50k: Age avarage is {more_50_k['mean']}, std is {more_50_k['std']}")
print(f"Less then or equal 50k: Age avarage is {less_or_eq_50_k['mean']}, std is {less_or_eq_50_k['std']}")


# **6. Правда ли, что люди, которые получают больше 50k, имеют минимум высшее образование? (признак *education – Bachelors, Prof-school, Assoc-acdm, Assoc-voc, Masters* или *Doctorate*)**

# In[7]:


df['education'].value_counts()


# In[9]:


# your code
indecator = (
    (df['salary'] == '>50K') &
    (df['education'].isin(educations))
).mean() / (df['salary'] == '>50K').mean()

if indecator == 1.0:
    print('Assumption is true')
else:
    print('Assumption is False')


# In[10]:


salary_mask = df['salary'] == '>50K'
if df.loc[salary_mask, 'education'].isin(educations).all():
    print('Assumption is true')
else:
    print('Assumption is False')


# **7. Выведите статистику возраста для каждой расы (признак *race*) и каждого пола. Используйте *groupby* и *describe*. Найдите таким образом максимальный возраст мужчин расы *Asian-Pac-Islander*.**

# In[12]:


# your code
static_age_by_race = df[['age', 'race']].groupby('race').describe()
static_age_by_sex = df[['age', 'sex']].groupby('sex').describe()

print(static_age_by_race)
print(static_age_by_sex)

max_age_men_asian = df.loc[ (df['sex'] == 'Male') & (df['race'] == 'Asian-Pac-Islander'), 'age' ].max()

print(f"максимальный возраст мужчин расы Asian-Pac-Islander : {max_age_men_asian}")


# **8. Среди кого больше доля зарабатывающих много (>50K): среди женатых или холостых мужчин (признак *marital-status*)? Женатыми считаем тех, у кого *marital-status* начинается с *Married* (Married-civ-spouse, Married-spouse-absent или Married-AF-spouse), остальных считаем холостыми.**

# In[16]:


# your code
married_status =['Married-civ-spouse', 'Married-spouse-absent' ,'Married-AF-spouse']
df_men = df[df['sex'] == 'Male'].copy()
p_married = ((df_men['marital-status'].isin(married_status)) & (df_men['salary'] == '>50K')).mean()
p_unmarried = ((~df_men['marital-status'].isin(married_status)) & (df_men['salary'] == '>50K')).mean()

indecator = p_married/p_unmarried
print(indecator) # if indecator > 1 means the married poeple is more then unmarried

# Other way my adding new column and group by it

df_men['is_married'] = df_men['marital-status'].isin(married_status)

result = df_men.groupby('is_married')['salary'].apply(lambda s: (s == '>50K').mean())
result


# **9. Какое максимальное число часов человек работает в неделю (признак *hours-per-week*)? Сколько людей работают такое количество часов и каков среди них процент зарабатывающих много?**

# In[43]:


# your code

max_hours_per_week = df['hours-per-week'].max()
workers = df.loc[df['hours-per-week'] == max_hours_per_week]
count_workers = workers.shape[0]
percent_high_income = (workers['salary'] == '>50K').mean()

print(f"Max hours per week workers spend at work :{max_hours_per_week}, they are {count_workers} wroker and the prec ")


# **10. Посчитайте среднее время работы (*hours-per-week*) зарабатывающих мало и много (*salary*) для каждой страны (*native-country*).**

# In[9]:


# your code
df.groupby(['native-country', 'salary'])['hours-per-week'].mean()


# **11.Сгруппируйте людей по возрастным группам *young*, *adult*, *retiree*, где:**
# * *young* соответствует 16-35 лет
# * *adult* - 35-70 лет
# * *retiree* - 70-100 лет
# 
# **Проставьте название соответсвтуещей группы для каждого человека в новой колонке AgeGroup**

# In[11]:


# your code
import numpy as np

conditions = [
    df['age'].between(16,35,inclusive='left'),
    df['age'].between(35,70, inclusive='left'),
    df['age'].between(70,100, inclusive='both')
]
choices = ['young', 'adult', 'retiree']

df['AgeGroup'] = np.select(conditions, choices, default='unknown')

df[['age', 'AgeGroup']]


# **12-13. Определите количество зарабатывающих >50K в каждой из возрастных групп (колонка AgeGroup), а также выведите название возрастной группы, в которой чаще зарабатывают больше 50К (>50K)**

# In[17]:


# your code
counts = df.loc[df['salary'] == '>50K'].groupby('AgeGroup').size()
print(counts)
counts.idxmax()


# **14. Сгруппируйте людей по типу занятости (колонка occupation) и определите количество людей в каждой группе. После чего напишите функциюю фильтрации filter_func, которая будет возвращать только те группы, в которых средний возраст (колонка age) не больше 40 и в которых все работники отрабатывают более 5 часов в неделю (колонка hours-per-week)**

# In[17]:


# your code
groups_size = df.groupby('occupation').size()

def filter_func(group):
    return ( group['age'].mean() <= 40) and (group['hours-per-week'].min() >5 )

filterd_group = df.groupby('occupation').filter(filter_func)

print(groups_size)
print(filterd_group)


# In[ ]:




