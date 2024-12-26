#!/usr/bin/env python
# coding: utf-8

# DATA CLEANING

# In[1]:


import matplotlib as mpl
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import statsmodels.api as sm


# Import CSV file to dataframe

# In[2]:


df = pd.read_csv('/Users/bhavyasaivolepu/Downloads/Reported_Crash_Locations.csv')


# In[3]:


df.info()


# Let's explore the data and see if any data changes occur so randomly that they aren't useful for our analysis

# In[4]:


pd.set_option("display.max_columns", None)
df.describe(include='all').T


# Looks like X,Y are same as Longitude,Latitude respectively so we can remove them

# In[5]:


df.drop(['X','Y'], axis=1, inplace=True)
df.head(100)


# Some columns are irrelavant so we can drop them

# In[6]:


df.drop(['UpdateDate','key_crash','LocalUse','LocationCity'], axis=1, inplace=True)
df.head(100)


# Lets see at what places more accidents are taking place

# In[7]:


df['LocationRoadNameOn'].value_counts()


# We can see location road names are irregular so we will rename and replace them properly 

# In[8]:



df.loc[df['LocationRoadNameOn'].str.match(pat = '440', case=False), 'LocationRoadNameOn'] = 'I-440'
df.loc[df['LocationRoadNameOn'].str.match(pat='^(?!.*440).*40.*$', case=False), 'LocationRoadNameOn'] = 'I-40'
df.loc[df['LocationRoadNameOn'].str.match(pat='Captial BLVD', case=False), 'LocationRoadNameOn'] = 'CAPITAL BLVD'
df.loc[df['LocationRoadNameOn'].str.contains( 'GLENWOOD AVE', case=False), 'LocationRoadNameOn'] = 'GLENWOOD AVE'
df.loc[df['LocationRoadNameOn'].str.contains('AVENT FERRY', case=False), 'LocationRoadNameOn'] = 'AVENT FERRY RD'
df.loc[df['LocationRoadNameOn'].str.contains('PULLEN RD', case=False), 'LocationRoadNameOn'] = 'PULLEN RD'
df.loc[df['LocationRoadNameOn'].str.contains('CAPITAL BLVD', case=False), 'LocationRoadNameOn'] = 'CAPITAL BLVD'
df.loc[df['LocationRoadNameOn'].str.contains('WESTERN BLVD', case=False), 'LocationRoadNameOn'] = 'WESTERN BLVD'
df.loc[df['LocationRoadNameOn'].str.contains('SIX FORKS RD', case=False), 'LocationRoadNameOn'] = 'SIX FORKS RD'
df.loc[df['LocationRoadNameOn'].str.contains('NEW BERN AVE', case=False), 'LocationRoadNameOn'] = 'NEW BERN AVE'

df['LocationRoadNameOn'].value_counts()


# Okay,we can see that quite a few streets that don't have many acccidents, let's filter out LocationRoadNameOn with more than 50 accidents

# In[9]:


df = df[df.groupby('LocationRoadNameOn').LocationRoadNameOn.transform('count')>50].copy() 
df['LocationRoadNameOn'].value_counts()


# Now lets see all the important columns and clean them if necessary

# In[10]:


df['LocationRelationToRoad'].value_counts()


# In[11]:


df['LocationRampIndicator'].value_counts()


# In[12]:


df['LocationMilesFromRoad'].value_counts()


# Converting Miles into Feet to maintain the distance consistency

# In[13]:


df.loc[:,'LocationMilesFromRoad'] *= 5280


# In[14]:


df['LocationMilesFromRoad'].value_counts()


# Creating a new column in dataframe

# In[15]:


LocationInFeetFromRoad = df.loc[: , ['LocationMilesFromRoad', 'LocationFeetFromRoad']]
total = LocationInFeetFromRoad.sum(axis=1)
df['LocationInFeetFromRoad'] = total


# In[16]:


df.info()


# In[17]:


df["LocationInFeetFromRoad"].value_counts()


# In[18]:


df['LocationDirectionFromRoad'].value_counts()


# In[19]:


df['FirstHarmfulEvent'].value_counts()


# Renaming events to have uniform data

# In[20]:


