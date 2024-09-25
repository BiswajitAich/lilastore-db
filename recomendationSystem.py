import sys
import pandas as pd
import regex as re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem.porter import PorterStemmer
id = sys.argv[1]
paths = [
        "/bangle/bracelet",
        "/bangle/mantasa",
        "/bangle/golden-bangle",
        "/bangle/oxydized-bangle",
        "/cosmetic/makeup",
        "/cosmetic/makeup",
        "/earring/adstone-earring",
        "/earring/adstone-earring",
        "/earring/fancy-earring",
        "/earring/funky-earring",
        "/earring/golden-earring",
        "/earring/oxydized-earring",
        "/earring/terracotta-earring",
        "/necklace/chemicalbead-necklace",
        "/necklace/choker",
        "/necklace/fancy-necklace",
        "/necklace/golden-necklace",
        "/necklace/kundan-necklace",
        "/necklace/mangalsutra",
        "/necklace/oxydized-necklace",
        "/necklace/terracotta-necklace",
        "/otherproduct/chain",
        "/otherproduct/kamarband",
        "/otherproduct/payal",
        "/otherproduct/ring"
        ]
def get_data():
    data = []
    for path in paths:
        try:
            with open(path[1:] +'.json', 'r') as f:
                jsdata = json.load(f)
                for item in jsdata:
                    item['path'] = path
                data.extend(jsdata)
        except FileNotFoundError:
            print(f"File {path}.json not found.")#lila-store-app-db\bangle\bracelet.json
    return data

def process_df(df):
  df['detail']=df['detail'].apply(lambda x: x.replace('[\n]',''))
  df['detail'] = df['detail'].apply(lambda x: ' '.join(re.sub('[".,:()]', ' ', x).replace('\n', ' ').lower().split()).strip())
  df['description'] = df["description"].apply(lambda x: x.lower().strip())
  return df

def join_columns(row):
    columns_to_join = ['price', 'detail', 'description']
    return ' '.join(str(row[col]) for col in columns_to_join)

ps = PorterStemmer()
def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)


data = get_data()
df = pd.DataFrame(data)
df = process_df(df)
df['tags'] = df.apply(join_columns, axis=1)
df["tags"] = df["tags"].apply(lambda x: x)
df['path_id'] = df['path'] + '/' + df['id'].astype(str)
df.drop(['price', 'detail', 'description', 'type', 'path', 'id'], axis=1, inplace=True)
df['tags'] = df['tags'].apply(stem)
cv = CountVectorizer(max_features=1000, stop_words='english')
vectors = cv.fit_transform(df['tags']).toarray()
cos_sim = cosine_similarity(vectors)

def recomendation(path_id):
    if path_id not in df['path_id'].values:
        print(f"Product with path_id '{path_id}' not found.")
        return []
    
    product_index = df[df['path_id'] == path_id].index[0]
    distances = cos_sim[product_index]
    product_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:11]
    
    recomends = []
    for i in product_list:
        recomends.append({
            'path': df.iloc[i[0]].path_id,
            'url': df.iloc[i[0]].url
        })
    
    return recomends


recomends = recomendation(id)
print(json.dumps(recomends))