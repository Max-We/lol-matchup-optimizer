#!/usr/bin/env python
# coding: utf-8

# In[20]:


import json
import pickle
from itertools import islice

from champs import top_champs

# Open the pkl file in read binary mode
with open('full_result.pickle', 'rb') as f:
    data = pickle.load(f)


# In[21]:

my_champ = input("Pick Your Champion")


# In[22]:


data[my_champ]


# In[23]:


results = {}
for c in data:
    garen_data = data[my_champ].copy()
    for k, v in garen_data.items():
        if float(v) < 0:
            garen_data[k] = 0 if float(data[c].get(k, 0)) > 0 else float(garen_data[k])
            # if float(data[c].get(k, 0)) > 0:
            #     print(f"{c} counters weakness {k}")

    results[c] = 0
    for value in garen_data.values():
        if float(value) < 0:
            results[c] += 1


# In[24]:


results = dict(sorted(results.items(), key=lambda item: item[1]))

for c in results:
    print(f"{c}: {results[c]}")


# In[25]:


def weak_matrix(champ):
    results = {}
    for c in data:
        garen_data = data[champ].copy()
        for k, v in garen_data.items():
            if float(v) < 0:
                garen_data[k] = 0 if float(data[c].get(k, 0)) > 0 else float(garen_data[k])
                # if float(data[c].get(k, 0)) > 0:
                #     print(f"{c} counters weakness {k}")
    
        results[c] = 0
        for value in garen_data.values():
            if float(value) < 0:
                results[c] += 1
        results = dict(sorted(results.items(), key=lambda item: item[1]))
    return dict(islice(results.items(), 7))


# In[26]:


def score(champ1, champ2):
    results = {}
    garen_data = data[champ1].copy()
    for k, v in garen_data.items():
        if float(v) < 0:
            garen_data[k] = 0 if float(data[champ2].get(k, 0)) > 0 else float(garen_data[k])
            # if float(data[c].get(k, 0)) > 0:
            #     print(f"{c} counters weakness {k}")

    results[champ2] = 0
    for value in garen_data.values():
        if float(value) < 0:
            results[champ2] += 1
    results = dict(sorted(results.items(), key=lambda item: item[1]))
    return dict(islice(results.items(), 7))


# In[27]:


wm = weak_matrix(my_champ)
wm


# In[28]:


def get_best_third_champ(champ):
    results = {}
    for c in weak_matrix(champ):
        batch = {}
        for c2 in weak_matrix(c):
            m = score(champ, c2)
            for k, v in m.items():
                batch[k] = v
        results[c] = batch
    return results


# In[29]:


def evaluate_triplets(results, champ):
    final = {}
    for c in results:
        sums = {}
        for c2 in results[c]:
            sums[c2] = results[c][c2] + wm.get(c, 100)
            
        min_value = min(sums.values())
        min_keys = [key for key, value in sums.items() if value == min_value]
    
        final[c] = {}
        for k in min_keys:
            final[c][k] = sums[k]

    print(f"These are your best 3-trick combos for {champ}:\n")
    for c in final:
        for c2 in final[c]:
            print(f"- {champ}, {c}, {c2} (Score: {final[c][c2]})")
    print("\n* Score stands for amount of counters a combo has. Lower is better.")


# In[30]:


evaluate_triplets(get_best_third_champ(my_champ), my_champ)


# In[31]:


# for c in top_champs:
#     evaluate_triplets(get_best_third_champ(c), c)


# In[ ]:

input("Press enter to exit...")