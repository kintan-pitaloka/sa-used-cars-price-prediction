# ---
# jupyter:
#   jupytext:
#     formats: notebooks//ipynb,markdown//md,scripts//py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: 'Python 3.8.5 64-bit (''ds_env'': conda)'
#     metadata:
#       interpreter:
#         hash: 8d4d772f21767a3a72f3356b4ab1badff3b831eb21eba306d4ebdf1fe7777d12
#     name: 'Python 3.8.5 64-bit (''ds_env'': conda)'
# ---

# %% [markdown]
# # Exploratory Data Analysis

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import missingno as msno
from utils import *

pio.templates.default = "presentation"

# %%
df = pd.read_csv("../data/processed/after_prep.csv")
df.head()

# %%
df.describe()

# %%
msno.matrix(df, color=(0, 0.4, 0.7), figsize=(8, 4))

# %%
fig, ax = plt.subplots(2, 1, figsize=(12, 7))
sns.histplot(data=df, x="Price", ax=ax[0])
sns.boxplot(data=df, x="Price", ax=ax[1])
plt.show()

# %%
df[df["Price"] > 80]

# %%
num_cols = [
    col for col in df.drop(columns="Price").columns if df[col].dtype != "object"
]
cat_cols = [
    col for col in df.drop(columns="Price").columns if df[col].dtype == "object"
]

# %%
plt.figure(figsize=(15, 6))

for index, col in enumerate(num_cols[:3]):
    plt.subplot(2, 3, index + 1)
    sns.histplot(data=df, x=col)

for index, col in enumerate(num_cols[:3]):
    plt.subplot(2, 3, index + 4)
    sns.boxplot(data=df, x=col)

plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 6))

for index, col in enumerate(num_cols[3:]):
    plt.subplot(2, 3, index + 1)
    sns.histplot(data=df, x=col)

for index, col in enumerate(num_cols[3:]):
    plt.subplot(2, 3, index + 4)
    sns.boxplot(data=df, x=col)

plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(8, 6))
plt.subplot(211)
sns.histplot(data=df, x="Kilometers_Driven")
plt.subplot(212)
sns.boxplot(data=df, x="Kilometers_Driven")
plt.tight_layout()
plt.show()

# %%
df = df[~(df.Kilometers_Driven > 1e6)]
df.shape

# %%
plt.figure(figsize=(8, 6))
plt.subplot(211)
sns.histplot(data=df, x="Kilometers_Driven")
plt.subplot(212)
sns.boxplot(data=df, x="Kilometers_Driven")
plt.tight_layout()
plt.show()

# %%
df[df.Seats >= 9]

# %%
df.describe(include=["object"])

# %%
cat_cols

# %%
cols_toplot = ["Fuel_Type", "Transmission", "Location", "Owner_Type"]
plt.figure(figsize=(12, 8))
countplot_annot(2, 2, data=df, columns=cols_toplot, rotate=45, rcol=cols_toplot)
plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 4))
countplot_annot(1, 1, data=df, columns=["Brand"], rotate=90, rcol=["Brand"])
plt.ylim(0, 1300)
plt.show()

# %%
fig = px.bar(
    y=df["Series"].value_counts()[:50],
    x=df["Series"].value_counts()[:50].keys(),
    text=df["Series"].value_counts()[:50],
)
fig.update_layout(autosize=False, width=1200, height=500)
fig.show()

# %%
plt.figure(figsize=(15, 4))

for index, col in enumerate(["Fuel_Type", "Transmission", "Owner_Type"]):
    plt.subplot(1, 3, index + 1)
    sns.barplot(data=df, x=col, y="Price")

plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(15, 4))

for index, col in enumerate(["Fuel_Type", "Transmission", "Owner_Type"]):
    plt.subplot(1, 3, index + 1)
    sns.boxplot(data=df, x=col, y="Price")

plt.tight_layout()
plt.show()

# %%
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x="Location", y="Price")
plt.show()

# %%
plt.figure(figsize=(15, 8))
sns.boxplot(data=df, x="Location", y="Price")
plt.show()

