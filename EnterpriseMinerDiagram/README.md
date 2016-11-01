#SAS Enterprise Miner diagram

This xml file can be imported into SAS Enterprise Miner to create a diagram workspace. The diagram can be modified to inlcude
different inputs and/or methods.

The target variable modeled is a binary variable indicating if an DDA title was purchased within 12 months of being added to the library catalog.

This assumes that book summary data (i.e. from Syndetics) is used as unstructured input. 

Nodes used include:

1. Sample
2. Decisions
3. Text Parsing
4. Text Filter
5. Text Topic
6. Text Cluster
7. Decision Tree
8. Regression
9. Model Comparison
