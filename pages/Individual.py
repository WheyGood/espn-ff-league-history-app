import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 16)

st.set_page_config(page_title="Your Individual League History",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.cache
def get_data():
    frame = pd.read_csv('total.csv')
    return frame


df = get_data()

# ---- SideBar ----
st.sidebar.header("Filter Here")
league_member = st.sidebar.selectbox(
    "Select League Member:",
    options=df["User"].unique()
    # default=df["User"].unique()
)

year_selector = st.sidebar.multiselect(
    "Select Year:",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

df_selection = df.query(
    "User == @league_member & Year == @year_selector"
)
# --- END Sidebar ---

# --- Main Page ---
st.title(f"{league_member}'s History")

# --- KPIs ---
df_champ = df.query(
    "User == @league_member"
)
champs = (df_champ['RK'] == 1).sum()

first_col, second_col = st.columns(2)
with first_col:
    st.subheader(f'{", ".join(map(str, year_selector))}')
with second_col:
    st.subheader(f'Championship(s): {champs} :trophy:')

total_wins = int(df_selection['W'].sum())
total_loses = int(df_selection['L'].sum())
total_points_for = round(df_selection['PF'].sum(), 2)
total_points_against = round(df_selection['PA'].sum(), 2)
ppg = round(df_selection['PF/G'].mean(), 2)
papg = round(df_selection['PA/G'].mean(), 2)

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.text("Total Wins")
    st.text(total_wins)
with col2:
    st.text("Total Loses")
    st.text(total_loses)
with col3:
    st.text('Total Points For')
    st.text(total_points_for)
with col4:
    st.text('Total Points Against')
    st.text(total_points_against)
with col5:
    st.text('Points Per Game')
    st.text(ppg)
with col6:
    st.text('Points Against Per Game')
    st.text(papg)

st.markdown("---")
# --- END KPIs ---

# --- Wins, Loses, Ties Bar Chart and Points For and Against per Season ---
left_column, right_column = st.columns(2)

fig_player_wins = px.bar(
    df_selection,
    x='Year',
    y=['W', 'L', 'T'],
    title='Wins, Loses, and Ties per Year',
    color_discrete_sequence=['#17A589', '#CB4335', '#ffbf69'],
    template='plotly_white',
    text_auto=True
)

fig_player_wins.update_layout(
    yaxis_title='Wins',
    # plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False)),
)
fig_player_wins.update_layout(font=dict(size=15))

fig_average_points = px.line(
    df_selection,
    x='Year',
    y=['PF/G', 'PA/G'],
    title='Points For and Points Against per Season',
    color_discrete_sequence=['#5DADE2', '#F4D03F'],
    markers=True
)
# fig_average_points.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     # xaxis=(dict(showgrid=False))
# )
fig_average_points.update_layout(
    font=dict(size=15),
    yaxis_title='Points Per Game'
)

with left_column:
    st.plotly_chart(fig_player_wins)
with right_column:
    st.plotly_chart(fig_average_points)
# --- END Wins, Loses, Ties Bar Chart and Points For and Against per Season ---

# --- Final Ranking Line Graph ---
fig_player_rank = px.line(
    df_selection,
    x='Year',
    y='RK',
    title='Final Ranking Each Season',
    color_discrete_sequence=['#2E4053'],
    markers=True,
    text='RK'
)
fig_player_rank.update_traces(textposition="bottom center")
fig_player_rank.update_layout(
    font=dict(size=15),
    yaxis_title='Final Rank'
)

fig_player_rank.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
fig_player_rank.update_yaxes(autorange='reversed')
st.plotly_chart(fig_player_rank, use_container_width=True)
# --- END Final Ranking Line Graph ---

# --- Points Scored Averages and Points Against Averages ---
df_avg_points_year = df.query(
    "Year == @year_selector"
)

final_left, final_right = st.columns(2)

fig_points_for_avg = px.line(
    df_selection,
    x='Year',
    y='PF',
    markers=True,
    title='Points Scored Per Season and League Average',
    color_discrete_sequence=['#5DADE2']
)
fig_points_for_avg.add_scatter(
    x=df_avg_points_year['Year'],
    y=df_avg_points_year.groupby('Year')['PF'].transform('mean'),
    mode='lines+markers',
    name='League Avg'
)
fig_points_for_avg.update_layout(font=dict(size=15))

fig_points_ag_avg = px.line(
    df_selection,
    x='Year',
    y='PA',
    markers=True,
    title='Points Against Per Season and League Average',
    color_discrete_sequence=['#F4D03F']
)
fig_points_ag_avg.add_scatter(
    x=df_avg_points_year['Year'],
    y=df_avg_points_year.groupby('Year')['PA'].transform('mean'),
    mode='lines+markers',
    name='League Avg'
)
fig_points_ag_avg.update_layout(font=dict(size=15))

with final_left:
    st.plotly_chart(fig_points_for_avg)
with final_right:
    st.plotly_chart(fig_points_ag_avg)
st.markdown("---")
# --- END Points Scored Averages and Points Against Averages ---

# --- Chart of Seasonal Data ---
df_selection = df_selection.rename({
    'PF/G': 'PPG',
    'PA/G': 'PAG',
    'RK': 'Rank'
}, axis=1)
df_selection = df_selection.sort_values(by='Year', ascending=False)
table = st.container()

with table:
    st.subheader('Seasonal Data History')
    fig_table = go.Figure(data=go.Table(
        columnwidth=[1, 1, 4, 1, 1, 2, 2, 1, 1, 1],
        header=dict(values=list(df_selection[['Year', 'Rank', 'Team', 'W', 'L', 'PF', 'PA',
                                                                              'PPG', 'PAG', 'Moves']].columns),
                    fill_color='#b185db',
                    align='center',
                    line_color='darkslategray',
                    height=30,
                    font=dict(color='white', size=20)),
        cells=dict(values=[df_selection.Year, df_selection.Rank, df_selection.Team,
                           df_selection.W, df_selection.L, df_selection.PF, df_selection.PA, df_selection.PPG,
                           df_selection.PAG, df_selection.Moves],
                   line_color='darkslategray',
                   fill_color='white',
                   align='center',
                   height=30,
                   font_size=18)))
    # fig_table.update_layout(margin=dict(l=5, r=5, b=5, t=5))
    fig_table.update_layout(margin=dict(l=5, r=5, b=5, t=5), width=1400)
    st.write(fig_table)
# --- END Chart of Seasonal Data ---
