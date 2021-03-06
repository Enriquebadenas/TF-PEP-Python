# -*- coding: utf-8 -*-
"""Trabajo2_EBC12_dic_23h.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HGkS7tEUm-ac2EuWDjoR-tunyivQV3g1

1. **Importación de librerias y del dataset.**
"""

import os
from google.colab import drive 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from pandas.api.types import CategoricalDtype
import scipy.stats as stats
import seaborn as sns

drive.mount('mydrive')

# df = pd.read_csv('/content/mydrive/MyDrive/TRABAJO 24 D EDEM/SydneyHousePrices.csv') #ruta malena
df = pd.read_csv('/content/mydrive/MyDrive/Colab Notebooks/SydneyHousePrices.csv', parse_dates=['Date'], index_col=['Date']) #ruta Enrique

"""Con lo que he añadido al final de la ruta de carga del fichero se arreglan la fechas pero estropeo los heatmap ¿? (EBC)"""

df

"""El dataset escogido trata sobre los precios de venta de las viviendas en Sydney. En este dataset hay tanto variables cualitatitivas como cuantitativas.

2. **Limpieza de la base de datos**

*Se va a proceder a realizar la limpieza de la base de datos mediante la sustitución de los valores faltantes por su media y la eliminación de aquellas filas con valores error. Como se puede observar a continuación, dicho proceso se ha de realizar únicamente con las variables BED, BATH y CAR.*
"""

df_mask=df['bed']>= 10
filtered_df = df[df_mask]
filtered_df

df_mask1=df['bath']>= 10
filtered_df1 = df[df_mask1]
filtered_df1

df_mask2=df['car']>= 10
filtered_df2 = df[df_mask2]
filtered_df2

df = df.drop(df[df['bed']>=10].index)
df = df.drop(df[df['bath']>=10].index)
df = df.drop(df[df['car']>=10].index)

df.isnull()
df.info(verbose=True,null_counts=True)
sns.heatmap(df.isnull(), cbar=False)

mean_car = df.car.mean()
df.car = df.car.fillna(mean_car)
mean_bed = df.bed.mean()
df.bed = df.bed.fillna(mean_bed)
sns.heatmap(df.isnull(), cbar=False)

"""Tras la realización de estos procesos obtenemos un dataset limpio. Esto nos permite ya comenzar con el análisis del dataset.

3. **Descripción de la target variable: SELLPRICE**

En este apartado se realiza un análisis de la variable target, SELLPRICE. Este análisis se realiza mediante su descripción gráfica.
Además con el fin de facilitar la realización de las hipótesis, se realiza la categorización de dicha variable.
"""

res = df.sellPrice.describe()
print (res)

m  = res[1]
sd = res[2]
n  = res[0]


df.loc[  (df['sellPrice']<1.197500e+06) ,"sellPrice_str"]= "Low price"
df.loc[ ((df['sellPrice']>= 1.197500e+06) & (df['sellPrice']<1.800000e+06)) ,"sellPrice_str"]= "Average price"
df.loc[  (df['sellPrice']>=1.800000e+06) ,"sellPrice_str"]= "High price"

my_categories=["Low price", "Average price", "High price"]
my_price_type = CategoricalDtype(categories=my_categories, ordered=True)
df["sellPrice_cat"] = df.sellPrice_str.astype(my_price_type)


mytable = pd.crosstab(df.sellPrice_cat, columns="count", normalize='columns')*100
print(mytable)
print (round(mytable,1))
plt.bar(mytable.index, mytable['count'], color="paleturquoise", edgecolor='black')
plt.xlabel('Price range')
plt.ylabel('Frequency')
plt.title('Figure 1. Sell price')
plt.show()

"""  4. **Descripción de las variables predictoras.**

"""

df.info()

"""Con el fin de realizar el análisis de las variables predictoras, se ha de conocer el tipo de variable que es cada una. El tipo de cada variable se muestra anteriormente.

Bed
"""

ef = df['bed'].describe() 
n = df.bed.count() 
m_bed= df.bed.mean()
sd_bed = df.bed.std()

