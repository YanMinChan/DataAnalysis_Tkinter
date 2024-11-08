import pandas as pd
import json

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

#
# View by browser
#
# Do we need to make it unique (a user can have a lot of event on the same page, or the user could have click (or did other event) on it a lot)
docs_views_browser = df["visitor_useragent"].unique()
print(docs_views_browser)

# write a function that remove the last part of the user agent (i.e. just Mozilla, not /5.0)
df["browser"] = df["visitor_useragent"]
df.loc[df["visitor_useragent"].str.lower().str.contains("mozilla"), "browser"] = "firefox"
df.loc[df["visitor_useragent"].str.lower().str.contains("ucweb"), "browser"] = "ucweb"
df.loc[df["visitor_useragent"].str.lower().str.contains("opera"), "browser"] = "opera"
df.loc[df["visitor_useragent"].str.lower().str.contains("dalvik"), "browser"] = "dalvik"

docs_views_browser = df["browser"].value_counts()
print(docs_views_browser)
print(len(df))

