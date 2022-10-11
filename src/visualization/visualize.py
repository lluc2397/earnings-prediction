import numpy as np
import matplotlib.pyplot as plt


SIZE_PLOT = (15, 9)


def best_and_average_plot(results_dict):
    X = np.arange(len(results_dict))
    ax = plt.subplot(111)
    fig = plt.gcf()
    fig.set_size_inches(*SIZE_PLOT)
    # fig.savefig('test2png.png', dpi=100)
    ax.bar(
        X,
        [results_dict[key]["score_position"] for key in results_dict.keys()],
        width=0.2,
        color="b",
        align="center",
    )
    ax.bar(
        X - 0.2,
        [results_dict[key]["r2_score_position"] for key in results_dict.keys()],
        width=0.2,
        color="g",
        align="center",
    )
    ax.bar(
        X + 0.2,
        [
            results_dict[key]["mean_squared_error_position"]
            for key in results_dict.keys()
        ],
        width=0.2,
        color="r",
        align="center",
    )
    ax.bar(
        X + 0.6,
        [
            results_dict[key]["mean_absolute_error_position"]
            for key in results_dict.keys()
        ],
        width=0.2,
        color="m",
        align="center",
    )
    ax.bar(
        X + 0.4,
        [results_dict[key]["average_position"] for key in results_dict.keys()],
        width=0.2,
        color="y",
        align="center",
    )
    ax.legend(("best score", "best r2 score", "best mse", "best mae", "average"))
    plt.xticks(X, results_dict.keys())
    plt.title("Positions lower is better", fontsize=17)
    plt.show()


def r2_and_score_plot(results_dict):
    X = np.arange(len(results_dict))
    ax = plt.subplot(111)
    fig = plt.gcf()
    fig.set_size_inches(*SIZE_PLOT)
    # fig.savefig('test2png.png', dpi=100)
    ax.bar(
        X,
        [results_dict[key]["score"] for key in results_dict.keys()],
        width=0.2,
        color="b",
        align="center",
    )
    ax.bar(
        X - 0.2,
        [results_dict[key]["r2_score"] for key in results_dict.keys()],
        width=0.2,
        color="g",
        align="center",
    )
    ax.legend(("best score", "best r2 score"))
    plt.xticks(X, results_dict.keys())
    plt.title("Accuracy score and r2 score closer to 1 is better", fontsize=17)
    plt.show()


def mse_best_comp_plot(results_dict):
    X = np.arange(len(results_dict))
    ax = plt.subplot(111)
    fig = plt.gcf()
    fig.set_size_inches(*SIZE_PLOT)
    # fig.savefig('test2png.png', dpi=100)
    ax.bar(
        X,
        [results_dict[key]["mean_squared_error"] for key in results_dict.keys()],
        width=0.2,
        color="b",
        align="center",
    )
    ax.legend(("best mse",))
    plt.xticks(X, results_dict.keys())
    plt.title("mean_squared_error lower is better", fontsize=17)
    plt.show()


def mae_best_comp_plot(results_dict):
    X = np.arange(len(results_dict))
    ax = plt.subplot(111)
    fig = plt.gcf()
    fig.set_size_inches(*SIZE_PLOT)
    # fig.savefig('test2png.png', dpi=100)
    ax.bar(
        X,
        [results_dict[key]["mean_absolute_error"] for key in results_dict.keys()],
        width=0.2,
        color="r",
        align="center",
    )
    ax.legend(("best mae",))
    plt.xticks(X, results_dict.keys())
    plt.title("mean_absolute_error lower is better", fontsize=17)
    plt.show()


def plot_charts(results_dict):
    best_and_average_plot(results_dict)
    r2_and_score_plot(results_dict)
    mse_best_comp_plot(results_dict)
    mae_best_comp_plot(results_dict)
