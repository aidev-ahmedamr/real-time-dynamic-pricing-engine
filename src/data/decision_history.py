import pandas as pd
from datetime import datetime
import os


HISTORY_FILE = "data/pricing_decisions.csv"


def save_decision(decision):

    record = decision.copy()

    record["timestamp"] = (
        datetime.utcnow().isoformat()
    )

    record["reasons"] = " | ".join(
        record["reasons"]
    )

    df = pd.DataFrame([record])

    if os.path.exists(HISTORY_FILE):

        df.to_csv(
            HISTORY_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        df.to_csv(
            HISTORY_FILE,
            index=False
        )
