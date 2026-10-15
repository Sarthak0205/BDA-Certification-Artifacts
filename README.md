# Big Data Analytics – Certification Hands-on Artefacts

## Overview

This repository contains practical artefacts demonstrating core Big Data technologies, distributed processing with Hadoop MapReduce, NoSQL database management using MongoDB, and space-efficient probabilistic data structures with Bloom Filters.

The hands-on work was originally conducted inside an Ubuntu/Linux Virtual Machine (VM) configured with Hadoop, YARN, and MongoDB environments. The code, datasets, and execution steps have been organized into this repository for academic review and certification submission.

---

## Artefacts

| Artefact | Technology | Purpose |
| :--- | :--- | :--- |
| **MongoDB CRUD & Aggregation** | MongoDB | Implements document insertion, querying, updates, deletions, and an aggregation pipeline on student records. |
| **Hadoop Reduce-Side Join** | Hadoop MapReduce (HDFS, YARN, Python) | Performs a distributed relational join across employee and department datasets using Hadoop Streaming. |
| **Bloom Filter** | Python 3 (`mmh3`, `bitarray`) | Implements a space-efficient probabilistic data structure for set membership testing and false-positive evaluation. |

---

## MongoDB

The MongoDB artefact (`MongoDB/mongodb_crud.js`) implements database operations on document data:

- **Database & Collection**: Uses the `collegeDB` database and `students` collection.
- **Insert Operations**:
  - `insertOne`: Inserts a single student record (`roll: 1, name: "Raj", course: "CSE", marks: 85`).
  - `insertMany`: Inserts multiple student records (`roll: 2, name: "Neha", course: "IT", marks: 90` and `roll: 3, name: "Amit", course: "CSE", marks: 75`).
- **Find Queries**:
  - `db.students.find()`: Retrieves all documents in the collection.
  - `db.students.find({ course: "CSE" })`: Filters documents belonging to the CSE department.
  - `.pretty()`: Formats document outputs for clean readability.
- **Update Operations**:
  - `updateOne`: Modifies Amit's record (`roll: 3`) by setting `marks: 80`.
  - `updateMany`: Updates all CSE students (`{ course: "CSE" }`) by setting `{ status: "Pass" }`.
- **Delete Operations**:
  - `deleteOne`: Removes the student record matching `{ roll: 2 }`.
  - `deleteMany`: Removes student records matching `{ status: "Fail" }`.
- **Aggregation Pipeline**:
  - Groups documents by course using `$group` and calculates average marks with `$avg`:
    ```javascript
    db.students.aggregate([
        {
            $group: {
                _id: "$course",
                avgMarks: { $avg: "$marks" }
            }
        }
    ])
    ```
- **Final Result**:
  - **Final observed CSE average**: **`82.5`** (calculated from Raj: 85 and Amit: 80).

---

## Reduce-Side Join

The Reduce-Side Join artefact implements a distributed join between two separate datasets using Hadoop Streaming and Python.

### Datasets
- **`emp.txt`**: Contains employee ID, employee name, and department ID (`emp_id,name,dept_id`):
  ```text
  1,Raj,10
  2,Neha,20
  3,Amit,10
  ```
- **`dept.txt`**: Contains department ID and department name (`dept_id,dept_name`):
  ```text
  10,HR
  20,Finance
  ```

### MapReduce Logic
- **`mapper.py`**: Reads incoming data from standard input, determines whether the record is an employee or department entry based on field count, and tags each record accordingly:
  - Employee records: emits `dept_id \t E,emp_id,name`
  - Department records: emits `dept_id \t D,dept_name`
- **`reducer.py`**: Reads sorted and grouped key-value pairs from standard input. It groups records by department ID (`dept_id`), buffers employee records and department names, and emits joined output records:
  ```text
  emp_id \t name \t dept_name
  ```
- **Hadoop Environment**: Executed with Hadoop MapReduce utilizing HDFS for distributed file storage and YARN for resource management.

### Expected / Output Records
```text
3	Amit	HR
1	Raj	HR
2	Neha	Finance
```
> *Note on Output Order*: Output order may vary because MapReduce processes keys in sorted/grouped order and partitions work across reducers.

---

## Bloom Filter

The Bloom Filter artefact demonstrates space-efficient probabilistic set membership testing.

### Python Implementation
- Implemented in Python using `mmh3` (MurmurHash3) and `bitarray`.
- Hash indices are calculated dynamically using `mmh3.hash(item, i) % size` across $k$ hash functions.
- Inserted items: `["apple", "banana", "grapes"]`.
- Queried items: `["apple", "banana", "mango", "orange"]`.

