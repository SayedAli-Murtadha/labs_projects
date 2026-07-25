def skew_calc(df):
    """
    Diagnoses skewness for every numeric column in a DataFrame and recommends a transformation based on the column's skewness and
    minimum value. Binary, encoded, and ID columns are excluded, since skewness isn't a meaningful for them.
    It returns a DataFrame with the following columns:
    Feature, Skewness, Degree, Direction, Recommended Transformation
    """
    import pandas as pd
    import numpy as np

    results = []

    for col in df.select_dtypes(include=[np.number]).columns:

        if df[col].nunique() <= 2:
            continue

        skew_val = df[col].skew()

        # Classify degree and direction
        if skew_val < -1:
            degree = "Highly Skewed"
            direction = "Negative"
        elif skew_val < -0.5:
            degree = "Moderately Skewed"
            direction = "Negative"
        elif skew_val <= 0.5:
            degree = "Approximately Symmetric"
            direction = "Negative" if skew_val < 0 else "Positive"
        elif skew_val <= 1:
            degree = "Moderately Skewed"
            direction = "Positive"
        else:
            degree = "Highly Skewed"
            direction = "Positive"

        # Recommend transformation
        if abs(skew_val) <= 0.5:
            rec = "None needed"
        elif degree == "Highly Skewed" and direction == "Positive":
            rec = "Box-Cox or Yeo-Johnson"
        elif degree == "Moderately Skewed" and direction == "Positive":
            rec = "Box-Cox or Yeo-Johnson"
        elif degree == "Moderately Skewed" and direction == "Negative":
            rec = "Box-Cox or Yeo-Johnson"
        elif degree == "Highly Skewed" and direction == "Negative":
            rec = "Box-Cox or Yeo-Johnson"
        else:
            rec = "log(x+1) or Yeo-Johnson"

        # Refine: log(x+1) for highly positive skewed data that includes zero
        if direction == "Positive" and degree == "Highly Skewed" and df[col].min() == 0:
            rec = "log(x+1) or Yeo-Johnson"

        results.append({
            'Feature': col,
            'Skewness': round(skew_val, 6),
            'Degree': degree,
            'Direction': direction,
            'Recommended Transformation': rec
        })

    return pd.DataFrame(results)
