from scipy.stats import ks_2samp


def detect_drift(
    reference_data,
    current_data,
    threshold=0.05
):

    drift_results = {}

    for column in reference_data.columns:

        if column not in current_data.columns:
            continue

        statistic, p_value = ks_2samp(
            reference_data[column],
            current_data[column]
        )

        drift_detected = (
            p_value < threshold
        )

        drift_results[column] = {
            "p_value": float(p_value),
            "drift_detected": drift_detected
        }

    return drift_results
