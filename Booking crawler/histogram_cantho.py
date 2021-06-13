import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

if __name__ == "__main__":
    df = pd.read_csv("booking_api/booking_api-Can Tho.csv")

    hotel_df = df.groupby(by="hotel_id").mean()

    sns.histplot(data=hotel_df, x="class", discrete=True, color="red")
    plt.show()

    sns.histplot(data=hotel_df, x="review_score", color="green")
    plt.show()

    sns.histplot(data=hotel_df, x="review_score", y="class", discrete=True, color="blue")
    plt.show()