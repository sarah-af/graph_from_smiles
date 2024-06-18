import numpy as np
from rdkit import Chem
from molgraph.chemistry import datasets
import json
from datasets import Dataset, DatasetDict


def smiles2dict(ds,output_file):
    #Get dataset from molgraph
    dataset = datasets.get(ds)
    x_train = dataset['test']['x']
    y_train = dataset['test']['y']

    node_feat = []
    edge_index = []
    edge_attr = []
    num_node = []

    #Loop through array of smiles
    for smiles in x_train:
        mol = Chem.MolFromSmiles(smiles)
        node_feats = []
        edge_indices = []
        edge_attrs = []
        num_nodes = mol.GetNumAtoms()
        num_node.append(num_nodes) 

        for atom in mol.GetAtoms():
            node_feats.append(atom.GetAtomicNum())
        node_feat.append(node_feats)

        for bond in mol.GetBonds():
            edge_indices.append([bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()])
            edge_attrs.append([bond.GetBondTypeAsDouble()])
        edge_attr.append(edge_attrs)
        
        #Convert edge_index from list of pairs to a list of 2 lists.
        flat_edge_index = [[], []]

        for pair in edge_indices:
            flat_edge_index[0].append(pair[0])
            flat_edge_index[1].append(pair[1])
        flat_edge_index = [np.array(flat_edge_index[0]), np.array(flat_edge_index[1])]
        flat_edge_index = [flat_edge_index[0].tolist(), flat_edge_index[1].tolist()]
        edge_index.append(flat_edge_index)
        
        
        
    
    ds_dict = Dataset.from_dict({
        'edge_index': edge_index,
        'edge_attr': edge_attr,
        'node_feat': node_feat,
        'num_nodes': num_node,
        'y': y_train
        
    })  

    dataset_dict = DatasetDict({'train': ds_dict})

    output_file = "ds_name.jsonl"
    with open(output_file, "w") as f:
        for example in dataset_dict["train"]:
            f.write(json.dumps(example) + "\n")
            

smiles2dict("dataset","file_name")