# %%
plt.figure(figsize=(15, 8))
sns.barplot(data=df, x="Brand", y="Price")
plt.xticks(rotation=90)
plt.show()

# %%
plt.figure(figsize=(15, 8))
sns.boxplot(data=df, x="Brand", y="Price")
plt.xticks(rotation=90)
plt.show()

# %%
import category_encoders as ce

t_encoder = ce.TargetEncoder()
df_temp = t_encoder.fit_transform(df.drop(columns=["Price"]), df["Price"])
df_temp = pd.concat([df_temp, df["Price"]], axis=1)

plt.figure(figsize=(14, 10))
sns.heatmap(df_temp.corr(), annot=True, linewidths=0.5, fmt=".2f")
plt.show()

# %%
import plotly.express as px

fig = px.scatter(
    df,
    x="Power (bhp)",
    y="Engine (CC)",
    size="Price",
    color="Transmission",
    hover_name="Brand",
    log_x=True,
    size_max=25,
)

fig.update_layout(title="Engine and Power correlation")
fig.show()

# %%
fig = px.scatter(
    df,
    x="Mileage (kmpl)",
    y="Engine (CC)",
    size="Price",
    color="Fuel_Type",
    hover_name="Brand",
    log_x=True,
    size_max=25,
    category_orders={"Fuel_Type": ["Diesel", "Petrol", "CNG", "LPG", "Electric"]},
)

fig.update_layout(
    title=dict(text="Engine and Mileage correlation", x=0),
    height=500,
    width=800,
    margin=dict(l=100, r=100, t=100, b=100),
)
fig.show()

# %%
from sklearn.preprocessing import MinMaxScaler

df_grp = df.groupby("Year")["Price", "Mileage (kmpl)"].mean()
df_grp_scaled = MinMaxScaler().fit_transform(df_grp)
df_grp_scaled = pd.DataFrame(df_grp_scaled, columns=df_grp.columns, index=df_grp.index)

trace1 = go.Scatter(
    x=df_grp_scaled.index, y=df_grp_scaled["Price"], mode="lines+markers", name="Price"
)

trace2 = go.Scatter(
    x=df_grp_scaled.index,
    y=df_grp_scaled["Mileage (kmpl)"],
    mode="lines",
    name="Mileage (kmpl)",
)

data = [trace1, trace2]
layout = go.Layout(title="Price and Mileage over the time", xaxis=dict(title="Year"))

fig = go.Figure(data=data, layout=layout)


fig.show()

# %%
import plotly.graph_objects as go

df_grp = df.groupby(["Brand", "Transmission"], as_index=False)["Price"].median()
df_grp.sort_values(by="Price", inplace=True)
df_grp.head()

fig = px.bar(
    df_grp,
    x="Brand",
    y="Price",
    color="Transmission",
    title="Median price by Brand",
    height=500,
    width=800,
)

fig.show()

# %%
df_grp = df.groupby(["Brand"], as_index=False).agg(
    Median_Price=("Price", "median"), Count=("Price", "count")
)
df_grp.sort_values(by="Median_Price", inplace=True)
df_grp.head()

fig = px.bar(
    df_grp,
    x="Brand",
    y="Count",
    title="Count of Cars by Brand",
    text="Count",
    height=500,
    width=800,
)

fig.add_trace(
    go.Scatter(x=df_grp["Brand"], y=df_grp["Median_Price"] * 10, name="Median Price")
)

fig.show()

# %% [markdown]
# # Update for Final Presentation

# %%
df.head()

# %%
from sklearn.preprocessing import MinMaxScaler

df_grp = df.groupby("Brand", as_index=False).agg(
    car_count=("Brand", "count"), car_price=("Price", "median")
)
df_grp.sort_values(by="car_price", ascending=False, inplace=True)

scaler = MinMaxScaler()
df_grp["car_count_scaled"] = (
    scaler.fit_transform(df_grp["car_count"].values.reshape(-1, 1)) + 0.02
)
df_grp["car_price_scaled"] = (
    scaler.fit_transform(df_grp["car_price"].values.reshape(-1, 1)) + 0.02
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_grp["Brand"],
        y=df_grp["car_count_scaled"],
        text=df_grp["car_count"],
        textposition="auto",
        name="CAR COUNT",
    )
)

