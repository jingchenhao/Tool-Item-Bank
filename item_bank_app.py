import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing import nx_pydot
from functools import reduce
pd.options.mode.chained_assignment = None





#pip show streamlit




def fix_decimal3(cols):
    for i in range(cols.shape[1]):
        cols.iloc[:,i] = cols.iloc[:,i].apply(lambda x:format(x,".3f"))
    return cols




import random

# Define the range for ItemIds
min_value = 10000
max_value = 99999

# Generate 5000 random ItemIds
item_ids = [random.randint(min_value, max_value) for _ in range(5000)]

# Define the subjects and their corresponding percentages
subjects = ["Math"] * 1500 + ["Language Arts"] * 1500 + ["Natural Science"] * 1000 + ["Spanish Language Arts"] * 1000


# Define reporting categories for each subject
# reporting_categories = {
#     "Math": random.choice(['1.Probability', '2.Algebra', '3.Geometry', '4.Measurement']),
#     "Language Arts": random.choice(['1.Vocabulary', '2.Reading', '3.Grammar', '4.Writing']),
#     "Natural Science": random.choice(['1.Biology', '2.Physics', '3.Earth Science', '4.Chemistry']),
#     "Spanish Language Arts": random.choice(['1.Vocabulary', '2.Reading', '3.Grammar', '4.Writing'])
# }

# Randomly assign reporting categories to each subject
random.shuffle(subjects)
#reporting_category_list = [reporting_categories[subject] for subject in subjects]

RC_list = []
for subject in subjects:
    if subject == 'Math':
        RC = random.choice(['1.Probability', '2.Algebra', '3.Geometry', '4.Measurement'])
    elif subject == 'Language Arts' or subject == 'Spanish Language Arts':
        RC = random.choice(['1.Vocabulary', '2.Reading', '3.Grammar', '4.Writing'])
    elif subject == 'Natural Science':
        RC = random.choice(['1.Biology', '2.Physics', '3.Earth Science', '4.Chemistry'])  
    RC_list.append(RC)

#-------------------------
min_grade = 1
max_grade = 6

# Generate 5000 random integers in the specified range
grade = [random.randint(min_grade, max_grade) for _ in range(5000)]

field_test_year = ["2015"] * 1500 + ["2016"] * 1500 + ["2017"] * 2000
random.shuffle(field_test_year)

#--------------------
# Set the parameters for the normal distribution
mean = 0
std_deviation = 1
num_samples = 5000

# Generate the normal distribution data
normal_data = np.random.normal(mean, std_deviation, num_samples)

#-----------------------
dok = ["1"] * 1200 + ["2"] * 1800 + ["3"] * 1600 + ["4"] * 400
random.shuffle(dok)

#-----------------------
item_level = ["1"] * 1000 + ["2"] * 1800 + ["3"] * 1600 + ["4"] * 600
random.shuffle(item_level)
#----------------------------

ks_category = [random.randint(1, 10) for _ in range(5000)]





#'ItemId', 'Subject', 'Grade', 'DOK', 'Language', 'Field_Test_Year', 'Reporting_Category','Knowledge_and_Skill', 'difficulty','item_level'
# math ['1.Probability','2.Algebra','3.Geometry','4.Measurement']
# language arts ['1.Vocabulary','2.Reading','3.Grammar','4.Writing']
# science ['1.Biology','2.Physics','3.Earth Science','4.Chemistry']





data = {
    'ItemId': item_ids,
    'Subject': subjects,
    'Grade': grade,
    'DOK':dok,
    'Field_Test_Year': field_test_year,
    'Reporting_Category': RC_list,
    'Knowledge_and_Skill': ks_category,
    'difficulty':normal_data,
    'item_level':item_level,
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)





df['Language'] = 'English'
df.loc[df.Subject.str.contains('Spanish'),'Language'] = 'Spanish'
df['ItemId'] = 'A'+df['ItemId'].astype(str)
df['Knowledge_and_Skill'] = df['Reporting_Category'] + '.'+df['Knowledge_and_Skill'].astype(str)
df['Subject_Grade'] = df['Subject'] + '_G' + df['Grade'].astype(str)



st.set_page_config(layout="wide")
st.title("A Quick Look of the Item Pool Data")



# ---side bar (individual item)----
st.sidebar.markdown("# Field Test Year")
#option = '2022'
option_year = st.sidebar.selectbox("Select a field test year",('2015', '2016','2017','ALL'))
if option_year == 'ALL':
    df_sub = df.copy()
else:
    df_sub = df.loc[df.Field_Test_Year == option_year, :]

df_sub = df_sub.reset_index(drop=True)
st.sidebar.write('Pool Sample Size N:', df_sub.shape[0])
#-------------------------------


