#!/usr/bin/env python
# coding: utf-8

# ## Упражнения по библиотеке Numpy

# In[2]:


import numpy as np


# **1.** Дан случайный массив, поменять знак у элементов, значения которых между 3 и 8

# In[6]:


arr = np.random.randint(0,10, size=10)
arr[(arr >3) & (arr <8)] *=-1 # ]3,8[ 
arr


# **2.** Заменить максимальный элемент случайного массива на 0

# In[9]:


# your code
arr = np.random.randint(0,50, size=10)
arr[arr.argmax()] = 0
arr


# **3.** Построить прямое произведение массивов (все комбинации с каждым элементом). На вход подается двумерный массив

# In[8]:


# your code
arr = np.array([[1,2],[3,4]])
print(arr.shape)
grid = np.array(np.meshgrid(*arr)).T.reshape(-1, arr.shape[0]) 
grid


# **4.** Даны 2 массива A (8x3) и B (2x2). Найти строки в A, которые содержат элементы из каждой строки в B, независимо от порядка элементов в B

# In[19]:


# your code
A= np.random.randint(1,10, size=(8,3))
B= np.random.randint(1,10, size=(2,2))

result = []
for row_a in A:
    for row_b in B:
        if all(elem in row_a for elem in row_b):
            result.append(row_a)
            break

result


# **5.** Дана 10x3 матрица, найти строки из неравных значений (например строка [2,2,3] остается, строка [3,3,3] удаляется)

# In[29]:


# your code
arr = np.random.randint(1,5,size=(10,3))

result =[]
for row in arr:
    if row[0] == row[1] ==row[2]:
        continue
    result .append(row)
result = np.array(result)
result


# Using Mask
mask= (arr[:,0] == arr[:,1]) & (arr[:,1]== arr[:,2])

fil_arr= arr[~mask]
print(f"result:\n{result}\nfilterd array by mask:\n{fil_arr}")



# **6.** Дан двумерный массив. Удалить те строки, которые повторяются

# In[36]:


# your code
arr = np.array([[1,2],[2,5],[1,2],[2,1]])
unique_arr = np.unique(arr,axis=0)
unique_arr


# ______
# ______

# Для каждой из следующих задач (1-5) нужно привести 2 реализации – одна без использования numpy (cчитайте, что там, где на входе или выходе должны быть numpy array, будут просто списки), а вторая полностью векторизованная с использованием numpy (без использования питоновских циклов/map/list comprehension).
# 
# 
# __Замечание 1.__ Можно считать, что все указанные объекты непустые (к примеру, в __задаче 1__ на диагонали матрицы есть ненулевые элементы).
# 
# __Замечание 2.__ Для большинства задач решение занимает не больше 1-2 строк.

# ___

# * __Задача 1__: Подсчитать произведение ненулевых элементов на диагонали прямоугольной матрицы.  
#  Например, для X = np.array([[1, 0, 1], [2, 0, 2], [3, 0, 3], [4, 4, 4]]) ответ 3.

# In[41]:


# your code
X = np.array([[1, 0, 1],
              [2, 0, 2],
              [3, 0, 3],
              [4, 4, 4]]) 
p=1
for i in range(min(X.shape)):
    if X[i,i] !=0:
        p *=X[i,i]

# Numpy
res = np.prod(np.diag(X)[np.diag(X)!=0])

print(f"Pythonic : {p}\nNumpy : {res}")


# * __Задача 2__: Даны два вектора x и y. Проверить, задают ли они одно и то же мультимножество.  
#   Например, для x = np.array([1, 2, 2, 4]), y = np.array([4, 2, 1, 2]) ответ True.

# In[52]:


# your code
x = np.array([1, 2, 2, 4])
y = np.array([4, 2, 1, 2])

# Pythonic
def check_arrs(x:np.array,y:np.array):
    if len(x) == len(y):
        return sorted(x) == sorted(y)
    return False

# Numpy
is_same_multiset = np.array_equal(np.sort(x), np.sort(y))

print(f"Pythonic: {check_arrs(x,y)}\nNumpy: {is_same_multiset}")
    


# * __Задача 3__: Найти максимальный элемент в векторе x среди элементов, перед которыми стоит ноль. 
#  Например, для x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0]) ответ 5.

# In[60]:


# your code
x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0])

vals = [value for i,value in enumerate(x) if i>0 and x[i-1] == 0 and value !=0]
max_value = max(vals)

# Numpy
condidates = x[1:][x[:-1] ==0] 
res = condidates.max()

print(f"Python: {max_value},\nNumPy: {res}")


# * __Задача 4__: Реализовать кодирование длин серий (Run-length encoding). Для некоторого вектора x необходимо вернуть кортеж из двух векторов одинаковой длины. Первый содержит числа, а второй - сколько раз их нужно повторить.  
#  Например, для x = np.array([2, 2, 2, 3, 3, 3, 5]) ответ (np.array([2, 3, 5]), np.array([3, 3, 1])).

# In[65]:


# your code
x = np.array([2, 2, 2, 3, 3, 3, 5])
def run_length_encode(x):
    values = []
    counts = []
    current = x[0]
    count = 1
    for value in x[1:]:
        if value == current:
            count += 1
        else:
            values.append(current)
            counts.append(count)
            current = value
            count = 1
    values.append(current)
    counts.append(count)

    return (np.array(values), np.array(counts))


# Numpy
def rle_numpy(x):     
    boundaries = x[1:] != x[:-1]
    values = x[np.concatenate(([True], boundaries))]
    ids = np.flatnonzero(np.concatenate(([True], boundaries, [True])) )  #[T, F, ,F, T, F, F, T, T] ==> [0,3,6,7]
    counts = np.diff(ids)
    return (values, counts)

