from io import BytesIO
import matplotlib.pyplot as plt

def create_ranking(stat_type: str, player_ranking: list) -> BytesIO:
    ranks = [i for i in range(1, 11)]  # Ranks from 1 to 10
    
    # Create lists to store player names and scores
    player_names = []
    scores = []
    
    # Iterate through player ranking
    for player in player_ranking:
        first_name, last_name = player[0], player[1]
        
        if stat_type == 'rebounds':
            score = player[2] + player[3]
        else:
            score = player[2]

        player_names.append(f'{first_name} {last_name}')
        scores.append(score)

    # Create a larger figure
    plt.figure(figsize=(30, 15))

    plt.scatter(ranks, scores, color='red')
    
    for rank, score, player in zip(ranks, scores, player_names):
        plt.text(rank, score + 0.05, f'{player} ({score})', ha='center', fontsize=12)

    plt.title(f'{stat_type.capitalize()} Rankings as Scatter Plot', fontsize=16)
    plt.xlabel('Rank', fontsize=14)
    plt.ylabel('Scores', fontsize=14)
    plt.gca().invert_xaxis()
    plt.tight_layout()

    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plt.close()
    return img_stream
