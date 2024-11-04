import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_onetime_distribution(data):
        grouped_df = data.groupby('onetime')['Expense'].sum().reset_index()
        grouped_df['onetime_label'] = grouped_df['onetime'].map({0: 'Regular', 1: 'One-time'})
        
        fig = px.pie(
            grouped_df,
            values='Expense',
            names='onetime_label',
            title='One-time vs Regular Expenses',
            color='onetime_label',
            color_discrete_map={
                'Regular': '#76a5af',
                'One-time': '#f5a399'
            }
        )
        
        fig.update_traces(
            textinfo='percent+label',
            hovertemplate='<b>Type:</b> %{label}<br><b>Expense:</b> ¥%{value:,.0f}',
            marker=dict(line=dict(color='#333333', width=1))
        )
        
        fig.update_layout(
            showlegend=True,
            legend=dict(title="Expense Type"),
            margin=dict(l=10, r=10, b=10, t=40),
            height=400
        )
        
        return fig

def plot_category_distribution(data):
    # Group by NewCategory and sum expenses
    category_data = data.groupby('NewCategory')['Expense'].sum().reset_index()
    
    fig = px.pie(
        category_data,
        values='Expense',
        names='NewCategory',
        title='Expense Distribution by Category',
        color='NewCategory',
        color_discrete_map={
            'Housing and Utilities': '#e2c596',
            'Food': '#99b98b',
            'Transportation': '#cda180',
            'Fitness': '#d6a7c3',
            'Souvenirs/Gifts/Treats': '#b4aea8',
            'Household and Clothing': '#e7d8c4',
            'Entertainment and Books': '#909eb3',
            'Miscellaneous': '#b3b3cc',
            'Personal Care and Medicines': '#b09fcb',
        }
    )
    
    fig.update_traces(
        textinfo='percent+label',
        texttemplate='%{label}<br>%{percent:.1%}',
        hovertemplate='<b>Category:</b> %{label}<br><b>Expense:</b> ¥%{value:,.0f}',
        marker=dict(line=dict(color='white', width=1.5))
    )
    
    fig.update_layout(
        font=dict(family='Garamond', size=12, color='white'),  # Set font style
        showlegend=False,
        margin=dict(l=10, r=10, b=10, t=40),
        height=400
    )
    
    return fig

def plot_sunburst(data):
    fig  = px.sunburst(data, path=['NewCategory', 'category'], values='Expense',
                    color='NewCategory',  # Color by the "NewCategory" column
                    title='Expense Distribution',
                    color_discrete_map={
            'Housing and Utilities': '#e2c596',  # Softer goldenrod
            'Food': '#99b98b',  # Softer olive green
            'Transportation': '#cda180',  # Soft caramel
            'Fitness': '#d6a7c3',  # Subtle mauve pink
            'Souvenirs/Gifts/Treats': '#b4aea8',  # Warm gray
            'Household and Clothing': '#e7d8c4',  # Very light taupe
            'Entertainment and Books': '#909eb3',  # Muted gray-blue
            'Miscellaneous': '#b3b3cc',  # Soft slate blue
            'Personal Care and Medicines': '#b09fcb',  # Muted lavender
        })

    # Update layout for aesthetics and size
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=40),  # Adjust margins for better visualization
        font=dict(family='Garamond', size=12, color='white'),  # Set font style
        title=dict(font=dict(size=20)),  # Set title font size
        coloraxis=dict(colorbar=dict(title='Expense Category')),  # Set color axis title
        width=400,  # Set the width in pixels
        height=400,  # Set the height in pixels
    )

    fig.update_traces(textinfo="label+percent parent")
    fig.update_traces(hovertemplate='<b>Category:</b> %{label}<br><b>Expense:</b> ¥ %{value:,.0f}',
                        marker=dict(line=dict(color='white', width=1.5)) )
    return fig

def plot_cumulative_expense(data, threshold=50000):
    # Prepare data
    data = data.copy()
    data['Date'] = pd.to_datetime(data['Date'])
    data['Cumulative Expense'] = data['Expense'].cumsum()
    
    
    # Plot cumulative expense over time
    fig = px.line(
        data,
        x='Date',
        y='Cumulative Expense',
        title='Cumulative Expenses Over Time (¥)',
        labels={'Cumulative Expense': 'Cumulative Expense (¥)', 'Date': 'Date'},
        color_discrete_sequence=['#76a5af']
    )

    # Identify sudden increase days
    # sudden_increase_days = data[data['Expense'] > threshold]

    # # Add vertical and horizontal dashed lines for sudden increases
    # for _, row in sudden_increase_days.iterrows():
    #     fig.add_shape(
    #         go.layout.Shape(
    #             type="line",
    #             x0=row['Date'],
    #             x1=row['Date'],
    #             y0=0,
    #             y1=row['Cumulative Expense'],
    #             line=dict(color="red", dash="dot")
    #         )
    #     )
    #     fig.add_shape(
    #         go.layout.Shape(
    #             type="line",
    #             x0=data['Date'].min(),
    #             x1=row['Date'],
    #             y0=row['Cumulative Expense'],
    #             y1=row['Cumulative Expense'],
    #             line=dict(color="red", dash="dot")
    #         )
    #     )

    fig.update_layout(
        width=600,
        height=400,
        title=dict(font=dict(size=20), x=0.5),
        yaxis=dict(tickformat=',.0f', title='Cumulative Expense (¥)'),
        font=dict(family='Garamond', size=14, color='black'),
    )
    return fig

def plot_expense_timeseries(data, dma_window=10):
    # Prepare data
    data = data.copy()
    data['Date'] = pd.to_datetime(data['Date'])
    dma_label = f"{dma_window}DMA"
    data[dma_label] = data['Expense'].rolling(window=dma_window).mean()
    
    # Plot daily expenses and moving average
    fig = px.line(
        data,
        x='Date',
        y='Expense',
        title='Expenses Over Time',
        labels={'Expense': "Expenses (in ¥)", 'Date': 'Date'},
        color_discrete_sequence=['#76a5af']
    )

    # Add moving average line
    fig.add_trace(
        go.Scatter(
            x=data['Date'],
            y=data[dma_label],
            mode='lines',
            name=dma_label,
            line=dict(color='#f5a399', width=2, dash='dash')
        )
    )

    fig.update_layout(
        width=800,
        height=400,
        title=dict(font=dict(size=20), x=0.5),
        yaxis=dict(tickformat=',.0f', title='Expense (¥)'),
        font=dict(family='Garamond', size=14, color='black'),
    )

    fig.update_traces(
        hovertemplate='<b>Date:</b> %{x|%b %d, %Y}<br><b>Expense:</b> ¥ %{y:,.0f}',
        line=dict(width=2)
    )
    
    return fig