x = df['bed']
plt.hist(x,edgecolor='black', color="lightcyan", bins=10)
plt.title("Figure 2. Number of beds")
plt.ylabel('Frequency')
plt.xlabel('Number of beds')
props = dict(boxstyle='round', facecolor='white',lw=0.5)
textstr = '$\mathrm{Mean}=%.1f$\n$\mathrm{S.D.}=%.1f$\n$\mathrm{n}=%.0f$'%(m_bed, sd_bed, n)
plt.text (7.5,57000, textstr , bbox=props)
plt.axvline(x=m_bed, linewidth=2,linestyle= 'solid', color="orange", label='Mean')
plt.show()

"""(EBC) he añadido el tamaño de la muestra al gráfico, a los 3 que siguen

Bath
"""

efe = df['bath'].describe() 
efe
n = df.bath.count() 
m_bath= df.bath.mean()
sd_bath = df.bath.std()

x = df['bath']
plt.hist(x,edgecolor='black', color="lightcyan", bins=10)
plt.title("Figure 3. Number of baths")
plt.ylabel('Frequency')
plt.xlabel('Number of baths')
props = dict(boxstyle='round', facecolor='white',lw=0.5)
textstr = '$\mathrm{Mean}=%.1f$\n$\mathrm{S.D.}=%.1f$\n$\mathrm{n}=%.0f$'%(m_bath, sd_bath, n)
plt.text (7.5,60000, textstr , bbox=props)
plt.axvline(x=m_bath, linewidth=2,linestyle= 'solid', color="orange", label='Mean')
plt.show()

"""Car"""

efs = df['car'].describe() 
efs
n = df.car.count() 
m_car= df.car.mean()
sd_car = df.car.std()

x = df['car']
plt.hist(x,edgecolor='black', color="lightcyan", bins=10)
plt.title("Figure 4. Number of parking lots")
plt.ylabel('Frequency')
plt.xlabel('Number of parking lots')
props = dict(boxstyle='round', facecolor='white',lw=0.5)
textstr = '$\mathrm{Mean}=%.1f$\n$\mathrm{S.D.}=%.1f$\n$\mathrm{n}=%.0f$'%(m_car, sd_car, n)
plt.text (7.5,75000, textstr , bbox=props)
plt.axvline(x=m_car, linewidth=2,linestyle= 'solid', color="orange", label='Mean')
plt.show()

"""Property type"""

mytable = pd.crosstab(df.propType, columns="count", normalize='columns')*100
# print(mytable)
print (round(mytable,1))
# print(mytable.sum())


plt.figure(figsize=(13,5))
plt.bar(mytable.index, mytable['count'], color="lightcyan", edgecolor='black')
plt.xlabel('Property Type')
plt.ylabel('Frequency')
plt.title('Figure 5. Property type')
plt.show()

"""Postal Code"""

cp_str = str(df['postalCode'])
print(type(cp_str))

#No me sale, se ha de pasar a str y despues realizar la tabla y representarlo (que alguien lo mire please)
mytable1 = pd.crosstab(df.cp_str, columns="count", normalize='columns')*100
print(mytable1)
print (round(mytable1,1))
plt.figure(figsize=(13,5))
plt.bar(mytable1.index, mytable1['count'])
plt.xlim(2000,3000)
plt.xlabel('Suburb')
plt.ylabel('Frequency')
plt.title('Figure 6. Suburb')
plt.show()

"""HIPÓTESIS 1:

*   HO: El número de camas no influye en el precio de venta.
*   H1: A mayor número de camas, mayor precio de venta.



"""

sp_highp = df.loc[  (df['sellPrice']>=1.800000e+06), "bed"]
sp_averagep = df.loc[ ((df['sellPrice']>= 1.197500e+06) & (df['sellPrice']<1.800000e+06)), "bed"]
sp_lowp = df.loc[  (df['sellPrice']<1.197500e+06) ,"bed"]


res3=stats.f_oneway(sp_highp,sp_averagep,sp_lowp)

print("F:", round(res3[0],3), "P.value:", round(res3[1],3))

ax = sns.pointplot(x="sellPrice_cat", y="bed", data=df, ci=95, join=0)
#plt.yticks(np.arange(0, 2000, step=100))
#plt.ylim(0,2000)
plt.axhline(y=df.bed.mean(), linewidth=1, linestyle= 'dashed', color="green")
props = dict(boxstyle="round", facecolor="white", lw=0.5)
plt.text(0,4,'Mean:1.266840e+06''\n''n:199051' '\n' 'F:12355.624' '\n' 'Pval.0,00:', bbox=props)
plt.xlabel('Number of beds')
plt.title('Figure 1. Precio de venta según el número de camas.''\n')
plt.show()

