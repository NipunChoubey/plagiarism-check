import os
import numpy as np
import pandas as pd

ROOT_PATH = 
CSV_PATH = r"similarity_results.csv"

def getSimilarity(file1, file2):
    
    file1_set = set(open(file1).readlines())
    file2_set = set(open(file2).readlines())
    
    N1 = len(file1_set)
    N2 = len(file2_set)
    
    set_diff12 = file1_set.difference(file2_set)
    set_diff21 = file2_set.difference(file1_set)

    overlap1 = (N1 - len(set_diff12))/N1
    overlap2 = (N2 - len(set_diff21))/N2
    
    return (len(file1_set.intersection(file2_set)), round(overlap1*100, 2), round(overlap2*100, 2))

student_records = {}
multiple_py_found = {}
no_py_found = []

# listing all files
for level1_item in os.listdir(ROOT_PATH):
    if os.path.isdir(os.path.join(ROOT_PATH, level1_item)):
        level2_items = os.listdir(os.path.join(ROOT_PATH, level1_item))
        count = len([f for f in level2_items if f[-3:]==".py"])

        if count > 1:
            multiple_py_found[level1_item] = count
        elif count == 0:
            no_py_found.append(level1_item)
        else:
            student_records[level1_item] = [f for f in level2_items if f[-3:]==".py"][0]


df = pd.DataFrame(columns=["Student1", "Student2", "Count", "SimilarityS1", "SimilarityS2"])

# checking similarity
for i in student_records:
    for j in student_records:
        if i==j:
            continue
        elif np.sum((df["Student2"]==i) & (df["Student1"]==j)): 
            continue
        else:
            file1 = os.path.join(ROOT_PATH, i, student_records[i])
            file2 = os.path.join(ROOT_PATH, j, student_records[j])
            similarity = getSimilarity(file1, file2)
            df = df.append({
                "Student1": i,
                "Student2": j,
                "Count": similarity[0],
                "SimilarityS1": similarity[1],
                "SimilarityS2": similarity[2],
            }, ignore_index=True)


df.sort_values(by=["Count"], ascending=False, inplace=True)
df.to_csv(CSV_PATH, index=False)

print("\n\nStudents with no files: ", no_py_found)
print("\n\nStudents with multiple files: ", multiple_py_found)
print("\n\nStudents with single file: ", list(student_records.keys()))
print("\n\nKindly see results in %s"%(CSV_PATH))