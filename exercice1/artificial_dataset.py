import pandas as pd
import numpy as np
from time import time

def generate_dataset(*, num_datapoints: int = 300):
    r"""Generate a numerical dataset of 300 datapoints and 6 columns.
        The first column contains only integers.
        The second column contains only floats.
        The third column has a mean close to 2.5.
        The fourth column is positively correlated.
        The fifth column is negatively correlated.
        The sixth one has a correlaction close to 0.
    """

    data = {}

    # Column 1: Integers
    data['col1'] = np.random.randint(1, 10, num_datapoints)

    # Column 2: Floats
    data['col2'] = np.random.uniform(0, 5, num_datapoints)

    # Column 3: Mean close to 2.5
    data['col3'] = np.random.normal(loc=2.5, scale=1, size=num_datapoints)

    # Column 4: Positively correlated
    data['col4'] = np.random.normal(loc=5, scale=2, size=num_datapoints) + 0.5 * data['col1']

    # Column 5: Negatively correlated
    data['col5'] = np.random.normal(loc=5, scale=2, size=num_datapoints) - 0.5 * data['col2']

    # Column 6: Correlation close to 0
    data['col6'] = np.random.normal(loc=5, scale=2, size=num_datapoints) + np.random.normal(loc=0, scale=2, size=num_datapoints)

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv('artificial_dataset.csv', index=False)

if __name__ == '__main__':
    print("[EX1] Generating dataset...")
    start = time()
    generate_dataset()
    print(f"[EX1] Done - {(time() - start):0.4f}s")
