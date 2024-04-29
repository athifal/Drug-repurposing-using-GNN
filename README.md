# Drug Repositioning with  Graph Neural Network

Drug repositioning, which involves redirecting existing drugs to new therapeutic purposes, is crucial for accelerating drug discovery efforts. Despite the extensive modeling of complex drug–disease associations in many studies, there is often a lack of emphasis on the relevance between different node embeddings.

To address this gap, we propose a novel weighted local information augmented graph neural network model for drug repositioning. This model incorporates a graph attention mechanism to dynamically allocate attention coefficients to drug and disease heterogeneous nodes, enhancing the effectiveness of target node information collection.

Key Features:
- **Graph Attention Mechanism:** Dynamically allocates attention coefficients to heterogeneous nodes.
- **Information Aggregation:** Emphasizes valuable heterogeneous and homogeneous information while preventing excessive embedding in a limited vector space.
- **Average Pooling:** Enhances local information during neighbor information aggregation.

Our approach omits self-node information aggregation to avoid excessive embedding of information, thereby emphasizing valuable heterogeneous and homogeneous information. Additionally, average pooling in neighbor information aggregation is introduced to enhance local information while maintaining simplicity. Finally, a multi-layer perceptron is employed to generate the final association predictions.

We validate the effectiveness of our model for drug repositioning through a 10-times 10-fold cross-validation on three benchmark datasets. Further validation includes analysis of predicted associations using multiple authoritative data sources, molecular docking experiments, and drug–disease network analysis, laying a solid foundation for future drug discovery endeavors.