st.sidebar.markdown("# Testing Language")
#option = '2022'
option_language = st.sidebar.selectbox("Select a testing language",('English','Spanish','ALL'))
if option_language == 'ALL':
    df_sub = df_sub.copy()
else:
    df_sub = df_sub.loc[df_sub.Language == option_language, :]

df_sub = df_sub.reset_index(drop=True)
st.sidebar.write('Pool Sample Size N:', df_sub.shape[0])


st.sidebar.markdown("# Subject")
#option = '2022'
option_subject = st.sidebar.selectbox("Select a subject",('Math','Language Arts','Natural Science','Spanish Language Arts','ALL'))
if option_subject == 'ALL':
    df_sub = df_sub.copy()
else:
    df_sub = df_sub.loc[df_sub.Subject == option_subject, :]

df_sub = df_sub.reset_index(drop=True)
st.sidebar.write('Pool Sample Size N:', df_sub.shape[0])





#------ show a subset of the data----------------------------------
st.markdown("## Data Structure")
cols = ['ItemId','Language','Subject','Grade','Field_Test_Year','DOK','Reporting_Category','Knowledge_and_Skill','difficulty','item_level']
st_ms = st.multiselect("Columns", df_sub.columns.tolist(), default=cols)
st.write(df_sub[st_ms].head(10))


st.title("Item Difficulty")
item_dif_dis = round(df_sub.groupby(['Subject','Grade']).difficulty.describe()[['count','mean','std','min','50%','max']],3)
item_dif_dis = item_dif_dis.reset_index()
sub_order = ['Math','Natural Science','Language Arts','Spanish Language Arts']
item_dif_dis['Subject'] = pd.Categorical(item_dif_dis['Subject'], sub_order)
item_dif_table = item_dif_dis.sort_values(by=['Subject','Grade'])
item_dif_table[['mean','std','min','50%','max']] = fix_decimal3(item_dif_table[['mean','std','min','50%','max']])
item_dif_table = item_dif_table.rename(columns={'50%':'median'})
item_dif_table = item_dif_table.reset_index(drop=True)
item_dif_table['count'] = item_dif_table['count'].astype(int)
st.markdown("## Descriptive Statistics of Item Difficulty")
st.write(item_dif_table)

#---------------draw item difficulty distribtuion plot----------------------------------------
dif_fig = px.box(df_sub, x="Subject_Grade", y="difficulty",width=1000,height=600,color="Subject",template='plotly_white')
st.markdown("## Item Difficulty Boxplot")
st.plotly_chart(dif_fig, use_container_width=True)





st.title("Item DOK and RALD")
#---------------draw DOK and ALD pie charts----------------------------------------
dok_table = pd.DataFrame(df_sub.groupby(['DOK']).size()).reset_index().rename(columns={0:'N'})
ald_table = pd.DataFrame(df_sub.groupby(['item_level']).size()).reset_index().rename(columns={0:'N'})
col1, col2 = st.columns(2)
# # draw pie chart
col1.markdown("## Percentage of Items at Each DOK Level")
fig1 = px.pie(dok_table, values='N', names='DOK')
col1.plotly_chart(fig1, use_container_width=True)
# # draw pie chart
col2.markdown("## Percentage of Items at Each RALD Level")
fig2 = px.pie(ald_table, values='N', names='item_level')
col2.plotly_chart(fig2, use_container_width=True)




#-----------------------------------------------------
st.markdown("## Reporting Categories")
rc = df_sub.groupby(['Reporting_Category', 'item_level']).size().reset_index()
rc['percentage'] = df_sub.groupby(['Reporting_Category', 'item_level']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
rc.columns = ['Reporting_Category', 'item_level','Counts', 'Percentage']
stack_bar_rc = px.bar(rc, x='Reporting_Category', y=['Counts'], color='item_level', text=rc['Percentage'].apply(lambda x: '{0:1.1f}%'.format(x)),width=1000,height=600,template='none')#plotly_white

st.plotly_chart(stack_bar_rc, use_container_width=True)
#stack_bar_rc.show()




#-----------------------------------------------------
st.markdown("## Knowledge and Skills")
ks = df_sub.groupby(['Knowledge_and_Skill', 'item_level']).size().reset_index()
ks['percentage'] = df_sub.groupby(['Knowledge_and_Skill', 'item_level']).size().groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).values
ks.columns = ['Knowledge_and_Skill', 'item_level','Counts', 'Percentage']
stack_bar_ks = px.bar(ks, x='Knowledge_and_Skill', y=['Counts'], color='item_level', text=ks['Percentage'].apply(lambda x: '{0:1.1f}%'.format(x)),width=1000,height=600,template='none')#plotly_white

st.plotly_chart(stack_bar_ks, use_container_width=True)






