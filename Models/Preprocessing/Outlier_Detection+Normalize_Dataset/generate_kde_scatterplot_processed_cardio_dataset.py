import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('Models/Datasets/processed_cardio_train.csv')
features = df.columns.tolist()

n_features = len(features)
nrows = (n_features // 4) + (1 if n_features % 4 != 0 else 0)
ncols = min(4, n_features)

fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 5 * nrows))

axes = axes.flatten()

for i, feature in enumerate(features):
    ax = axes[i]

    secax = ax.twinx()
    secax.scatter(df[feature], np.random.normal(loc=0.5, scale=0.1, size=df.shape[0]), alpha=0.3, color='red')
    secax.set_yticks([])

    df[feature].plot(kind='kde', ax=ax, color='blue')

    ax.set_xlabel(feature)
    ax.set_title(f'KDE and Scatter plot of {feature}')

for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig('Models/Preprocessing/Outlier_Detection+Normalize_Dataset/Features_KDE_and_Scatter_Plots.png')
plt.close(fig)