### Membership Testing & Results
- **Observed Results**:
  - `apple` returned `True`
  - `banana` returned `True`
  - `mango` returned `False` in the final 50-bit configuration
  - `orange` returned `False` in the final 50-bit configuration
- **Probabilistic Properties**:
  - **Zero False Negatives**: Bloom filters do not produce false negatives for correctly inserted items; an inserted item will always evaluate to `True`.
  - **False Positives**: Bloom filters may produce false positives because hash collisions can cause bit positions for an uninserted item to already be set to `1`.
- **Theoretical False-Positive Probability Experiment (`false_positive_probability.py`)**:
  - Configuration: $m = 50$ (bit array size), $k = 3$ (hash functions), $n = 3$ (inserted items).
  - Formula: $p \approx (1 - e^{-k \cdot n / m})^k$
  - **Probability**: $\approx 0.00447$
  - **Percentage**: $\approx 0.447\%$

---

## Technologies Used

- **Hadoop HDFS**
- **Hadoop MapReduce**
- **YARN**
- **Python 3**
- **MongoDB**
- **mmh3**
- **bitarray**

---

## Learning Outcomes / Skills Demonstrated

- **HDFS data handling**: Staging datasets and reading outputs in distributed storage.
- **MapReduce programming**: Designing mapper and reducer scripts for distributed data pipelines.
- **Reduce-Side Join**: Implementing multi-source data joins using tagging and reducer-side grouping.
- **NoSQL CRUD operations**: Managing collections, documents, filtered queries, updates, and removals in MongoDB.
- **MongoDB aggregation**: Constructing multi-stage aggregation pipelines for grouped analytical queries.
- **Probabilistic data structures**: Building and tuning bit-array Bloom filters for efficient membership testing.
- **Python scripting**: Developing clean, modular scripts for data processing and algorithmic verification.
- **Big Data processing concepts**: Understanding shuffle-and-sort mechanics, partition grouping, and trade-offs between precision and memory consumption.

---

## How to Run

### 1. MongoDB
Ensure the MongoDB service is running, then execute `mongodb_crud.js` using the MongoDB shell:
```bash
mongosh < MongoDB/mongodb_crud.js
```
*(Alternatively, in the legacy `mongo` shell: `mongo < MongoDB/mongodb_crud.js`)*

### 2. Bloom Filter
Install required Python dependencies:
```bash
pip3 install mmh3 bitarray
```
Run the implementation and experiment files:
```bash
# Run basic Bloom filter test (20-bit array)
python3 Bloom-Filter/bloom_filter.py

# Run tuned Bloom filter test (50-bit array)
python3 Bloom-Filter/bloom_test.py

# Run theoretical false-positive probability calculation
python3 Bloom-Filter/false_positive_probability.py
```

### 3. Reduce-Side Join
Requires a configured Hadoop environment with HDFS and YARN running.

1. Create input directory and stage datasets in HDFS:
   ```bash
   hdfs dfs -mkdir -p /join_input
   hdfs dfs -put Reduce-Side-Join/emp.txt /join_input/
   hdfs dfs -put Reduce-Side-Join/dept.txt /join_input/
   ```

2. Execute the Hadoop Streaming job:
   ```bash
   hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
     -files Reduce-Side-Join/mapper.py,Reduce-Side-Join/reducer.py \
     -input /join_input \
     -output /join_output \
     -mapper mapper.py \
     -reducer reducer.py
   ```

3. View the joined output from HDFS:
   ```bash
   hdfs dfs -cat /join_output/part-*
   ```

---

## Results

- **MongoDB**: Successfully performed document CRUD operations; the aggregation pipeline grouped records by course and computed the final CSE average marks as **`82.5`**.
- **Reduce-Side Join**: Joined employee records with their respective department names in MapReduce, successfully producing the joined output records (`3 Amit HR`, `1 Raj HR`, and `2 Neha Finance`).
- **Bloom Filter**: Correctly validated member items (`apple`, `banana` returned `True`) and rejected non-members (`mango`, `orange` returned `False` in the 50-bit test), with a theoretical false-positive probability of **`0.447%`** ($p \approx 0.00447$).

---

## Repository Purpose

This repository serves as the organized submission of the hands-on artefacts required for the Big Data Analytics certification assessment. It preserves the verified source code, execution workflows, and outputs for formal academic evaluation.
