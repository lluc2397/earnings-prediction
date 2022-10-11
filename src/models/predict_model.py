from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    classification_report,
    mean_absolute_error,
)
from statistics import mean


def calculate_bests(results_dict, X_train, y_train, y_test):
    best_calculation = [
        "score",
        "r2_score",
        "mean_squared_error",
        "mean_absolute_error",
    ]

    for key, value in results_dict.items():
        model = results_dict[key]["model"]
        pred = results_dict[key]["pred"]
        results_dict[key] = {
            "score": model.score(X_train, y_train),  # Closer to 1 is better
            "r2_score": r2_score(y_test, pred),  # Closer to 1 is better
            "mean_squared_error": mean_squared_error(y_test, pred),  # Lower is better
            "mean_absolute_error": mean_absolute_error(y_test, pred),  # Lower is better
        }

    best_score = []
    best_r2 = []
    best_mse = []
    best_mae = []
    for key, value in results_dict.items():
        score = results_dict[key]["score"]
        r2 = results_dict[key]["r2_score"]
        mse = results_dict[key]["mean_squared_error"]
        mae = results_dict[key]["mean_absolute_error"]
        best_score.append(score)
        best_r2.append(r2)
        best_mse.append(mse)
        best_mae.append(mae)

    best_score.sort(reverse=True)
    best_r2.sort(reverse=True)
    best_mse.sort()
    best_mae.sort()

    for key, value in results_dict.items():
        score = results_dict[key]["score"]
        r2 = results_dict[key]["r2_score"]
        mse = results_dict[key]["mean_squared_error"]
        mae = results_dict[key]["mean_absolute_error"]

        best_score_index = best_score.index(score) + 1
        best_r2_index = best_r2.index(r2) + 1
        best_mse_index = best_mse.index(mse) + 1
        best_mae_index = best_mae.index(mae) + 1
        results_dict[key]["score_position"] = best_score_index
        results_dict[key]["r2_score_position"] = best_r2_index
        results_dict[key]["mean_squared_error_position"] = best_mse_index
        results_dict[key]["mean_absolute_error_position"] = best_mae_index
        results_dict[key]["average_position"] = mean(
            [best_score_index, best_r2_index, best_mse_index, best_mae_index]
        )
    return results_dict
