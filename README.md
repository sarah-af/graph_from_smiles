Graph datasets consisting of lists or (nested lists) containing the following features,
* Edge_index
* edge_attr
* node_feat
* num_nodes
* label

The SMILES list is read from the Molgraph Library [https://github.com/akensert/molgraph].
The dataset can be used to train 🤗 Graphormer model [https://huggingface.co/blog/graphml-classification].

Using the function requires rdkit, molgraph, and datasets.
