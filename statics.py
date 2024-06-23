import pandas as pd
import streamlit as st

data=pd.read_csv("ipl_data/deliveries.csv")
#print(data.columns)

df=data[['match_id','batter','bowler','batsman_runs','extra_runs','extras_type','total_runs','is_wicket','player_dismissed','dismissal_kind', 'fielder']]
#print(df.head())

st.set_page_config("cricket statics")
st.header("Statics of player")
bowler=tuple(df.bowler.unique())
batshman=tuple(df.batter.unique())
fielder=tuple(df.fielder.unique())

players=tuple(set(bowler+batshman+fielder))
selected_player=st.selectbox("Batting team player",players)
opponent_player=st.selectbox("Bowling team player",players)

st.header(f"{selected_player} VS {opponent_player} in ipl statics")

st.subheader("Bowling Column")

df1=df[(df['batter']==selected_player)& (df['bowler']==opponent_player)]

lenth=[i for i in range(len(df1))]
df1.index=lenth

non_bowler_dismissals = ['run out', 'retired hurt', 'hit wicket', 'obstructing the field', 'retired out']
wicket_not_by_bowler = len(df1[df1['dismissal_kind'].isin(non_bowler_dismissals)])
wicket_not_taken_index=df1[df1['dismissal_kind'].isin(non_bowler_dismissals)].index
#df1.batsman_runs.mean()
#wicket=df1.is_wicket.value_counts()
#no_of_wiket=wicket[1]
no_of_match=df1.match_id.nunique()
st.write(f"No of match head to head bowling: {no_of_match}")
#w=df1['is_wicket']
wicket=df1[df1['is_wicket']==1]
no_of_wiket=len(wicket)-wicket_not_by_bowler
st.write(f"No of wickets  taken by {opponent_player}: {no_of_wiket}")
total_ball=len(df1[df1.extras_type!="wides"])
#st.write(f"Total balls  {selected_player}  faced againest {opponent_player}: {total_ball}")
no_of_over=total_ball/6
Avg_runs_per_over=df1.batsman_runs.sum()/no_of_over
st.write(f"Average runs per over: {Avg_runs_per_over:.3f}")
batsman_run=df1.batsman_runs.sum()
st.write(f"{selected_player}'s Runs : {batsman_run}")
bat_sr=batsman_run/total_ball
st.write(f"batshman strick rate : {bat_sr*100:.3f}")
extra_runs=df1.total_runs.sum()-batsman_run
st.write(f"Extra runs : {extra_runs}")

total_wicket_indices=df1['is_wicket'][df1['is_wicket']==1].index
wicket_indices=total_wicket_indices.difference(wicket_not_taken_index)
if len(wicket_indices) > 1:
    # Compute the differences between consecutive wicket indices
    balls_between_wickets = wicket_indices.to_series().diff().dropna()
    
    # Calculate the average balls required to take a wicket
    avg_ball_required_to_take_wicket = balls_between_wickets.mean()
    
    # Calculate the standard deviation of balls between wickets
    std_ball_required_to_take_wicket = balls_between_wickets.std()
    
    st.write(f"Avg ball required to take a wicket : {avg_ball_required_to_take_wicket:.0f}")

elif len(wicket_indices) == 1:
    # If there is only one wicket, we cannot calculate the difference, mean, or standard deviation
    st.write("Only one wicket taken")
else:
    # If there are no wickets
    st.write("No wickets taken.")


st.subheader("Fielding Column")
df2=df[(df.player_dismissed==selected_player)&(df.fielder==opponent_player)]
no_of_time_out_by_field=len(df2)
st.write(f"No .of time out by fielding : {no_of_time_out_by_field}")