#no entiendo este error

"""HIPÓTESIS
H2--> Influye la fecha de venta en el preciode venta. Cualitativa por cuantitativa-->Es interesante ya que si coincide con un periodo de crisis económica el precio podría verse afectado.
H3-->Influye el suburbio en el precio de venta.-->Cualitativa por cuantitativa
H4-->Influye el codigo postal en el precio de venta.-->Yo diría que es cuanti por cuali por que los estadísticos descriptivos del código postal no deben ser importantes a la hora de realizar el análisis.-->Esta hipótesis es parecida a la anterior ya que es el precio segun la zona, pero el código postal debería abarcar un rango terriotrial mayor que el suburbio, asi que se podrían extraer datos distintos, si os fijáis un mismo código postal abarca varios suburbios, se puede comprobar en el dataset. Corregidme si no estoy en lo cierto.

H5-->Influye el número de baños en el precio de venta.-->Cuanti por cuanti.
H6-->Influye el número de plazas de garaje en el precio de venta-->Cuanti por cuanti
H7-->Influye el tipo de propiedad de la casa en el precio de venta-->Cuali por cuanti


"""

HO: no influye el número de baños en el precio de venta de la vivienda
H5: si influye el número de baños en el precio de venta de la vivienda (Por nfavoe, mis variables salen desordenadas, si alguien puede ayudarme)

"""***Enrique, parte del subsetting por años***"""

df.info()

# seguro que con un FOR queda más elegante
m_sellp_11= df['sellPrice']['2011'].mean()/1000
m_sellp_12= df['sellPrice']['2012'].mean()/1000
m_sellp_13= df['sellPrice']['2013'].mean()/1000
m_sellp_14= df['sellPrice']['2014'].mean()/1000
m_sellp_15= df['sellPrice']['2015'].mean()/1000
m_sellp_16= df['sellPrice']['2016'].mean()/1000
m_sellp_17= df['sellPrice']['2017'].mean()/1000
m_sellp_18= df['sellPrice']['2018'].mean()/1000
m_sellp_19= df['sellPrice']['2019'].mean()/1000
# divido por 1000 porque el precio sale en millones y en le gráfico se lee peor
preciomedioyear = [m_sellp_11, m_sellp_12,m_sellp_13,m_sellp_14,m_sellp_15,m_sellp_16,m_sellp_17,m_sellp_18,m_sellp_19,]
print(preciomedioyear)


bar_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'] # lista de etiquetas el eje X
plt.bar(bar_list, preciomedioyear, edgecolor='black') # primer argumento=nombre barras, segundo argumento=longitud de las barras
plt.title('Figure 1. Average sell price by year')
plt.ylabel('Sell Price x1000$')
plt.xlabel('Year')
# plt.text(2.1, 60, 'n: 731')
plt.show()

"""LUIS"""

os.chdir(r'C:\Users\luiso\Desktop\EDEM21-22\Fundamentos')
os.getcwd()

df = pd.read_csv ('SydneyHousePrices.csv', sep=',',decimal = '.')



df.sellPrice.describe()




df.loc[  (df['sellPrice']<1.197500e+06) ,"sellPrice_str"]= "Low price"
df.loc[ ((df['sellPrice']>= 1.197500e+06) & (df['sellPrice']<1.800000e+06)) ,"sellPrice_str"]= "Average price"
df.loc[  (df['sellPrice']>=1.800000e+06) ,"sellPrice_str"]= "High price"

my_categories=["Low price", "Average price", "High price"]
my_price_type = CategoricalDtype(categories=my_categories, ordered=True)
df["sellPrice_cat"] = df.sellPrice_str.astype(my_price_type)


mytable = pd.crosstab(df.sellPrice_cat, columns="count", normalize='columns')*100
print(mytable)
print (round(mytable,1))





#Formato del gráfico.
plt.figure(figsize=(5,5))
ax = sns.pointplot(x="sellPrice_str", y="bath", data=df,ci=95, join=0)

#Ajustar eje eje y
plt.yticks(np.arange(0, 6, step=1))
plt.ylim(0, 6)