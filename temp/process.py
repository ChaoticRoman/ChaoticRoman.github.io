import csv
import os
from tkinter import Tk
from tkinter import filedialog

import matplotlib.pyplot as plt

COLUMNS_PER_SAMPLE = 10  # Number of samples in the CSV (each sample has 10 columns)

X_DATA = "Strain (%)"
X_DATA_INDEX = 2   # Strain (%) is in the 3rd column of each sample

Y_DATA = "Stress (MPa)"
Y_DATA_INDEX = 1  # Stress (MPa) is in the 2nd column of each sample


def csv_to_json(csv_file_path):
    # Open the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Read the header rows
        titles = next(reader)  # First row with sample titles
        headers = next(reader)  # Second row with column names
        units = next(reader)  # Third row with units
        
        # Prepare the output list
        output = []
        
        num_samples = len(titles) // COLUMNS_PER_SAMPLE
        
        # Initialize lists to store data for each sample
        samples = [{"title": f"Příloha zkušebního protokolu – tahový diagram vzorku č.: {titles[i*10].strip()}",
                    X_DATA: [],
                    Y_DATA: []} for i in range(num_samples)]
        
        # Iterate over the remaining rows (data rows)
        for row in reader:
            for i in range(num_samples):
                # Extract Strain and Stress for each sample
                strain = row[i * COLUMNS_PER_SAMPLE + X_DATA_INDEX]
                stress = row[i * COLUMNS_PER_SAMPLE + Y_DATA_INDEX]
                
                # Append the data to the corresponding sample
                if strain and stress:  # Ensure the values are not empty
                    samples[i][X_DATA].append(float(strain))
                    samples[i][Y_DATA].append(float(stress))
        
        return samples


def plot(json_data, directory):
    for i, sample in enumerate(json_data):
        plt.figure(figsize=[12, 9])
        plt.plot(sample[X_DATA], sample[Y_DATA])
        plt.title(sample["title"])
        plt.xlabel(X_DATA)
        plt.ylabel(Y_DATA)
        plt.grid()
        plt.savefig(os.path.join(directory, f"{i}.svg"), format="svg")
        plt.savefig(os.path.join(directory, f"{i}.png"), format="png")


def process(filename):
    directory = os.path.dirname(file_path)
    plot(csv_to_json(filename), directory)


if __name__ == "__main__":
    # Hide the root window
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Select a file")

    if file_path:
        process(file_path)