fig.add_trace(
    go.Bar(
        x=df_grp["Brand"],
        y=df_grp["car_price_scaled"],
        text=df_grp["car_price"],
        textposition="auto",
        name="MEDIAN CAR PRICE",
    )
)
fig.update_layout(height=500, width=1400)

fig.show()

# %%
from sklearn.preprocessing import MinMaxScaler

df_grp = df.groupby("Brand", as_index=False).agg(
    car_count=("Brand", "count"), car_price=("Price", "median")
)
df_grp.sort_values(by="car_price", ascending=False, inplace=True)
df_grp = df_grp[df_grp["car_count"] > 5]

scaler = MinMaxScaler()
df_grp["car_count_scaled"] = (
    scaler.fit_transform(df_grp["car_count"].values.reshape(-1, 1)) + 0.02
)
df_grp["car_price_scaled"] = (
    scaler.fit_transform(df_grp["car_price"].values.reshape(-1, 1)) + 0.02
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_grp["Brand"],
        y=df_grp["car_count_scaled"],
        text=df_grp["car_count"],
        textposition="auto",
        name="CAR COUNT",
    )
)

fig.add_trace(
    go.Bar(
        x=df_grp["Brand"],
        y=df_grp["car_price_scaled"],
        text=df_grp["car_price"],
        textposition="auto",
        name="MEDIAN CAR PRICE",
    )
)
fig.update_layout(height=500, width=1400)

fig.show()

# %%
df_grp = df.groupby("Brand", as_index=False).agg(
    car_count=("Brand", "count"), car_price=("Price", "median")
)
df_grp[df_grp["car_count"] < 5]

# %%
from sklearn.preprocessing import MinMaxScaler

df_grp = df.groupby("Location", as_index=False).agg(
    car_count=("Location", "count"), car_price=("Price", "median")
)
df_grp.sort_values(by="car_price", ascending=False, inplace=True)

scaler = MinMaxScaler()
df_grp["car_count_scaled"] = (
    scaler.fit_transform(df_grp["car_count"].values.reshape(-1, 1)) + 0.1
)
df_grp["car_price_scaled"] = (
    scaler.fit_transform(df_grp["car_price"].values.reshape(-1, 1)) + 0.1
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_grp["Location"],
        y=df_grp["car_count_scaled"],
        text=df_grp["car_count"],
        textposition="auto",
        name="CAR COUNT",
    )
)

fig.add_trace(
    go.Bar(
        x=df_grp["Location"],
        y=df_grp["car_price_scaled"],
        text=df_grp["car_price"],
        textposition="auto",
        name="MEDIAN CAR PRICE",
    )
)
fig.update_layout(height=400, width=1000)

fig.show()


# %%
def segment(price):
    if price <= 5.64:
        return "Low"
    elif price <= 20:
        return "Middle"
    else:
        return "High"


df["Segment"] = df["Price"].apply(segment)

fig = px.histogram(df, x="Segment", y="Price", histfunc="avg")
fig.show()


# %%

# %%
df_grp = df.groupby(["Segment", "Brand"], as_index=False).agg(Count=("Price", "count"))
df_grp.sort_values(by="Count", ascending=False, inplace=True)


def filtering(data):
    if data["Count"] < 100:
        return "Other"
    else:
        return data["Brand"]


df_grp["Brand2"] = df_grp.apply(filtering, axis=1)

fig = px.pie(df_grp[df_grp["Segment"] == "Low"], values="Count", names="Brand2")
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(title="Low", showlegend=False)
fig.show()

# %%
df_grp = df.groupby(["Segment", "Brand"], as_index=False).agg(Count=("Price", "count"))
df_grp.sort_values(by="Count", ascending=False, inplace=True)


def filtering(data):
    if data["Count"] < 80:
        return "Other"
    else:
        return data["Brand"]


df_grp["Brand2"] = df_grp.apply(filtering, axis=1)

fig = px.pie(df_grp[df_grp["Segment"] == "Middle"], values="Count", names="Brand2")
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(title="Middle", showlegend=False)
fig.show()

