import json
import requests
import pandas as pd

# Based on https://maayanlab.cloud/Enrichr/help#api with some modifications
ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/addList'
genes_str = '\n'.join([
    #'YWHAZ', 'YWHAH', 'NPTX2', 'NPTXR', 'VGF', 'SCG2', 'CPLX2'
    "GAD1", "NRGN", "SNCG"
])
description = 'Synaptic genes'
payload = {
    'list': (None, genes_str),
    'description': (None, description)
}

response = requests.post(ENRICHR_URL, files=payload)
if not response.ok:
    raise Exception('Error analyzing gene list')

data = json.loads(response.text)
print(data)

user_list_id = data['userListId']

ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/view?userListId=%s'
user_list_id = user_list_id
response = requests.get(ENRICHR_URL % user_list_id)
if not response.ok:
    raise Exception('Error getting gene list')

data=json.loads(response.text)
print(data)


ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'
user_list_id = user_list_id
gene_set_library = 'BioPlanet_2019'
response = requests.get(
    ENRICHR_URL + query_string % (user_list_id, gene_set_library)
 )
if not response.ok:
    raise Exception('Error fetching enrichment results')

data= json.loads(response.text)
print(data)

#Convert json to array
data = data["BioPlanet_2019"]

# the columns are named as in the json file
columns = ['Index', 'Pathway', 'p-value', 'Odds Ratio', 'Combined Score', 'Genes', 'Adjusted p-value', 'Column 8', 'Column 9']

df = pd.DataFrame(data, columns=columns)

#remove rows where adjusted p-value is over 0.05
df = df[df['Adjusted p-value'] < 0.05]


#For exporting to R the df is saved as a csv file
df.to_csv('pathway_data_No_Change_Prots.csv', index=False)