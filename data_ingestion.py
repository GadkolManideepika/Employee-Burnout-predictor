import os
import pandas as pd


def load_data(filepath: str):
    """
    Load mock communication data from CSV.
    Expected columns: employee_id, timestamp, message_text

    The caller may supply a path that is already absolute, a path relative to
    the current working directory, or a path relative to this module. We
    attempt to read the file in that order to make the function resilient to
    different invocation patterns.
    """
    # first try the path as given (cwd relative or absolute)
    if os.path.exists(filepath):
        candidate = filepath
    else:
        # otherwise, try joining with the backend directory
        base_dir = os.path.dirname(__file__)
        candidate = os.path.join(base_dir, filepath)
        if not os.path.exists(candidate):
            # still missing; also try removing any leading "backend/" prefix that
            # might have been added by callers who pass a package-style path
            stripped = filepath.split(os.sep)
            if stripped and stripped[0].lower() == os.path.basename(base_dir).lower():
                candidate = os.path.join(base_dir, *stripped[1:])
    try:
        data = pd.read_csv(candidate)
        required_cols = {"employee_id", "timestamp", "message_text"}
        if not required_cols.issubset(data.columns):
            raise ValueError(f"CSV must contain columns: {required_cols}")
        return data.to_dict(orient="records")
    except Exception as e:
        # print to stderr so the Flask log will capture it
        print(f"Error loading data from {candidate}: {e}")
        return []
