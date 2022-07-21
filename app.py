import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

st.set_page_config(page_title="Fantasy League Database",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.cache  # Get the Required DataFrame from a CSV File
def get_data():
    frame = pd.read_csv('total.csv')
    return frame


df = get_data()

# --- Title Page ---
st.title("Your Fantasy League Database")
st.subheader('Welcome!')
st.text("Use the Sidebar to view the league members individual stat history page, "
        "and to filter out any league members or years for comparisons")

# --- SideBar ---
st.sidebar.header("Player and Year Filter")
league_member = st.sidebar.multiselect(
    "Select League Member:",
    options=df["User"].unique(),
    default=df["User"].unique()
)

year_selector = st.sidebar.multiselect(
    "Select Year:",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

df_selection = df.query(
    "User == @league_member & Year == @year_selector"
)
# ---- SideBar END ----

# --- Champions Table ---
df_selection2 = df_selection.rename({
    'PF/G': 'PPG',
    'PA/G': 'PAG'
}, axis=1)
df_selection2 = df_selection2.query('RK == 1')
df_selection2 = df_selection2.sort_values(by='Year', ascending=False)
table = st.container()

with table:
    st.subheader('Championship Seasons')
    fig_table = go.Figure(data=go.Table(
        columnwidth=[1, 2, 4, 1, 1, 2, 2, 1, 1, 1],
        header=dict(values=list(df_selection2[['Year', 'User', 'Team', 'W', 'L', 'PF', 'PA',
                                               'PPG', 'PAG', 'Moves']].columns),
                    fill_color='#fcbf49',
                    align='center',
                    line_color='darkslategray',
                    height=30,
                    font=dict(color='black', size=20)),
        cells=dict(values=[df_selection2.Year, df_selection2.User, df_selection2.Team,
                           df_selection2.W, df_selection2.L, df_selection2.PF, df_selection2.PA, df_selection2.PPG,
                           df_selection2.PAG, df_selection2.Moves],
                   line_color='darkslategray',
                   fill_color='white',
                   align='center',
                   height=30,
                   font_size=18)))
    # fig_table.update_layout(margin=dict(l=5, r=5, b=5, t=5))
    fig_table.update_layout(margin=dict(l=5, r=5, b=1, t=5), width=1400, height=300)
    st.write(fig_table)
# --- END Champions Table ---

# --- Wins BarChart ---
df_wl = df_selection.groupby(by=['User']).sum()[['W', 'L']].reset_index()
# df_wl = df_wl.reset_index()
df_wl = df_wl.sort_values(by='W', ascending=False)

fig_wl_bar = px.bar(
    df_wl,
    x='User',
    y=['W', 'L'],
    title='Wins and Loss per Member',
    color_discrete_sequence=['#17A589', '#CB4335'],
    template='plotly_white',
    text_auto=True,
    barmode='group'
)

fig_wl_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title='Wins',
    # xaxis_title='League Member',
    xaxis_title='',
    font=dict(size=15),
    title_font_size=26,
    # yaxis=(dict(showgrid=False)),
)
st.plotly_chart(fig_wl_bar, use_container_width=True)
# --- END Wins Chart ---

# --- Most Points Scored Table and Points Against Table ---
left_column1, right_column1 = st.columns(2)

df_points = df_selection.groupby(by='User')[['PF', 'PA']].sum().reset_index()
df_points = df_points.sort_values(by='PF', ascending=True)

# Points For Bar Chart
fig_points_bar = px.bar(
    df_points,
    y='User',
    x='PF',
    title='Total Points Scored',
    color_discrete_sequence=['#5e548e'],
    template='plotly_white',
    text_auto=True,
    orientation='h',
    height=700
    # barmode='group'
)

fig_points_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title='',
    xaxis_title='Points Scored',
    font=dict(size=16),
    title_font_size=24,
    # yaxis=(dict(showgrid=False)),
)

df_points = df_points.sort_values(by='PA', ascending=True)

# Points Against Bar
fig_points_ag_bar = px.bar(
    df_points,
    y='User',
    x='PA',
    title='Total Points Against',
    color_discrete_sequence=['#b56576'],
    template='plotly_white',
    text_auto=True,
    orientation='h',
    height=700
)

fig_points_ag_bar.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title='',
    xaxis_title='Points Against',
    font=dict(size=16),
    title_font_size=24,
    # yaxis=(dict(showgrid=False)),
)

with left_column1:
    st.plotly_chart(fig_points_bar)
with right_column1:
    st.plotly_chart(fig_points_ag_bar)
# --- END Most Points Scored Table and Points Against Table ---

