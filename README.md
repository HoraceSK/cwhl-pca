# cwhl-pca
Principal Component Analysis for expenses of the company CheWangHuLian.
## Project scan
In the normal operation of a company without major business changes, the monthly amount of management expenses should not be much different. If there is a large fluctuation, there may be some large expenses. If it exceeds the level of importance, it should be taken seriously Investigate the cause clearly.
## Analysis
The detailed ledger is converted into a data matrix that is easy to analyze, and then the Minkowski distance + ward method is used to hierarchically cluster the variables to obtain a clustering data matrix, and then the variance maximization is used to perform principal component analysis to find the The original variables corresponding to the largest components of the feature vector are the most important detailed subjects that cause fluctuations in monthly amounts during the year of management expenses.
