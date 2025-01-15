import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Muat data
combined_df = pd.read_csv("https://raw.githubusercontent.com/auliasarics/Proyek-Data-Analisis-dengan-Python/refs/heads/main/dashboard/data_air_quality.csv")

# Definisi parameter dan rentang nilai
parameter_ranges = {
    'PM2.5': 'pm25_ranges',
    'PM10': 'pm10_ranges',
    'SO2': 'so2_ranges',
    'NO2': 'no2_ranges',
    'CO': 'co_ranges',
    'O3': 'o3_ranges',
}

# Visualisasi tren kualitas udara
st.title("Tren Kualitas Udara Berdasarkan Parameter di Berbagai Stasiun Pengukuran")
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
fig.suptitle('Tren Kualitas Udara Berdasarkan Parameter di Berbagai Stasiun Pengukuran', fontsize=16)
for ax, (param, ranges) in zip(axes.flatten(), parameter_ranges.items()):
    sns.lineplot(data=combined_df, x='year', y=param, hue='station', ax=ax)
    ax.set_title(f'Tren {param} di Berbagai Stasiun')
    ax.set_xlabel('Tahun')
    ax.set_ylabel(param)
plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)

# Heatmap korelasi
weather_columns = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
air_quality_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
correlation_matrix = combined_df[weather_columns + air_quality_columns].corr()
st.title("Heatmap Korelasi antara Parameter Cuaca dan Kualitas Udara")
fig = plt.figure(figsize=(7, 5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Heatmap Korelasi antara Parameter Cuaca dan Kualitas Udara')
st.pyplot(fig)

# Perbandingan kualitas udara antar stasiun
start_year = 2015
end_year = 2017
air_quality_parameters = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
station_names = [
    'Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 
    'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'
]
st.title(f"Perbandingan Kualitas Udara Antar Stasiun ({start_year}-{end_year})")
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
fig.suptitle(f'Perbandingan Kualitas Udara Antar Stasiun ({start_year}-{end_year})', fontsize=16)
for i, parameter in enumerate(air_quality_parameters):
    row = i // 3
    col = i % 3
    axs[row, col].set_title(parameter)
    for j, station in enumerate(station_names):
        filtered_data = combined_df[
            (combined_df['year'] >= start_year) & 
            (combined_df['year'] <= end_year) & 
            (combined_df['station'] == station)
        ]
        axs[row, col].bar(station, filtered_data[parameter].mean(), label=station)
    axs[row, col].set_xlabel('Stasiun')
    axs[row, col].set_ylabel('Rata-rata Kualitas Udara')
    axs[row, col].legend()
plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)
