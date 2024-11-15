import pandas as pd
import json
import itertools
import pycountry_convert as pc

#
# Load data
#
records = []
with open('sample_small.json') as f:
    for line in f:
        records.append(json.loads(line))

df = pd.DataFrame.from_records(records)

#
# View by country
#
doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
docs_views_country = df.loc[(df["subject_doc_id"] == doc_id) & (df["event_type"] == "impression")]
print(docs_views_country["visitor_country"].unique())
print(docs_views_country.head())
# Doing continent
docs_views_country["continent"] = docs_views_country["visitor_country"]

print(pc.country_alpha2_to_continent_code("US"))

for i in docs_views_country.index:
    docs_views_country.loc[i, "continent"] = pc.country_alpha2_to_continent_code(docs_views_country.loc[i, "visitor_country"])
print(docs_views_country["continent"].unique())

#
# View by browser
#
# Do we need to make it unique (a user can have a lot of event on the same page, or the user could have click (or did other event) on it a lot)
docs_views_browser = df["visitor_useragent"].unique()
#print(docs_views_browser)

# write a function that remove the last part of the user agent (i.e. just Mozilla, not /5.0)
df["browser"] = df["visitor_useragent"]
df.loc[df["visitor_useragent"].str.lower().str.contains("mozilla"), "browser"] = "firefox"
df.loc[df["visitor_useragent"].str.lower().str.contains("ucweb"), "browser"] = "ucweb"
df.loc[df["visitor_useragent"].str.lower().str.contains("opera"), "browser"] = "opera"
df.loc[df["visitor_useragent"].str.lower().str.contains("dalvik"), "browser"] = "dalvik"

docs_views_browser = df["browser"].value_counts()
print(docs_views_browser)
print(len(df))

#
# Reader profile
#
x = df.loc[(df["event_type"] == "pagereadtime")]
x = x.groupby(["visitor_uuid"])[["event_readtime"]].sum()
x = x.sort_values(by=["event_readtime"], ascending=False)
x = x.head(10)
print(x) # only the uuid there

#
# Also likes
#

def viewer(doc_uuid):
    viewers = df.loc[(df["subject_doc_id"] == doc_uuid) & (df["event_type"] == "impression")]
    return viewers["visitor_uuid"].unique()

def documents(viewer_uuid):
    document = df.loc[(df["visitor_uuid"] == viewer_uuid) & (df["event_type"] == "impression")]
    return document["subject_doc_id"].unique()

def also_likes(doc_uuid, user_uuid, sort):
    vs = viewer(doc_uuid)
    to_remove = documents(user_uuid)
    all_ds = []
    for v in vs:
        ds = documents(v)
        all_ds.extend(ds)
    res_iter = itertools.groupby(all_ds)
    res = [
        (key, len(list(group)))
        for key, group in res_iter
        if key not in to_remove
    ]
    res = sort(res)
    return res

def sorting(docs):
    return [
        z[0]
        for z in sorted(
            docs,
            key=lambda y: y[1],
            reverse=True
        )
    ]

print(also_likes(doc_id, "b417fd6f88d6516d", sorting))