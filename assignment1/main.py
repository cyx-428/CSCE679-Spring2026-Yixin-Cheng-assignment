from data_processing import Data
from viz_matrix import build_matrix_figure

# ======================
# Configuration Section
# ======================
DATA_PATH = "data/temperature_daily.csv"
OUTPUT_HTML = "output/assignment1_output.html"
LAST_N_YEARS = 10
COLOR_SCALE = 'RdYlBu_r'


def main():
    data = Data(DATA_PATH)
    df10, years = data.keep_last_n_years(10)
    monthly_max, monthly_min = data.get_monthly_extreme(df10)

    fig = build_matrix_figure(df10, years, monthly_max, monthly_min, colorscale=COLOR_SCALE)
    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")
    print(f"Saved in: {OUTPUT_HTML}")


if __name__ == '__main__':
    main()
