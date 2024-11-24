import ModelV2
import View

win = View.Window()
win.mainloop()

# Testing the ModelV2
model = ModelV2.Model()
model.load_data('../sample_small.json')
doc_id = "120111003737-ff0d62c2f9e64064b73f058095e4f081"
user_id = "b417fd6f88d6516d"
df = model.view_by_country(doc_id)
print(df["visitor_country"].unique())

df = model.view_by_continent(doc_id)
print(df["continent"].unique())

df = model.view_by_browser()
print(df["browser"].value_counts())

df = model.reader_profile()
print(df.head(10))

df = model.also_likes_default(doc_id=doc_id, user_id=user_id)
print(df)