df.loc[df['FirstHarmfulEvent'].str.contains('Left turn', na=False),'FirstHarmfulEvent'] = 'Left Turn'
df.loc[df['FirstHarmfulEvent'].str.contains('Right turn', na=False),'FirstHarmfulEvent'] = 'Right Turn'
df.loc[df['FirstHarmfulEvent'].str.contains('object', na=False),'FirstHarmfulEvent'] = 'Any object'
df.loc[df['FirstHarmfulEvent'].str.contains('Rear end', na=False),'FirstHarmfulEvent'] = 'Rear end'
df.loc[df['FirstHarmfulEvent'].str.contains('Sideswipe', na=False),'FirstHarmfulEvent'] = 'Sideswipe'
df.loc[df['FirstHarmfulEvent'].str.contains('Ran off', na=False),'FirstHarmfulEvent'] = 'Ran off Road'


# In[21]:


df['FirstHarmfulEvent'].value_counts()


# In[22]:


df['MostHarmfulEvent'].value_counts()


# Renaming events to have uniform data

# In[23]:


df.loc[df['MostHarmfulEvent'].str.contains('Ran off', na=False),'MostHarmfulEvent'] = 'Ran off road'
df.loc[df['MostHarmfulEvent'].str.contains('Left turn', na=False),'MostHarmfulEvent'] = 'Left Turn'
df.loc[df['MostHarmfulEvent'].str.contains('Right turn', na=False),'MostHarmfulEvent'] = 'Right Turn'
df.loc[df['MostHarmfulEvent'].str.contains('object', na=False),'MostHarmfulEvent'] = 'Any object'
df.loc[df['MostHarmfulEvent'].str.contains('Rear end', na=False),'MostHarmfulEvent'] = 'Rear end'
df.loc[df['MostHarmfulEvent'].str.contains('Sideswipe', na=False),'MostHarmfulEvent'] = 'Sideswipe'


# In[24]:


df['MostHarmfulEvent'].value_counts()


# In[25]:


df['RoadClassification'].value_counts()


# In[26]:


df['RoadFeature'].value_counts()


# Renaming events to have uniform data

# In[27]:


df.loc[df['RoadFeature'].str.contains('Off-ramp', na=False),'RoadFeature'] = 'OFF ramp'
df.loc[df['RoadFeature'].str.contains('On-ramp', na=False),'RoadFeature'] = 'ON ramp'


# In[28]:


df['RoadFeature'].value_counts()


# In[29]:


df.info()


# DATA EXPLORATION

# Lets see if weather has any effect on these accidents

# In[30]:


df['WeatherContributedToCrash'].value_counts()


# In[31]:


df1 = df[df['WeatherContributedToCrash'] == 'Yes']


# In[32]:


df1


# lets see what are the weather conditions that contritubed to the crash

# In[33]:


df1['WeatherCondition1'].value_counts()


# In[34]:


df1["WeatherCondition1"].value_counts().head(5).plot(kind="bar",figsize=(20, 10))
plt.title("Accidents based on Weather, Top 5 ")
plt.xlabel("Weather Condition")
plt.ylabel("Number of Accidents 2015-2022")
plt.show()


# We can see that Rain is the most common weather during the accident
# Lets plot them according to the year and see

# In[35]:


sns.countplot(y=df1['Crash_Date_Year'])
plt.title("By Year")
plt.xlabel("Total Number of Traffic Accidents")
plt.ylabel("Year")
plt.show()


# In[36]:


df1[df1["WeatherCondition1"] == "Rain"].groupby("Crash_Date_Year")["killed"].sum().plot(label='Rain',figsize=(20, 10))
df1[df1["WeatherCondition1"] == "Cloudy"].groupby("Crash_Date_Year")["killed"].sum().plot(label='Cloudy')
df1[df1["WeatherCondition1"] == "Clear"].groupby("Crash_Date_Year")["killed"].sum().plot(label='Clear')
df1[df1["WeatherCondition1"] == "Snow"].groupby("Crash_Date_Year")["killed"].sum().plot(label='Snow')
df1[df1["WeatherCondition1"] == "Sleet, hail, freezing rain/drizzle"].groupby("Crash_Date_Year")["killed"].sum().plot(label='Sleet, hail, freezing rain/drizzle') 
plt.legend()
plt.title("Deaths by Year, Top 5 Conditions")
plt.ylabel("Death rating sum")
plt.xlabel("Year")
plt.show()


# As we can see from these plots, in 2015, there were accidents caused by rain that caused people to die.

# Let's find out where most of the fatal accidents

# In[37]:


