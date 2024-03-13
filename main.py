import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Data Visualisation")
st.title("Spotify Data Visualisation")
st.header("Users:")

df1 = pd.read_json("./Data/Userdata.json", orient='index')
df2 = pd.read_json("./Data/StreamingHistory.json")
df3 = pd.read_json("./Data/Inferences.json")

df_info = pd.DataFrame(df3)
df_history = pd.DataFrame(df2)
df_user = pd.DataFrame(df1)

# ---------------- Inferences-----------------#
ls = []
for i in range(len(df_info)):
    infor = df_info['inferences'][i][:2]
    ls.append(infor)
df_infor = pd.DataFrame(ls)
df_infor = df_infor.rename(columns={0: "party"})
df_infor['count'] = df_infor.groupby('party')['party'].transform('count')

# --------Inferences datset------------------#
df_infor = df_infor.drop_duplicates()
sum = df_infor['count'].sum()
df_infor['percentage'] = (df_infor['count'] / sum) * 100

# --------Inferences Graph------------------#
bar_chart = px.bar(df_infor, x='party', y='count',
                   text='count',
                   color_discrete_sequence=['#F63366'],
                   template='plotly_white')

pie_chart = px.pie(df_infor, values='percentage', names='party', color_discrete_sequence=['#F63366'])

df_group = df_history.groupby('artistName').sum()

# -----------------StreamlitSetup--------------#

# r = st.button("Reset", type='primary')
# st.caption("(Double click to reset Visualisation)")

col1, col4, col2, col3 = st.columns(4)
with col1:
    st.text(df_user[0]['username'])
with col2:
    button = st.button("Inferences Data")
with col4:
    history_button = st.button("Streaming Data")
with col3:
    button2 = st.button("User Details")

if "load_state1" not in st.session_state:
    st.session_state.load_state1 = False

if "load_state" not in st.session_state:
    st.session_state.load_state = False

if button2:
    st.session_state.load_state1 = False
    st.session_state.load_state = False
    st.table(df_user[0])

if button or st.session_state.load_state:
    st.session_state.load_state = True
    st.session_state.load_state1 = False

    st.subheader("Inferences")
    st.text("1P - First Party Services\n3P - Third Party Services")
    tog = st.toggle("Pie Chart")
    if tog:
        st.plotly_chart(pie_chart)
    else:
        st.plotly_chart(bar_chart)
    data = st.button("Show Full Data")
    st.button("Reset", type='primary', key=2)
    if data:
        st.table(df_info)

if history_button or st.session_state.load_state1:

    st.session_state.load_state = False
    st.session_state.load_state1 = True
    if history_button:
        st.experimental_rerun()
    st.subheader("Streaming history")
    choices = st.multiselect("Choose to Compare Which are most played:", ["Artist", 'Track'])
    for i in choices:
        if i == 'Artist':
            df_group = df_group.sort_values(by='msPlayed', ascending=False)
            values = st.slider(label="Select no of Datapoints:", value=(0, len(df_group)))
            df_group = df_group.iloc[values[0]:values[1]]
            bar_chart2 = px.bar(df_group, y='msPlayed', x=df_group.index,
                                color_discrete_sequence=['#F63366'],
                                template='plotly_white',
                                title="Artist Vs msPlayed"
                                )

            st.plotly_chart(bar_chart2)


        elif i == 'Track':

            df_grouped2 = df_history.groupby('trackName').sum().sort_values(by='msPlayed', ascending=False)
            values_2 = st.slider(label="Select no of Datapoints:", value=(0, len(df_grouped2)))
            df_grouped2 = df_grouped2.iloc[values_2[0]:values_2[1]]
            bar_chart3 = px.bar(df_grouped2, y='msPlayed', x=df_grouped2.index,
                                color_discrete_sequence=['#F63366'],
                                template='plotly_white',
                                title="TrackName Vs msPlayed")

            st.plotly_chart(bar_chart3)
    data2 = st.button("Show Full Data", key=5)
    st.button("Reset", type='primary', key=3)
    if data2:
        st.table(df_history)
