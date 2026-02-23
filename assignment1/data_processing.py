import pandas as pd
import pdb


class Data:
    def __init__(self, dir):
        self.df = pd.read_csv(dir)

        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['year'] = self.df['date'].dt.year
        self.df['month'] = self.df['date'].dt.month
        self.df['day'] = self.df['date'].dt.day

        self.df['max_temperature'] = pd.to_numeric(self.df['max_temperature'])
        self.df['min_temperature'] = pd.to_numeric(self.df['min_temperature'])

    def keep_last_n_years(self, n):
        max_year = int(self.df['year'].max())
        min_year = max_year - (n-1)
        df10 = self.df[(self.df["year"] >= min_year) & (self.df["year"] <= max_year)]
        years = list(range(min_year, max_year+1))
        return df10, years

    def get_monthly_extreme(self, df10):
        monthly_max = df10.groupby(['year', 'month'])['max_temperature'].max()
        monthly_min = df10.groupby(['year', 'month'])['min_temperature'].min()
        return monthly_max, monthly_min


if __name__ == '__main__':
    data = Data('temperature_daily.csv')
    df10, years = data.keep_last_n_years(10)
    monthly_max, monthly_min = data.get_monthly_extreme(df10)
    pdb.set_trace()