# %%
df_grp = df.groupby(["Segment", "Brand"], as_index=False).agg(Count=("Price", "count"))
df_grp.sort_values(by="Count", ascending=False, inplace=True)


def filtering(data):
    if data["Count"] < 20:
        return "Other"
    else:
        return data["Brand"]


df_grp["Brand2"] = df_grp.apply(filtering, axis=1)

fig = px.pie(df_grp[df_grp["Segment"] == "High"], values="Count", names="Brand2")
fig.update_traces(textposition="inside", textinfo="percent+label")
fig.update_layout(title="High", showlegend=False)
fig.show()

# %%
print(px.colors.qualitative.D3)

# %%
df_grp = df.groupby("Segment", as_index=False).agg(Count=("Brand", "count"))
df_grp.sort_values(by="Count", ascending=False, inplace=True)

colors = ["#F38B34"] * 3
colors[-1] = "lightslategray"

fig = go.Figure(
    data=[
        go.Bar(
            x=df_grp["Segment"],
            y=df_grp["Count"],
            text=df_grp["Count"],
            textposition="auto",
            marker_color=colors,
        )
    ]
)
fig.update_layout(
    title="Market Segments",
    xaxis=dict(title=""),
    yaxis=dict(title="Count"),
    height=500,
    width=800,
    margin=dict(l=100, r=50, t=100, b=50),
)
fig.show()


# %%
fig = px.histogram(
    df,
    x="Segment",
    color="Transmission",
    barnorm="percent",
    color_discrete_sequence=["#F38B34", "#349df3", "#8a34f3", "#9df334"],
)
fig.update_layout(
    title="Market segmentation based on Transmission",
    xaxis=dict(title=""),
    yaxis=dict(title="Proportion"),
    height=500,
    width=800,
    margin=dict(l=100, r=100, t=100, b=50),
)
fig.show()

# %%
fig = px.histogram(
    df,
    x="Segment",
    color="Owner_Type",
    barnorm="percent",
    category_orders={"Owner_Type": ["First", "Second", "Third", "Fourth & Above"]},
    color_discrete_sequence=["#F38B34", "#349df3", "#8a34f3", "#9df334"],
)
fig.update_layout(
    title="Market segmentation based on Owner Type",
    xaxis=dict(title=""),
    yaxis=dict(title="Proportion"),
    height=500,
    width=800,
    margin=dict(l=100, r=100, t=100, b=50),
)
fig.show()


# %%
def zone(data):
    if data in ["Kolkata"]:
        return "Eastern"
    elif data in ["Delhi", "Jaipur"]:
        return "Northern"
    elif data in ["Ahmedabad", "Mumbai", "Pune"]:
        return "Western"
    else:
        return "Southern"


# Northern ["Delhi", "Jaipur"]
# Central ["Kolkata"]
# Western ["Ahmedabad", "Mumbai", "Pune"]
# Southern ["Chennai", "Hyderabad", "Bengaluru", "Coimbatore", "Kochi"]

df["Zone"] = df["Location"].apply(zone)

fig = px.histogram(df, x="Segment", color="Zone", barnorm="percent")
fig.update_layout(
    title="Market segmentation based on Zone",
    xaxis=dict(title=""),
    yaxis=dict(title="Proportion"),
    height=500,
    width=800,
    margin=dict(l=100, r=100, t=100, b=50),
)
fig.show()

# %%
fig = px.histogram(
    df,
    x="Segment",
    color="Fuel_Type",
    barnorm="percent",
    category_orders={
        "Fuel_Type": ["Diesel", "Petrol", "CNG", "LPG", "Electric"],
        "Segment": ["Low", "Middle", "High"],
    },
    color_discrete_sequence=["#F38B34", "#349df3", "#8a34f3", "#9df334"],
)
fig.update_layout(
    title="Market segmentation based on Fuel Type",
    xaxis=dict(title=""),
    yaxis=dict(title="Proportion"),
    height=500,
    width=800,
    margin=dict(l=100, r=100, t=100, b=50),
)
fig.show()

# %%

