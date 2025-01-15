import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data (asumsi kamu sudah memiliki DataFrame combined_df yang berisi data kualitas udara)
combined_df = pd.read_csv('data_air_quality.csv')

# Ranges untuk parameter kualitas udara (contoh, kamu bisa sesuaikan)
pm25_ranges = [0, 10, 20, 30, 40]
pm10_ranges = [0, 20, 40, 60, 80]
so2_ranges = [0, 50, 100, 150, 200]
no2_ranges = [0, 50, 100, 150, 200]
co_ranges = [0, 1, 2, 3, 4]
o3_ranges = [0, 20, 40, 60, 80]

parameter_ranges = {
    'PM2.5': pm25_ranges,
    'PM10': pm10_ranges,
    'SO2': so2_ranges,
    'NO2': no2_ranges,
    'CO': co_ranges,
    'O3': o3_ranges,
}

# Streamlit title
st.title("Dashboard Kualitas Udara")

# Visualisasi Tren Kualitas Udara Berdasarkan Parameter
st.header('Tren Kualitas Udara Berdasarkan Parameter di Berbagai Stasiun Pengukuran')

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
fig.suptitle('Tren Kualitas Udara Berdasarkan Parameter di Berbagai Stasiun Pengukuran', fontsize=16)

for ax, (param, ranges) in zip(axes.flatten(), parameter_ranges.items()):
    sns.lineplot(data=combined_df, x='year', y=param, hue='station', ax=ax)
    ax.set_title(f'Tren {param} di Berbagai Stasiun')
    ax.set_xlabel('Tahun')
    ax.set_ylabel(param)

plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)  # Pastikan fig diberikan sebagai argumen

# Visualisasi Heatmap Korelasi antara Cuaca dan Kualitas Udara
st.header('Heatmap Korelasi antara Cuaca dan Kualitas Udara')

weather_columns = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
air_quality_columns = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

correlation_matrix = combined_df[weather_columns + air_quality_columns].corr()

fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
plt.title('Heatmap Korelasi antara Parameter Cuaca dan Kualitas Udara')
st.pyplot(fig)  # Pastikan fig diberikan sebagai argumen

# Perbandingan Kualitas Udara Antar Stasiun
st.header('Perbandingan Kualitas Udara Antar Stasiun (2015-2017)')

start_year = 2015
end_year = 2017

air_quality_parameters = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

station_names = [
    'Aotizhongxin', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan', 'Gucheng', 
    'Huairou', 'Nongzhanguan', 'Shunyi', 'Tiantan', 'Wanliu', 'Wanshouxigong'
]

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
fig.suptitle(f'Perbandingan Kualitas Udara Antar Stasiun ({start_year}-{end_year})', fontsize=16)

for i, parameter in enumerate(air_quality_parameters):
    row = i // 3
    col = i % 3

    axs[row, col].set_title(parameter)
    
    for j, station_name in enumerate(station_names):
        filtered_data = combined_df[(combined_df['year'] >= start_year) & (combined_df['year'] <= end_year) & (combined_df['station'] == station_name)]
        axs[row, col].bar(station_name, filtered_data[parameter].mean(), label=station_name)

    axs[row, col].set_xlabel('Stasiun')
    axs[row, col].set_ylabel('Rata-rata Kualitas Udara')
    axs[row, col].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])
st.pyplot(fig)  # Pastikan fig diberikan sebagai argumen


