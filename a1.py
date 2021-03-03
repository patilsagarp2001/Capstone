from bs4 import BeautifulSoup
import requests
import pandas as pd


List_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(List_url).text

soup = BeautifulSoup(source, 'xml')
table=soup.find('table')

#dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
column_names = ['Postalcode','Borough','Neighborhood']
df = pd.DataFrame(columns = column_names)

# Search all the postcode, borough, neighborhood 
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data

df.head()

df=df[df['Borough']!='Not assigned']

df[df['Neighborhood']=='Not assigned']=df['Borough']
df.head()



temp_df=df.groupby('Postalcode')['Neighborhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighborhood':'Neighborhood_joined'},inplace=True)

df_merge = pd.merge(df, temp_df, on='Postalcode')

df_merge.drop(['Neighborhood'],axis=1,inplace=True)

df_merge.drop_duplicates(inplace=True)

df_merge.rename(columns={'Neighborhood_joined':'Neighborhood'},inplace=True)

df_merge.head()

df_merge.shape
