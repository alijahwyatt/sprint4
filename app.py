# %% [markdown]
# ### Sprint #4: Dashboard V0
# 
# DS4003 | Spring 2024
# 
# 
# **Objectives**
# 
# The objective of this sprint id to begin the dashboard build.
# 
# **Instructions**
# 
# Start coding your dashboard. You may begin with whatever elements you prefer. 
# The sprint deliverable must include at least one graph/data table with two UI components (radio button, slider, etc). 
# The graph does not need to be in final form, but needs to have all the basic elements and styling in place.
# 
# **Deliverables**
# 
# URL to Github Repo with Render URL in the readme
# 
# **Submission**
# 
# Submit your assignment on Canvas
# 

# %%
#import dependencies
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# %%
#read in df
df = pd.read_csv("data.csv")
df.head()

# %%
#load CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# %%
#initialize app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# %%
#print min and max car years for layout 
min_year = df['model_year'].min()
max_year = df['model_year'].max()

#round down the minimum year to the nearest decade
rounded_min_year = (min_year // 10) * 10

#round up the maximum year to the nearest decade and then add 5
rounded_max_year = (((max_year + 5) // 10) * 10) + 5

# %%

#make sure brands are sorted alphabetically case insensitive and default brand is first brand
sorted_brands = sorted(df['brand'].unique(), key=lambda x: x.lower())
first_brand = sorted_brands[0]



#create app
app.layout = html.Div([
 #add title and description
    html.H2("Average Price per Brand by Year"),
    html.H5('The app currently displays a graph that looks at the average price of all the models for a specific brand through a range of selected years. A year range slider, and a dropdown is included and the graph is completely functional and has all the basic elements and styling in place, though some changes might be made.'),
    html.Div([
        html.Div([
            # create dropdown menu to select brand
            html.Label('Select Brand'),
            dcc.Dropdown(
                id='brand-dropdown',
                options=[
            {'label': category, 'value': category} for category in sorted_brands
        ],
        value=first_brand
            ),
        ],
         #changing format
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'}),
        
        html.Div([
            # create slider to select year
            dcc.RangeSlider(
                #set min to rounded min year to make slider look cleaner
               min=rounded_min_year,
                #set max to rounded max year to make slider look cleaner
               max=rounded_max_year,
               step=None,
               #initialize year silder 
               value=[min_year, min_year],
               id='year-range-slider',
               #setting marks in increments of 5
               marks={str(year): str(year) for year in range(rounded_min_year, rounded_max_year+ 1, 5)}
            ) , 
        ],
        #changing format
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'})
        ]),
    # Line graph to compare model year prices of a specific brand
    dcc.Graph(
        id='brand-price-graph',
        figure=px.bar(df,
                      x='model_year',
                      y='price',
                      color='brand'
                    )
                .update_layout(
                    title='Average Price by Model Year for Selected Brand',
                    xaxis_title='Model Year',
                    yaxis_title='Average Price'
                )
        )


])

#define callbacks
@app.callback(
    Output('brand-price-graph', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
#create update graph function
def update_graph(selected_brand, year_range):
    #make sure selected_brand is always a list
    if isinstance(selected_brand, str):
        selected_brand = [selected_brand]

    # create filtered df based on selected brand and years
    filtered_df = df[(df['brand'].isin(selected_brand)) & df['model_year'].between(year_range[0], year_range[1])]

    # Calculate the average price for each model year within the filtered data
    avg_price_by_year = filtered_df.groupby('model_year')['price'].mean().reset_index()

    # making graph
    fig = px.bar(avg_price_by_year,
                       #set x axis to year, y axis to price, color to brand
                       x='model_year', 
                       y='price', 
                       title='Price by Model Year',
                       color='model_year', 
                       )
    #create titles 
    fig.update_layout(
                    title='Price by Model Year',
                    xaxis_title='Year',
                    yaxis_title='Price',
                )
    #calculate the max price for the selected brand to use as my y axis scaling
    max_price_brand = filtered_df['price'].max()

    #set a fixed range for the y-axis based on the maximum price of the selected brand
    fig.update_yaxes(range=[0, max_price_brand]) 
    #set fixed range for x axis so graph doesn't get smaller
    fig.update_xaxes(range=[df['model_year'].min(), df['model_year'].max()])

    return fig  

# %%
#run app
if __name__ == '__main__':
    app.run_server(jupyter_mode='tab', debug=True, port=8051)


