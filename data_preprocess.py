import shutil
import os
import pandas as pd


# Clean the labels
LABEL_PATH = 'Data_Entry_2017.csv'

# Read csv file into dataframe
df = pd.read_csv(LABEL_PATH, dtype=str)

# Rename columns to 'labels', 'index' and 'image'
df = df.rename(columns={'Image Index': 'image', 'Finding Labels': 'label'})

df = df[['image', 'label']]
df['label'] = df['label'].str.replace('|', '#')
df = df[~df['label'].str.contains('#')]

# Downsample so that we only have 1000 rows of images with label of "No finding"

rowsNoFinding = df[df['label'] == "No Finding"].sample(5000, random_state=123)
rowsInfilt = df[df['label'] == "Infiltration"].sample(5000, random_state=123)
rowsRest = df[~df['label'].isin(['No Finding', 'Infiltration'])]


# Combine dataframes and shuffle randomly
df_downsampled = rowsRest.append(
    [rowsNoFinding, rowsInfilt]).sample(frac=1, random_state=123)

df_downsampled['label'].value_counts()

df = df_downsampled


print(df['label'].value_counts())

df.to_csv('data_labels_medium.csv', index=False)

df = pd.read_csv('data_labels_medium.csv', dtype=str)

print(df['label'].value_counts())

filenames = df['image'].tolist()

print(len(filenames))


subfolders = ['01', '02', '03', '04', '05',
              '06', '07', '08', '09', '10', '11', '12']


# Move all images that has label from cleaned dataframe from original dataset folder to new folder
def createMediumDataset():
    for i in subfolders:
        originalPath = 'nih-xray/images_0' + i + '/images/'
        for fn in filenames:
            if os.path.isfile(originalPath + fn):
                print('Yes')
                shutil.move(originalPath + fn, "dataset-medium/images/" + fn)


# createMediumDataset()
