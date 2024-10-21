import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import pandas as pd
import matplotlib
import glob


def parse_areas(name):
    for elem in name.split('_'):
        if 'areas' in elem:
            n_areas = int(elem[-1])
            return n_areas

def parse_sparsity(name):
    for elem in name.split('_'):
        if 'sparsity' in elem:
            sparsity = float(elem.split('-')[-1])
            return sparsity

def get_data(directory, threshold):
    files = glob.glob(f'{directory}/*_lossThreshold-{threshold}*.csv')
    df = pd.DataFrame(columns=['Test accuracy', 'Areas', 'Algorithm'])
    for f in files:
        areas = parse_areas(f)
        sparsity = parse_sparsity(f)
        acc = pd.read_csv(f).iloc[0].mean()
        df = df._append({'Test accuracy': acc, 'Areas': areas, 'Sparsity': sparsity}, ignore_index=True)
    return df

if __name__ == '__main__':

    output_directory = 'charts/test'
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    matplotlib.rcParams.update({'axes.titlesize': 30})
    matplotlib.rcParams.update({'axes.labelsize': 30})
    matplotlib.rcParams.update({'xtick.labelsize': 25})
    matplotlib.rcParams.update({'ytick.labelsize': 25})
    plt.rcParams.update({"text.usetex": True})
    plt.rc('text.latex', preamble=r'\usepackage{amsmath,amssymb,amsfonts}')

    data_self_fl = {}

    for th in [20, 40, 80]:
        d = get_data(f'data-test', th)
        data_self_fl[th] = d

    for th in data_self_fl.keys():
        plt.figure(figsize=(12, 8))
        data_comparison = data_self_fl[th]
        # sns.color_palette('viridis', as_cmap=True)
        # sns.set_palette('viridis')
        palette = ['#440154', '#31688e', '#35b779', '#fde725']
        ax = sns.boxplot(data=data_comparison, x='Areas', y='Test accuracy', hue='Sparsity', palette=palette)
        sns.move_legend(ax, 'lower left')
        plt.title(f'$ \sigma = {th}$')
        plt.ylabel('$Accuracy - Test$')
        plt.ylim(0, 1)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)
        plt.savefig(f'{output_directory}/test-accuracy-comparison-threshold-{th}.0.pdf', dpi=500)
        plt.close()