print(f"Python {run_length_encode(x)},\nNumpy: {rle_numpy(x)}")


# * __Задача 5__: Даны две выборки объектов - X и Y. Вычислить матрицу евклидовых расстояний между объектами. Сравните с функцией scipy.spatial.distance.cdist по скорости работы.

# In[15]:


# your code
import math
import time
from scipy.spatial.distance import cdist

def caluc_euclidean_distance(x, y):
    return math.sqrt(sum((a - b)**2 for a, b in zip(x, y)))

def distance_matrix(X, Y):
    n = len(X)
    m = len(Y)
    D = [[0.0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            D[i][j] = caluc_euclidean_distance(X[i], Y[j])
    return D

def euclidean_distance(X, Y):
    diff = X[:, None, :] - Y[None, :, :]
    return np.sqrt(np.sum(diff**2, axis=2))

# generate random data
X = np.random.rand(100, 50)
Y = np.random.rand(100, 50)

# measure pure python
start = time.time()
D_python = distance_matrix(X, Y)
t_python = time.time() - start

# measure scipy
start = time.time()
D_scipy = cdist(X, Y)
t_scipy = time.time() - start

# measure numpy
start_np = time.time()
D_numpy = euclidean_distance(X, Y)
t_numpy = time.time() - start_np

print(f"Python time: {t_python}")
print(f"SciPy time: {t_scipy}")
print(f"Numpy time: {t_numpy}")



# _______
# ________

# * #### __Задача 6__: CrunchieMunchies __*__
# 
# Вы работаете в отделе маркетинга пищевой компании MyCrunch, которая разрабатывает новый вид вкусных, полезных злаков под названием **CrunchieMunchies**.
# 
# Вы хотите продемонстрировать потребителям, насколько полезны ваши хлопья по сравнению с другими ведущими брендами, поэтому вы собрали данные о питании нескольких разных конкурентов.
# 
# Ваша задача - использовать вычисления Numpy для анализа этих данных и доказать, что ваши **СrunchieMunchies** - самый здоровый выбор для потребителей.
# 

# In[16]:


import numpy as np


# 1. Просмотрите файл cereal.csv. Этот файл содержит количества калорий для различных марок хлопьев. Загрузите данные из файла и сохраните их как calorie_stats.

# In[17]:


calorie_stats = np.loadtxt("./data/cereal.csv", delimiter=",")
calorie_stats


# 2. В одной порции CrunchieMunchies содержится 60 калорий. Насколько выше среднее количество калорий у ваших конкурентов?
# 
# Сохраните ответ в переменной average_calories и распечатайте переменную в терминале

# In[19]:


# your code
average_calories = np.average(calorie_stats)
average_calories


# 3. Корректно ли среднее количество калорий отражает распределение набора данных? Давайте отсортируем данные и посмотрим.
# 
# Отсортируйте данные и сохраните результат в переменной calorie_stats_sorted. Распечатайте отсортированную информацию

# In[29]:


calorie_stats_sorted = np.sort(calorie_stats)
calorie_stats_sorted


# 4. Похоже, что большинство значений выше среднего. Давайте посмотрим, является ли медиана наиболее корректным показателем набора данных.
# 
# Вычислите медиану набора данных и сохраните свой ответ в median_calories. Выведите медиану, чтобы вы могли видеть, как она сравнивается со средним значением.

# In[21]:


# your code
median_calories = np.median(calorie_stats_sorted)
median_calories


# 5. В то время как медиана показывает, что по крайней мере половина наших значений составляет более 100 калорий, было бы более впечатляюще показать, что значительная часть конкурентов имеет более высокое количество калорий, чем CrunchieMunchies.
# 
# Рассчитайте различные процентили и распечатайте их, пока не найдете наименьший процентиль, превышающий 60 калорий. Сохраните это значение в переменной nth_percentile.

# In[31]:


# your code
percentiles = np.percentile(calorie_stats, np.arange(101))
nth_percentile = np.argmax(percentiles > 60)
nth_percentile


# 6. Хотя процентиль показывает нам, что у большинства конкурентов количество калорий намного выше, это неудобная концепция для использования в маркетинговых материалах.
# 
# Вместо этого давайте подсчитаем процент хлопьев, в которых содержится более 60 калорий на порцию. Сохраните свой ответ в переменной more_calories и распечатайте его

# In[32]:


# your code
more_calories = np.mean(calorie_stats_sorted > 60) * 100
more_calories


# 7. Это действительно высокий процент. Это будет очень полезно, когда мы будем продвигать CrunchieMunchies. Но один вопрос заключается в том, насколько велики различия в наборе данных? Можем ли мы сделать обобщение, что в большинстве злаков содержится около 100 калорий или разброс еще больше?
# 
# Рассчитайте величину отклонения, найдя стандартное отклонение, Сохраните свой ответ в calorie_std и распечатайте на терминале. Как мы можем включить эту ценность в наш анализ?

# In[33]:


# your code
calorie_std = np.std(calorie_stats_sorted,ddof=1)
calorie_std
# (107 - 60) / 19.5 = 2.4 std below the mean 


# 8. Напишите короткий абзац, в котором кратко изложите свои выводы и то, как, по вашему мнению, эти данные могут быть использованы в интересах Mycrunch при маркетинге CrunchieMunchies.

# In[35]:


# your code
output = f'''
        Наш продукт CrunchieMunchies содержит 60 калорий, что меньше, чем у {more_calories}% конкурентов. 
        Среднее значение калорийности среди злаков составляет {average_calories}, 
        а стандартное отклонение равно {calorie_std}, что означает: большинство значений 
        лежат в диапазоне {average_calories} ± {calorie_std}. 
        Таким образом, 60 калорий — это заметно ниже типичного уровня на рынке.
'''
print(output)

