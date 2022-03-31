import pandas as pd
import streamlit as st 
import numpy as np
import plotly.graph_objs as go
from online_metrics.create_data import create_dataframe
from basket_optimization.basket_optimization import select_multiple_products, create_basket, create_basket_set, build_frequent_sets, build_rules


def display_basket():
    st.header("Basket Optimization")
    st.write("""Market Basket Analysis is one of the key techniques used by large retailers to uncover associations between items. It works by looking for combinations of items that occur together frequently in transactions. To put it another way, it allows retailers to identify relationships between the items that people buy.
     """)
    data = create_dataframe()
    data = select_multiple_products(data)

    basket = create_basket(data)
    basket_set = create_basket_set(basket)

    st.subheader("Frequent Itemset")
    st.write(""" An itemset is considered as "frequent" if it meets a user-specified support threshold.""")
    frequent_itemsets = build_frequent_sets(basket_set)
    st.dataframe(frequent_itemsets.head(15))

    st.subheader("Association Rules")
    st.write("""Association rules are usually required to satisfy a user-specified minimum support and a user-specified minimum confidence at the same time.""")
    rules = build_rules(frequent_itemsets)
    st.dataframe(rules)
