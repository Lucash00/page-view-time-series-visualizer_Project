import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    # Add title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('M').mean()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create a bar plot, using the year as the x-axis and month labels for grouping
    df_bar.groupby([df_bar.index.year, df_bar.index.month]).mean().unstack().plot(kind='bar', ax=ax, width=0.8)

    # Add title and labels
    ax.set_title('Average Monthly freeCodeCamp Forum Page Views')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Preparar los datos para los box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]  # Cambié %B a %b para obtener la abreviatura del mes

    # Asegúrate de que cada mes tenga datos
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df_box['month'] = pd.Categorical(df_box['month'], categories=months, ordered=True)

    # Crear subgráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))  # Crear dos subgráficos, uno al lado del otro

    # Primer box plot: Año
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, showfliers=True)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Segundo box plot: Mes
    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, 
                showfliers=True)  # Mostrar los outliers
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Guardar imagen y devolver fig
    fig.savefig('box_plot.png')
    return fig
