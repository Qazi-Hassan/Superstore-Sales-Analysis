# Import required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your cleaned dataset
df = pd.read_csv('superstore_cleaned.csv')  # replace with your actual data file

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Superstore Sales & Profit Dashboard"

# Create key figures
category_fig = px.bar(df.groupby('Category').sum(numeric_only=True).reset_index(),
                      x='Category', y=['Sales', 'Profit'],
                      barmode='group', title='Sales & Profit by Category')

sub_category_fig = px.bar(df.groupby('Sub-Category').sum(numeric_only=True).reset_index(),
                          x='Sub-Category', y='Profit',
                          color='Profit', title='Profit by Sub-Category')

region_fig = px.pie(df, names='Region', values='Profit', title='Profit Share by Region')

discount_profit_fig = px.scatter(df, x='Discount', y='Profit',
                                 color='Category',
                                 title='Impact of Discount on Profit')

monthly_sales_fig = px.line(df.groupby('Order Date').sum(numeric_only=True).reset_index(),
                            x='Order Date', y='Sales',
                            title='Monthly Sales Trend')

shipping_mode_fig = px.bar(df.groupby('Ship Mode').sum(numeric_only=True).reset_index(),
                           x='Ship Mode', y='Profit',
                           title='Profit by Shipping Mode')

segment_fig = px.pie(df, names='Segment', values='Profit', title='Profit by Customer Segment')

state_fig = px.bar(df.groupby('State').sum(numeric_only=True).reset_index().sort_values('Profit'),
                   x='Profit', y='State', orientation='h',
                   title='Profit by State')

outliers_fig = px.scatter(df[df['Profit'].abs() > 2000], x='Sales', y='Profit',
                          color='Category', size='Discount',
                          title='High Profit/Loss Orders (Outliers)')

# Define app layout
app.layout = html.Div([
    html.H1("📊 Superstore Sales & Profitability Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Dropdown(
            id='category-filter',
            options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],
            value=None,
            placeholder="Filter by Category",
            clearable=True
        ),
    ], style={'width': '40%', 'margin': 'auto', 'marginBottom': '20px'}),

    dcc.Tabs([
        dcc.Tab(label='📈 Category & Sub-Category', children=[
            dcc.Graph(figure=category_fig),
            dcc.Graph(figure=sub_category_fig),
        ]),

        dcc.Tab(label='🌍 Region & State Performance', children=[
            dcc.Graph(figure=region_fig),
            dcc.Graph(figure=state_fig),
        ]),

        dcc.Tab(label='💸 Discount & Profit Impact', children=[
            dcc.Graph(figure=discount_profit_fig),
        ]),

        dcc.Tab(label='📅 Monthly Sales Trend', children=[
            dcc.Graph(figure=monthly_sales_fig),
        ]),

        dcc.Tab(label='🚚 Shipping Mode Analysis', children=[
            dcc.Graph(figure=shipping_mode_fig),
        ]),

        dcc.Tab(label='👥 Customer Segments', children=[
            dcc.Graph(figure=segment_fig),
        ]),

        dcc.Tab(label='⚠️ Outliers & High-Value Orders', children=[
            dcc.Graph(figure=outliers_fig),
        ]),
    ])
])

# Interactivity: update graphs based on category filter
@app.callback(
    Output(component_id='discount-profit-graph', component_property='figure'),
    Input(component_id='category-filter', component_property='value')
)
def update_discount_profit(selected_category):
    if selected_category:
        filtered_df = df[df['Category'] == selected_category]
    else:
        filtered_df = df

    updated_fig = px.scatter(filtered_df, x='Discount', y='Profit',
                             color='Sub-Category',
                             title=f'Discount vs Profit ({selected_category or "All Categories"})')
    return updated_fig

# Add placeholder for updated graph
app.layout.children.insert(2, dcc.Graph(id='discount-profit-graph', figure=discount_profit_fig))

# Run app
if __name__ == '__main__':
    app.run(debug=True)
