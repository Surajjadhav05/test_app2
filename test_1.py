import pandas as pd
import streamlit as st
import pyTigerGraph as tg

Domain = "https://fraud-demo.i.tgcloud.io"
Graph = "Fraud"
Secret = "o98ha1r06p1rh5t1uhqkak9svsikof0p"
conn = tg.TigerGraphConnection(host=Domain, graphname=Graph, gsqlSecret=Secret)
 
authToken = conn.getToken(Secret)
authToken = authToken[0]

st.title("Streamlit test Web app")

uploaded_file=st.file_uploader("Please upload account file here", type=["csv","excel"])

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.header("Uploaded File")
    st.dataframe(df)
    
    account_nos=df.account_no.unique().tolist()

    bob = conn.runInstalledQuery(queryName = "output_ids",params={"ids":account_nos})

    df=pd.DataFrame(columns=["acc_no","hops","cid","in_giant_component"])
    acc_no=[]
    hops=[]
    cid=[]
    account_opened_date=[]

    for i in range(len(bob[0]["output"])):
        value=bob[0]["output"][i]['attributes']
        acc_no.append(value['id'])
        hops.append(value['hops'])
        cid.append(value['cid'])
        account_opened_date.append([value['opened']])
        
        

    df["acc_no"]=acc_no
    df["hops"]=hops
    df['cid']=cid
    df['account_opened_date']=account_opened_date

    st.header("Account Details")
    st.dataframe(df)

else:
    st.header("Please Upload file to fetch data")
