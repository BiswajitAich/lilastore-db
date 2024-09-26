import json
import sys
import numpy as np
import pandas as pd

id = sys.argv[1]
cos_sim = np.load('recommendation/cos_sim.npy')
df = pd.read_pickle('recommendation/recommendation_data.pkl')

def recommendation(path_id):
    if path_id not in df['path_id'].values:
        print(f"Product with path_id '{path_id}' not found.")
        return []
    
    product_index = df[df['path_id'] == path_id].index[0]
    distances = cos_sim[product_index]
    product_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:11]
    
    recommends = []
    for i in product_list:
        recommends.append({
            'path': df.iloc[i[0]].path_id,
            'url': df.iloc[i[0]].url
        })
    
    return recommends


recommends = recommendation(id)
print(json.dumps(recommends))