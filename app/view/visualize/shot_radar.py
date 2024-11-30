from io import BytesIO

from app.dal.fetch_players import get_player_shooting

import matplotlib.pyplot as plt
import numpy as np

import logging

def shot_percentage_radar(name, shot_type):
    stats = []
    values = []
    shooting = get_player_shooting(name)

    if not shooting:
        return None

    for season in shooting:
        stats.append(f"{season[0]}")
        match shot_type:
            case 1:  # Free throws
                attempts = season[6]
                made = season[5]
            case 2:  # Two-pointers
                attempts = season[2]
                made = season[1]
            case 3:  # Three-pointers
                attempts = season[4]
                made = season[3]
            case _:
                raise ValueError("Invalid shot type. Choose 1 (Free throws), 2 (Two-pointers), or 3 (Three-pointers).")
        values.append(made / attempts if attempts > 0 else 0)

    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(14, 12), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)

    for angle, value in zip(angles, values):
        ax.text(angle, value - 0.05, f'{value:.2%}', ha='center', va='bottom', fontsize=8, weight='bold', color='purple')
    
    for i, angle in enumerate(angles[:-1]):
        ax.text(angle, values[i] * 1.2, str(stats[i]) + '/' + str(int(stats[i]) + 1), color='black', ha='center', va='center', fontsize=10)

    ax.set_yticklabels([])
    ax.xaxis.set_visible(False)

    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    return img_stream