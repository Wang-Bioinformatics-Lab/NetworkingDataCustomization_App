import streamlit as st
import pandas as pd

import gnpsdata
from gnpsdata import workflow_classicnetworking

# Write the page label
st.set_page_config(
    page_title="Second Page",
)

# Getting a text field
st.write("Welcome to the GNPS2 Classical Networking Customization For Tall Table!")

gnps2task = st.text_input("GNPS2 Task", "64c0216723a74d17b730dd93fee168b9")

clusterinfo_df = workflow_classicnetworking.get_clusterinfo_dataframe(gnps2task, gnps2=True)

# Cleanups
import os

clusterinfo_df["filename"] = clusterinfo_df["#Filename"].apply(lambda x: os.path.basename(x))
clusterinfo_df["cluster index"] = clusterinfo_df["#ClusterIdx"]

clusterinfo_df = clusterinfo_df[["filename", "cluster index"]]

# Filtering clusters to only those that have more 1 MS/MS
clustersummary_df = clusterinfo_df.groupby("cluster index").count()
clustersummary_df = clustersummary_df[clustersummary_df.filename > 1]
accepted_clusters = set(clustersummary_df.index)
clusterinfo_df = clusterinfo_df[clusterinfo_df["cluster index"].isin(accepted_clusters)]

# Getting Metadata From Dataset
try:
    metadata_df = workflow_classicnetworking.get_metadata_dataframe(gnps2task, gnps2=True)
except:
    # Making metadata for all filenames for itself
    all_filenames = set(clusterinfo_df["filename"])

    metadata_df = pd.DataFrame()
    metadata_df["filename"] = list(all_filenames)
    metadata_df["ATTRIBUTE_filename"] = metadata_df["filename"]

# Merging it all together
all_clusters_metadata_df = clusterinfo_df.merge(metadata_df, on="filename")

