import json
import requests
import pandas as pd



# Based on https://maayanlab.cloud/Enrichr/help#api with some modifications
ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/addList'
genes_str = '\n'.join([
    'YWHAZ', 'YWHAE', 'GAP43',"NRGN", "GDI1", "CPLX2", "NPTX2"
    #'YWHAZ', 'YWHAH', 'NPTX2', 'NPTXR', 'VGF', 'SCG2', 'CPLX2',"GAP43"  ## Previous lists
    #"YWHAZ", "STX7", "CHGA", "NPTXR", "NPTX2"
])
description = 'Synaptic paper genes'
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

## Pathway enrichment analysis
ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/enrich'
query_string = '?userListId=%s&backgroundType=%s'
user_list_id = user_list_id

# the columns are named as the json file
columns = ['Index', 'Pathway', 'p-value', 'Odds Ratio', 'Combined Score', 'Genes', 'Adjusted p-value', 'Column 8', 'Column 9']


################# BioPlanet_2019 #################
gene_set_library = 'BioPlanet_2019'
response = requests.get(
    ENRICHR_URL + query_string % (user_list_id, gene_set_library)
 )
if not response.ok:
    raise Exception('Error fetching enrichment results')

data2 = json.loads(response.text)
print(data2)

#Convert json to array
data2 = data2["BioPlanet_2019"]

#Convert array to df
BioPlanet_df = pd.DataFrame(data2, columns=columns)

#Remove rows where adjusted p-value is over 0.05
#BioPlanet_df = BioPlanet_df[BioPlanet_df['Adjusted p-value'] < 0.05]

# NEW CODE: Add pathway sizes using Option 1
print("Fetching pathway sizes...")
DOWNLOAD_URL = 'https://maayanlab.cloud/Enrichr/geneSetLibrary'
params = {'mode': 'text', 'libraryName': gene_set_library}

response = requests.get(DOWNLOAD_URL, params=params)

if response.ok:
    # Parse the response to get pathway sizes
    lines = response.text.strip().split('\n')
    pathway_sizes = {}
    
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split('\t')
            if len(parts) >= 3:  # Ensure we have pathway name and genes
                pathway_name = parts[0]
                genes = [g.strip() for g in parts[2:] if g.strip()]  # Skip description, get genes
                pathway_sizes[pathway_name] = len(genes)
    
    print(f"Loaded {len(pathway_sizes)} pathway sizes")
    
    # Add pathway size as a new column
    BioPlanet_df['Pathway_Size'] = BioPlanet_df['Pathway'].map(pathway_sizes)
    
    print("Added Pathway_Size column")
else:
    print("Warning: Could not fetch pathway sizes")
    
    
BioPlanet_df['Genes_Count'] = BioPlanet_df['Genes'].apply(len)
   
BioPlanet_df['Overlap'] = BioPlanet_df['Genes_Count'].astype(str) + '/' + BioPlanet_df['Pathway_Size'].astype(str)


BioPlanet_df.to_csv('BioPlanet_pathway_synapse.csv', index=False)
     