# --- PPG a Season Range Chart
fig_ppg = px.line(
    df_selection,
    x='User',
    y='PF/G',
    color='User',
    title='Points Per Game Range',
    color_discrete_sequence=px.colors.qualitative.Dark24,
    markers=True,
    hover_data=["PF/G", "Year"]
)
fig_ppg.update_layout(
    font=dict(size=15),
    yaxis_title='PPG',
    xaxis_title='',
    height=700
)
st.plotly_chart(fig_ppg, use_container_width=True)
# --- END PPG a Season Range Chart

# --- PAG a Season Range Chart
fig_pag = px.line(
    df_selection,
    x='User',
    y='PA/G',
    color='User',
    title='Points Against per Game Range',
    color_discrete_sequence=px.colors.qualitative.Dark24,
    markers=True,
    hover_data=["PA/G", "Year"]
)
fig_pag.update_layout(
    font=dict(size=15),
    yaxis_title='PAG',
    xaxis_title='',
    height=700
)
st.plotly_chart(fig_pag, use_container_width=True)
# --- END PAG a Season Range Chart

# --- Scoring Titles Table ---
df_selection3 = df_selection.rename({
    'PF/G': 'PPG',
    'PA/G': 'PAG',
    'RK': 'Rank'
}, axis=1)

df_selection3 = df_selection3.sort_values('PF').drop_duplicates(['Year'], keep='last')
df_selection3 = df_selection3.sort_values(by='Year', ascending=False)
table2 = st.container()

with table2:
    st.subheader('Scoring Title Winners')
    st.write('Need everyone selected for true winners!')
    fig_st_table = go.Figure(data=go.Table(
        columnwidth=[1, 1, 2, 1, 1, 2, 2, 1],
        header=dict(values=list(df_selection3[['Year', 'Rank', 'User', 'W', 'L', 'PF', 'PPG']].columns),
                    fill_color='#c1fba4',
                    align='center',
                    line_color='darkslategray',
                    height=30,
                    font=dict(color='black', size=20)),
        cells=dict(values=[df_selection3.Year, df_selection3.Rank, df_selection3.User,
                           df_selection3.W, df_selection3.L, df_selection3.PF, df_selection3.PPG],
                   line_color='darkslategray',
                   fill_color='white',
                   align='center',
                   height=30,
                   font_size=18)))
    # fig_table.update_layout(margin=dict(l=5, r=5, b=5, t=5))
    fig_st_table.update_layout(margin=dict(l=5, r=5, b=1, t=5), width=1400, height=300)
    st.write(fig_st_table)
# --- END Scoring Title Table ---

# --- Worst Defense of the Year ---
df_selection4 = df_selection.rename({
    'PF/G': 'PPG',
    'PA/G': 'PAG',
    'RK': 'Rank'
}, axis=1)

df_selection4 = df_selection4.sort_values('PA').drop_duplicates(['Year'], keep='last')
df_selection4 = df_selection4.sort_values(by='Year', ascending=False)
table3 = st.container()

with table3:
    st.subheader('Worst Defense of the Year')
    fig_wd_table = go.Figure(data=go.Table(
        columnwidth=[1, 1, 2, 1, 1, 2, 2, 1],
        header=dict(values=list(df_selection4[['Year', 'Rank', 'User', 'W', 'L', 'PA', 'PAG']].columns),
                    fill_color='#ffd6ff',
                    align='center',
                    line_color='darkslategray',
                    height=30,
                    font=dict(color='black', size=20)),
        cells=dict(values=[df_selection4.Year, df_selection4.Rank, df_selection4.User,
                           df_selection4.W, df_selection4.L, df_selection4.PA, df_selection4.PAG],
                   line_color='darkslategray',
                   fill_color='white',
                   align='center',
                   height=30,
                   font_size=18)))
    # fig_table.update_layout(margin=dict(l=5, r=5, b=5, t=5))
    fig_wd_table.update_layout(margin=dict(l=5, r=5, b=1, t=5), width=1400, height=300)
    st.write(fig_wd_table)
# --- END worst Defense of the Year ---

# --- Moves Pie Chart ---
df_moves = df_selection.groupby(by='User')['Moves'].sum().reset_index()

fig_moves = px.pie(
    df_moves,
    values='Moves',
    names='User',
    title='Total Moves per Member'
)
fig_moves.update_traces(
    textinfo='percent+label',
    textposition='inside',
    textfont_size=16,
    textfont_color='black',
    # marker=dict(line=dict(color='#000000', width=1))
)
fig_moves.update_layout(
    margin=dict(t=40, b=0, l=0, r=0),
    uniformtext_minsize=14,
    uniformtext_mode='hide',
    title_font_size=24,
)
st.plotly_chart(fig_moves, use_container_width=True)
# --- END Moves Pie Chart ---