df1["LocationRoadNameOn"].value_counts().head(10).plot(kind="bar",figsize=(20, 10))
plt.title("Total Accidents by Road/street, top 10")
plt.xlabel("Road/Street Name")
plt.ylabel("Number of Accidents 2015-2022")
plt.show()


# Okay,By this plot we undertsood that I-40 is where most accidents take place under the weather condition
# Now lets look where accidents take place overall in raleigh 

# In[38]:


df["LocationRoadNameOn"].value_counts().head(10).plot(kind="bar",figsize=(20, 10))
plt.title("Total Accidents by Road/street, top 10")
plt.xlabel("Road/Street Name")
plt.ylabel("Number of Accidents 2015-2022")
plt.show()


# Okay,irrespective of the weather condition most of the accidents occur on I-40

# Lets explore how many accidents take place in different year, months,day of week,Hour of the day irrespective of deeaths

# In[39]:


sns.countplot(y=df['Crash_Date_Month'],order=['January','February','March','April','May','June','July','August','September','October','November','December'])
plt.title("By Month")
plt.xlabel("Total Number of Traffic Accidents")
plt.ylabel("Month")
plt.show()


# October is the month with highest accidents,July being the least

# In[40]:


sns.countplot(y=df['Crash_Date_DOW'],order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title("By Day of the Week")
plt.xlabel("Total Number of Traffic Accidents")
plt.ylabel("Day of the Week")
plt.show()


# Day with highest accidents is friday and least is Sunday.

# In[41]:


sns.countplot(y=df['Crash_Date_Hour'])
plt.title("By Hour of the Day")
plt.xlabel("Total Number of Traffic Accidents")
plt.ylabel("Hour of the Day")
plt.show()


# In[42]:


sns.countplot(y=df['Crash_Date_Year'])
plt.title("By Year")
plt.xlabel("Total Number of Traffic Accidents")
plt.ylabel("Year")
plt.show()


# In year 2019,2022 there are highest,Least no of accidents

# Now,lets see in what months,week of the day,Hour of the day and which road/streets does this accidents take place where deaths took place

# In[43]:


df[df["LocationRoadNameOn"] == "I-40"].groupby("Crash_Date_Month")["killed"].sum().loc[['January','February','March','April','May','June','July','August','September','October','November','December']].plot(label='I-40',figsize=(20,10))
df[df["LocationRoadNameOn"] == "I-440"].groupby("Crash_Date_Month")["killed"].sum().loc[['January','February','March','April','May','June','July','August','September','October','November','December']].plot(label='I-440')
df[df["LocationRoadNameOn"] == "CAPITAL BLVD"].groupby("Crash_Date_Month")["killed"].sum().loc[['January','February','March','April','May','June','July','August','September','October','November','December']].plot(label='CAPITAL BLVD')
df[df["LocationRoadNameOn"] == "GLENWOOD AVE"].groupby("Crash_Date_Month")["killed"].sum().loc[['January','February','March','April','May','June','July','August','September','October','November','December']].plot(label='GLENWOOD AVE')
df[df["LocationRoadNameOn"] == "SIX FORKS RD"].groupby("Crash_Date_Month")["killed"].sum().loc[['January','February','March','April','May','June','July','August','September','October','November','December']].plot(label='SIX FORKS RD')
plt.legend()
plt.title("Deaths Increase by Month, Top 5 Road/Streets")
plt.ylabel("Death rating sum")
plt.xlabel("Month of Year")
plt.show()


# From the above plot we can tell where fatal accidents are occured and in which month
# for example:On Glenwood Rd the highest number of fatal accidents took place in Jan,May

# Similarly,Plotted for day of week , Hour of the day

# In[44]:


df[df["LocationRoadNameOn"] == "I-40"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='I-40',figsize=(20,10))
df[df["LocationRoadNameOn"] == "I-440"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='I-440')
df[df["LocationRoadNameOn"] == "CAPITAL BLVD"].groupby("Crash_Date_DOW")["killed"].sum().loc[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].plot(label='CAPITAL BLVD')
df[df["LocationRoadNameOn"] == "GLENWOOD AVE"].groupby("Crash_Date_DOW")["killed"].sum().loc[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].plot(label='GLENWOOD AVE')
df[df["LocationRoadNameOn"] == "SIX FORKS RD"].groupby("Crash_Date_DOW")["killed"].sum().loc[['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']].plot(label='SIX FORKS RD')
plt.legend()
plt.title("No of Deaths by Day of the Week, Top 5 Road/Streets")
plt.ylabel("Deaths rating sum ")
plt.xlabel("Day of the Week")
plt.show()


# In[45]:


df[df["LocationRoadNameOn"] == "I-40"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='I-40',figsize=(20,10))
df[df["LocationRoadNameOn"] == "I-440"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='I-440')
df[df["LocationRoadNameOn"] == "CAPITAL BLVD"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='CAPITAL BLVD')
df[df["LocationRoadNameOn"] == "GLENWOOD AVE"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='GLENWOOD AVE')
df[df["LocationRoadNameOn"] == "SIX FORKS RD "].groupby("Crash_Date_Hour")["killed"].sum().plot(label='SIX FORKS RD ')
plt.legend()
plt.title("No of deaths by Hour of the Day, Top 5 Streets")
plt.ylabel("Deaths rating sum")
plt.xlabel("Hour of the Day")
plt.show()


# In[46]:


df['MostHarmfulEvent'].value_counts()


# In[47]:


df[df["MostHarmfulEvent"] == "Rear end"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='Rear end',figsize=(20,10))
df[df["MostHarmfulEvent"] == "Sideswipe"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='Sideswipe')
df[df["MostHarmfulEvent"] == "Angle"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='Angle')
df[df["MostHarmfulEvent"] == "Left Turn"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='Left Turn')
df[df["MostHarmfulEvent"] == "Parked Motor Vehicle"].groupby("Crash_Date_Hour")["killed"].sum().plot(label='Parked Motor Vehicle')
plt.legend()
plt.title("No of deaths by Hour of the Day, Top 5 HarmfulEvents")
plt.ylabel("Deaths rating sum")
plt.xlabel("Hour of the Day")
plt.show()


# In[48]:


df[df["MostHarmfulEvent"] == "Rear end"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='Rear end')
df[df["MostHarmfulEvent"] == "Sideswipe"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='Sideswipe')
df[df["MostHarmfulEvent"] == "Angle"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='Angle')
df[df["MostHarmfulEvent"] == "Left Turn"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='Left Turn')
df[df["MostHarmfulEvent"] == "Parked Motor Vehicle"].groupby("Crash_Date_DOW")["killed"].sum().plot(label='Parked Motor Vehicle')
plt.legend()
plt.title("No of deaths by  Day, Top 5 HarmfulEvents")
plt.ylabel("Deaths rating sum")
plt.xlabel("DOW")
plt.show()


# In[49]:


df[df["MostHarmfulEvent"] == "Rear end"].groupby("Crash_Date_Month")["killed"].sum().plot(label='Rear end',figsize=(20,10))
df[df["MostHarmfulEvent"] == "Sideswipe"].groupby("Crash_Date_Month")["killed"].sum().plot(label='Sideswipe')
df[df["MostHarmfulEvent"] == "Angle"].groupby("Crash_Date_Month")["killed"].sum().plot(label='Angle')
df[df["MostHarmfulEvent"] == "Left Turn"].groupby("Crash_Date_Month")["killed"].sum().plot(label='Left Turn')
df[df["MostHarmfulEvent"] == "Parked Motor Vehicle"].groupby("Crash_Date_Month")["killed"].sum().plot(label='Parked Motor Vehicle')
plt.legend()
plt.title("No of deaths by Month, Top 5 HarmfulEvents")
plt.ylabel("Deaths rating sum")
plt.xlabel("Month of the Day")
plt.show()


# Now lets look at the different type of persons presnet during the crash

# In[50]:


df['drivers'].value_counts()
 


# In[51]:


df['passengers'].value_counts()


# In[52]:


df['pedestrians'].value_counts()


# If we observe this value counts we can say that there are majority of 2 drivers, 1 passenger,1 pedastrian at the time of crash

# Lets see how far is the locations from these roads

# In[53]:


df["LocationInFeetFromRoad"].value_counts()


# 7128 feet is farthest location from that Road,0 ft is most frequent here which means crash is on that road itself

# Summary:
#  After analyzing the crashes data in raleigh from 2015-2022,these are some observations:
# - From all these plots, Only about 5% of the crash were effected by weather condition which is mostly by rain.Rain is also major factor in deaths during the crash.
# - Apart from weather condition,we got to know crashes have taken place majorly in 2019 year,october month,Friday,around 17:00 on I-40 road.
# - Most harmuful event that had occured and caused deaths is Rear end.
# - Most of the accidents happen on road itself or 100ft away on road but also got know that some crashes are as far as 7128feet from road. 

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




