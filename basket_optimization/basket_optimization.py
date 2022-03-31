import streamlit as st
from mlxtend.frequent_patterns import apriori, association_rules

def select_multiple_products(df):
    df = df[['order_id', 'order_item_id', 'product_id', 'seller_id',
       'shipping_limit_date', 'price', 'freight_value']]
    df.insert(7, 'quantity',1)
    #If you want to cross check the data you can replace 10 with 80.
    item_freq = df['product_id'].value_counts()
    df = df[df.isin(item_freq.index[item_freq >= 50]).values]
    return df

@st.cache
def create_basket(df):
    #Create a basket of all products, orders and quantity
    basket = (df.groupby(['order_id','product_id'])['quantity']).sum().unstack().reset_index().fillna(0).set_index('order_id')
    return basket

def encode_units(x):
    if x<= 0:
        return 0
    if x>=1:
        return 1
@st.cache
def create_basket_set(df):
    #Convert 0.0 to 0, convert the units to One hot encoded values
    basket_sets = df.applymap(encode_units)
    return basket_sets

def build_frequent_sets(df):
    #Build frequent itemsets
    frequent_itemsets = apriori(df, min_support = 0.0001, use_colnames = True)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets

def build_rules(df):
    #Create Rules
    rules = association_rules(df, metric = 'support', min_threshold = 0.0001)
    #Products having 50% confidence likely to be purchased together
    rules = rules[rules['confidence'] >= 0.30]
    return rules