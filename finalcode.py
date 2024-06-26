# -*- coding: utf-8 -*-
"""finalcode.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HUJpPSJ2-VAE440hb457Zr9YbO447or7
"""

from google.colab import drive
drive.mount('/content/drive')

import math
import scipy.io as scio
import numpy as np
mat = scio.loadmat("/content/drive/MyDrive/data/Cdataset/Cdataset.mat") #: This line loads the data
drug_sim = mat["drug"].astype(np.float64)
disease_sim = mat["disease"].astype(np.float64)
drug_name = mat["Wrname"].reshape(-1)
drug_num = len(drug_name)
disease_name = mat["Wdname"].reshape(-1)
disease_num = len(disease_name)
interactions = mat["didr"]

import pandas as pd
df = pd.DataFrame(disease_sim)
print(df)

import pandas as pd


df = pd.DataFrame(drug_sim)
print(df)

print(drug_num)

print(disease_num)



k=0
for i in range(0,409):
 for j in range(0,663):
  if interactions[i,j]==1:
    # print("yes")
    k=k+1
  else:
    pass
print(k)

# Assign the drug_sim array to the drug_similarity variable
drug_similarity = drug_sim
# Create a square matrix of zeros with dimensions based on the shape of drug_similarity
drug_drug_Matrix = np.zeros((drug_similarity.shape[0], drug_similarity.shape[0]), np.float32)
# Assign drug_similarity to drug_sim_Matrix
drug_sim_Matrix = drug_similarity

# Loop over each drug index in drug_similarity
for drug_num0 in range(drug_similarity.shape[0]):
    # Create an empty dictionary to store drug similarities for each drug
    drug_sim = {}

    # Loop over each drug index again to compute similarity
    for drug_num1 in range(drug_similarity.shape[0]):
        # Skip if the drug index is the same (no self-similarity)
        if drug_num0 == drug_num1:
            continue

        # Store the similarity value in the dictionary drug_sim
        drug_sim[drug_num1] = drug_sim_Matrix[drug_num0][drug_num1]

    # Sort the drugs based on their similarity values in descending order
    sorted_drug_list = sorted(drug_sim.items(), key=lambda d: d[1], reverse=True)

    # Take the top 7 most similar drugs (or all if there are fewer than 7)
    for i in range(min(7, len(sorted_drug_list))):
        drug_num1 = sorted_drug_list[i][0]
        # Set the corresponding entry in drug_drug_Matrix to 1 (indicating similarity)
        drug_drug_Matrix[drug_num0][drug_num1] = 1

import pandas as pd


df = pd.DataFrame(drug_drug_Matrix)
print(df)

# Assign the disease_sim array to the disease_similarity variable
disease_similarity = disease_sim
# Create a square matrix of zeros with dimensions based on the shape of disease_similarity
disease_disease_Matrix = np.zeros((disease_similarity.shape[0], disease_similarity.shape[0]), np.float32)
# Assign disease_similarity to disease_sim_Matrix
disease_sim_Matrix = disease_similarity

# Loop over each disease index in disease_similarity
for disease_num0 in range(disease_similarity.shape[0]):
    # Create an empty dictionary to store disease similarities for each disease
    disease_sim = {}

    # Loop over each disease index again to compute similarity
    for disease_num1 in range(disease_similarity.shape[0]):
        # Skip if the disease index is the same (no self-similarity)
        if disease_num0 == disease_num1:
            continue

        # Store the similarity value in the dictionary disease_sim
        disease_sim[disease_num1] = disease_sim_Matrix[disease_num0][disease_num1]

    # Sort the diseases based on their similarity values in descending order
    sorted_disease_list = sorted(disease_sim.items(), key=lambda d: d[1], reverse=True)

    # Take the top 7 most similar diseases (or all if there are fewer than 7)
    for i in range(min(7, len(sorted_disease_list))):
        disease_num1 = sorted_disease_list[i][0]
        # Set the corresponding entry in disease_disease_Matrix to 1 (indicating similarity)
        disease_disease_Matrix[disease_num0][disease_num1] = 1

import pandas as pd


df = pd.DataFrame(disease_disease_Matrix)
print(df)

truth_label=interactions

import pandas as pd


df = pd.DataFrame(truth_label)
print(df)

print(truth_label.shape)

print(drug_drug_Matrix.shape)

print(disease_disease_Matrix.shape)

from sklearn.model_selection import KFold

# Initialize a KFold object with 10 splits, shuffling, and a random state
kfold = KFold(n_splits=10, shuffle=True, random_state=666)

# Get the indices of non-zero elements (positive interactions) in the interactions array
pos_row, pos_col = np.nonzero(interactions)

# Get the indices of zero elements (negative interactions) by subtracting interactions from 1
neg_row, neg_col = np.nonzero(1 - interactions)

# Assert that the sum of positive and negative interactions equals the total number of elements
assert len(pos_row) + len(neg_row) == np.prod(interactions.shape)

# Initialize empty lists to store train and test data masks
train_data, test_data = [], []

# Iterate over the splits generated by kfold.split(pos_row) and kfold.split(neg_row)
for (train_pos_idx, test_pos_idx), (train_neg_idx, test_neg_idx) in zip(kfold.split(pos_row),
                                                                        kfold.split(neg_row)):
    # Initialize train and test masks as boolean arrays of the same shape as interactions
    train_mask = np.zeros_like(interactions, dtype="bool")
    test_mask = np.zeros_like(interactions, dtype="bool")

    # Stack the positive row and column indices to create positive edges
    train_pos_edge = np.stack([pos_row[train_pos_idx], pos_col[train_pos_idx]])
    train_neg_edge = np.stack([neg_row[train_neg_idx], neg_col[train_neg_idx]])

    # Stack the negative row and column indices to create negative edges
    test_pos_edge = np.stack([pos_row[test_pos_idx], pos_col[test_pos_idx]])
    test_neg_edge = np.stack([neg_row[test_neg_idx], neg_col[test_neg_idx]])

    # Concatenate positive and negative edges to get train and test edges
    train_edge = np.concatenate([train_pos_edge, train_neg_edge], axis=1)
    test_edge = np.concatenate([test_pos_edge, test_neg_edge], axis=1)

    # Set the corresponding entries in train and test masks to True based on train and test edges
    train_mask[train_edge[0], train_edge[1]] = True
    test_mask[test_edge[0], test_edge[1]] = True

    # Append the train and test masks to the train_data and test_data lists
    train_data.append(train_mask)
    test_data.append(test_mask)

seed = 666
final_all_auroc, final_all_aupr = [], []
all_train_mask=train_data
all_test_mask=test_data

import math  # Importing the math module for mathematical operations
import random  # Importing the random module for generating random numbers

class BatchManager(object):  # Defining a class named BatchManager

    def __init__(self, data, batch_size, type):  # Defining the constructor method
        disease_input, drug_input, labels = [], [], []  # Initializing empty lists
        disease_sim_Matrix, drug_sim_Matrix, mask, label = data  # Unpacking data into variables
        disease_drug_Adj = np.zeros((disease_sim_Matrix.shape[0], drug_sim_Matrix.shape[0]))  # Creating a zero-filled matrix
        disease_drug_Adj = get_train_adj(disease_drug_Adj, mask, label)  # Computing disease-drug adjacency matrix

        if type == "train":  # Checking the type parameter
            disease_disease_sim_Matrix, drug_drug_sim_Matrix, train_mask, truth_label = data  # Unpacking data for training
            for i in range(len(train_mask)):  # Looping over train_mask rows
                for j in range(len(train_mask[0])):  # Looping over train_mask columns
                    if train_mask[i][j]:  # Checking if the mask value is True
                        disease_input.append(i)  # Appending disease index to input list
                        drug_input.append(j)  # Appending drug index to input list
                        labels.append(disease_drug_Adj[i][j])  # Appending label based on adjacency matrix
                    else:
                        disease_input.append(i)  # Appending disease index to input list
                        drug_input.append(j)  # Appending drug index to input list
                        labels.append(0)  # Appending 0 as label when mask is False

            num_batch = int(math.ceil(len(disease_input) / batch_size))  # Calculating number of batches
            self.batch_data = list()  # Initializing an empty list for batch data

            for i in range(num_batch):  # Looping over the number of batches
                input_disease = disease_input[i * batch_size: (i + 1) * batch_size]  # Slicing input disease data for batch
                input_drug = drug_input[i * batch_size: (i + 1) * batch_size]  # Slicing input drug data for batch
                label = labels[i * batch_size: (i + 1) * batch_size]  # Slicing labels for batch
                self.batch_data.append(  # Appending batch data to batch_data list
                    [disease_drug_Adj, disease_disease_sim_Matrix, drug_drug_sim_Matrix, input_disease, input_drug, label]
                )

        elif type == "valid" or type == "test":  # Checking if the type is valid or test
            disease_disease_sim_Matrix, drug_drug_sim_Matrix, test_mask, truth_label = data  # Unpacking data for validation/test
            for i in range(len(test_mask)):  # Looping over test_mask rows
                for j in range(len(test_mask[0])):  # Looping over test_mask columns
                    if test_mask[i][j]:  # Checking if the mask value is True
                        disease_input.append(i)  # Appending disease index to input list
                        drug_input.append(j)  # Appending drug index to input list
                        labels.append(truth_label[i][j])  # Appending true label based on truth_label matrix

            num_batch = int(math.ceil(len(disease_input) / batch_size))  # Calculating number of batches
            self.batch_data = list()  # Initializing an empty list for batch data

            for i in range(num_batch):  # Looping over the number of batches
                input_disease = disease_input[i * batch_size: (i + 1) * batch_size]  # Slicing input disease data for batch
                input_drug = drug_input[i * batch_size: (i + 1) * batch_size]  # Slicing input drug data for batch
                label = labels[i * batch_size: (i + 1) * batch_size]  # Slicing labels for batch
                self.batch_data.append(  # Appending batch data to batch_data list
                    [disease_drug_Adj, disease_disease_sim_Matrix, drug_drug_sim_Matrix, input_disease, input_drug, label]
                )

        self.len_data = len(self.batch_data)  # Storing the length of batch_data as an attribute

    def iter_batch(self, shuffle=False):  # Defining a method to iterate over batches
        if shuffle:  # Checking if shuffle is True
            random.shuffle(self.batch_data)  # Shuffling the batch_data list
        for idx in range(self.len_data):  # Looping over the length of batch_data
            yield self.batch_data[idx]  # Yielding batches one by one during iteration

"""The iter_batch method allows iteration over batches, optionally shuffling the batch order if specified. This class structure facilitates efficient handling of data batches during the machine learning workflow, ensuring proper data organization and management for training and evaluation tasks."""

def get_train_adj(adj, train_mask, truth_label):
    """
    Update the adjacency matrix based on the training mask and truth labels.

    Parameters:
    - adj (numpy.ndarray): The adjacency matrix to update.
    - train_mask (numpy.ndarray): The training mask indicating which entries to update.
    - truth_label (numpy.ndarray): The true labels corresponding to the mask entries.

    Returns:
    - adj (numpy.ndarray): The updated adjacency matrix.
    """
    for i in range(train_mask.shape[0]):  # Iterate over rows of train_mask
        for j in range(train_mask.shape[1]):  # Iterate over columns of train_mask
            if train_mask[i][j]:  # Check if the mask value is True
                adj[i][j] = truth_label[i][j]  # Update the adjacency matrix value
    return adj  # Return the updated adjacency matrix

import tensorflow as tf
import math

def random_uniform_init(shape, name, dtype=tf.float32):
    # Create a name scope for operations inside this block
    with tf.name_scope('uniform_normal'):
        # Calculate the standard deviation for random normal initialization
        std = 1.0 / math.sqrt(shape[1])
        # Create a variable with random normal initialization
        embeddings = tf.get_variable(name, shape=shape, dtype=dtype,
                                     initializer=tf.initializers.random_normal(stddev=std))
    # Normalize the embeddings along axis 1 (L2 normalization)
    return tf.nn.l2_normalize(embeddings, 1)

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops
from tensorflow.python.eager import context

def cyclic_learning_rate(global_step,
                         learning_rate=0.01,
                         max_lr=0.1,
                         step_size=4.,
                         gamma=0.99994,
                         mode='triangular',
                         name=None):
    # Check if global_step is provided
    if global_step is None:
        raise ValueError("global_step is required for cyclic_learning_rate.")

    # Define a name scope for the operations
    with ops.name_scope(name, "CyclicLearningRate", [learning_rate, global_step]) as name:
        # Convert learning_rate to tensor
        learning_rate = ops.convert_to_tensor(learning_rate, name="learning_rate")
        dtype = learning_rate.dtype
        global_step = math_ops.cast(global_step, dtype)
        step_size = math_ops.cast(step_size, dtype)

        def cyclic_lr():
            """Helper to recompute learning rate; most helpful in eager-mode."""
            # Compute cycle
            double_step = math_ops.multiply(2., step_size)
            global_div_double_step = math_ops.divide(global_step, double_step)
            cycle = math_ops.floor(math_ops.add(1., global_div_double_step))

            # Compute x
            double_cycle = math_ops.multiply(2., cycle)
            global_div_step = math_ops.divide(global_step, step_size)
            tmp = math_ops.subtract(global_div_step, double_cycle)
            x = math_ops.abs(math_ops.add(1., tmp))

            # Compute clr (cyclic learning rate)
            a1 = math_ops.maximum(0., math_ops.subtract(1., x))
            a2 = math_ops.subtract(max_lr, learning_rate)
            clr = math_ops.multiply(a1, a2)

            # Adjust clr based on mode
            if mode == 'triangular2':
                clr = math_ops.divide(clr, math_ops.cast(math_ops.pow(2, math_ops.cast(cycle-1, tf.int32)), tf.float32))
            if mode == 'exp_range':
                clr = math_ops.multiply(math_ops.pow(gamma, global_step), clr)

            return math_ops.add(clr, learning_rate, name=name)

        # Execute cyclic_lr function if not in eager execution mode
        if not context.executing_eagerly():
            cyclic_lr = cyclic_lr()

        return cyclic_lr

# Graph Neural Networks for Drug Repositioning
import tensorflow as tf
import numpy as np
from keras.regularizers import l2
from tensorflow.python.keras.layers import Dense



class Model(object):

    def __init__(self):
        """
        :param config:
        """
        self.lr = 0.01
        self.batch_size = 1024*3
        self.disease_dim = 125
        self.drug_dim = 125
        self.disease_size = 409
        self.drug_size = 663
        self.latent_dim = 64
        self.attention_flag = 1
        self.atten_dim =64
        self.l2 = 1 # init=0

        self.global_step = tf.Variable(0, trainable=False)
        # self.best_dev_auroc = tf.Variable(0.0, trainable=False)
        # self.best_test_auroc = tf.Variable(0.0, trainable=False)
        # self.best_dev_aupr = tf.Variable(0.0, trainable=False)
        # self.best_test_aupr = tf.Variable(0.0, trainable=False)

        # input
        self.e_p_Adj = tf.placeholder(dtype=tf.float32,
                                      shape=[self.disease_size, self.drug_size])
        self.e_e_Adj = tf.placeholder(dtype=tf.float32,
                                      shape=[self.disease_size, self.disease_size])
        self.p_p_Adj = tf.placeholder(dtype=tf.float32,
                                      shape=[self.drug_size, self.drug_size])

        self.input_disease = tf.placeholder(dtype=tf.int32, shape=[None])
        self.input_drug = tf.placeholder(dtype=tf.int32, shape=[None])
        self.label = tf.placeholder(dtype=tf.float32, shape=[None])

        self.disease_embedding = random_uniform_init(name="disease_embedding_matrix",
                                                    shape=[self.disease_size, self.disease_dim])
        self.drug_embedding = random_uniform_init(name="drug_embedding_matrix",
                                                      shape=[self.drug_size, self.drug_dim])

        with tf.variable_scope("model_disease", reuse=tf.AUTO_REUSE):
            gcn_output = self.gcn(self.e_p_Adj, self.drug_embedding, self.drug_dim, self.disease_embedding,
                                  self.latent_dim, self.attention_flag)

            # Modeling top-k diseases Interaction information
            if 7 > 0:
                disease_edges = tf.reduce_sum(self.e_e_Adj, 1)
                disease_edges = tf.tile(tf.expand_dims(disease_edges, 1), [1, self.disease_dim])
                ave_disease_edges = tf.divide(tf.matmul(self.e_e_Adj, self.disease_embedding), disease_edges)

                w2 = tf.get_variable('w2', shape=[self.disease_dim, self.latent_dim],
                                     initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1))
                b2 = tf.get_variable('b2', shape=[self.latent_dim],
                                     initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1))
                h_e_e = tf.nn.xw_plus_b(ave_disease_edges, w2, b2)  # disease_size*latent_dim

                self.h_e = tf.nn.selu(tf.add(gcn_output, h_e_e))
            else:
                self.h_e = tf.nn.selu(gcn_output)

        with tf.variable_scope("model_drug", reuse=tf.AUTO_REUSE):
            gcn_output = self.gcn(tf.transpose(self.e_p_Adj), self.disease_embedding, self.disease_dim,
                                  self.drug_embedding, self.latent_dim, self.attention_flag)

            # Modeling top-k drugs Interaction information
            if 7> 0:
                drug_edges = tf.reduce_sum(self.p_p_Adj, 1)
                drug_edges = tf.tile(tf.expand_dims(drug_edges, 1), [1, self.drug_dim])
                ave_drug_edges = tf.divide(tf.matmul(self.p_p_Adj, self.drug_embedding), drug_edges)

                w3 = tf.get_variable('w3', shape=[self.drug_dim, self.latent_dim],
                                     initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1))
                b3 = tf.get_variable('b3', shape=[self.latent_dim],
                                     initializer=tf.truncated_normal_initializer(mean=0.0, stddev=1))
                h_p_p = tf.nn.xw_plus_b(ave_drug_edges, w3, b3)  # drug_size*latent_dim

                self.h_p = tf.nn.selu(tf.add(gcn_output, h_p_p))
            else:
                self.h_p = tf.nn.selu(gcn_output)

        with tf.variable_scope("drug_rec", reuse=tf.AUTO_REUSE):
            h_e_1 = tf.nn.embedding_lookup(self.h_e, self.input_disease)  # batch_size * disease_latent_dim
            h_p_1 = tf.nn.embedding_lookup(self.h_p, self.input_drug)  # batch_size * drug_latent_dim
            input_temp = tf.multiply(h_e_1, h_p_1)
            for l_num in range(1):
                input_temp = Dense(self.disease_dim, activation='selu', kernel_initializer='lecun_uniform')(input_temp)  # MLP hidden layer
            z = Dense(1, kernel_initializer='lecun_uniform', name='prediction')(input_temp)
            z = tf.squeeze(z)

        self.label = tf.squeeze(self.label)
        self.loss = tf.losses.sigmoid_cross_entropy(self.label, z)
        self.z = tf.sigmoid(z)

        # train
        with tf.variable_scope("optimizer"):
            self.opt = tf.train.AdamOptimizer(learning_rate=cyclic_learning_rate(global_step=self.global_step,
                                                                                 learning_rate=self.lr*0.1,
                                                                                 max_lr=self.lr,
                                                                                 mode='exp_range',
                                                                                 gamma=.999))
            # apply grad clip to avoid gradient explosion
            self.grads_vars = self.opt.compute_gradients(self.loss)
            capped_grads_vars = [[tf.clip_by_value(g, -3, 3), v]
                                 for g, v in self.grads_vars]


            self.train_op = self.opt.apply_gradients(capped_grads_vars, self.global_step)

        # saver of the model
        self.saver = tf.train.Saver(tf.global_variables(), max_to_keep=5)

    def gcn(self, adj, ner_inputs, ner_dim, self_inputs, latent_dim, attention_flag=False):
        """
        Aggregate information from neighbor nodes
        :param adj: Adjacency matrix
        :param attention_flag: GAT flag
        :param ner_inputs: disease or drug embedding
        :param ner_dim: ner_inputs dimension
        :param self_inputs:
        :param latent_dim: output dimension
        :return:
        """
        # aggregate heterogeneous information
        if attention_flag:
            query = tf.tile(tf.reshape(self_inputs, (self_inputs.shape[0], 1, self_inputs.shape[1])), [1, ner_inputs.shape[0], 1])
            key = tf.tile(tf.reshape(ner_inputs, (1, ner_inputs.shape[0], ner_inputs.shape[1])), [self_inputs.shape[0], 1, 1])
            key_query = tf.reshape(tf.concat([key, query], -1), [ner_inputs.shape[0]*self_inputs.shape[0], -1])
            alpha = Dense(self.atten_dim, activation='relu', use_bias=True, kernel_regularizer=l2(self.l2))(key_query)
            alpha = Dense(1, activation='relu', use_bias=True, kernel_regularizer=l2(self.l2))(alpha)
            alpha = tf.reshape(alpha, [self_inputs.shape[0], ner_inputs.shape[0]])
            alpha = tf.multiply(alpha, adj)  # disease_size * drug_size
            alpha_exps = tf.nn.softmax(alpha, 1)
            w1 = tf.get_variable('w1', shape=[ner_dim, latent_dim],
                                 initializer=tf.truncated_normal_initializer(mean=0, stddev=1))
            b1 = tf.get_variable('b1', shape=[latent_dim],
                                 initializer=tf.truncated_normal_initializer(mean=0, stddev=1))
            alpha_exps = tf.tile(tf.expand_dims(alpha_exps, -1), [1, 1, ner_inputs.shape[1]])
            e_r = tf.nn.xw_plus_b(tf.reduce_sum(tf.multiply(alpha_exps, key), 1), w1, b1)
        else:
            edges = tf.matmul(adj, ner_inputs)
            w1 = tf.get_variable('w1', shape=[ner_dim, latent_dim],
                                 initializer=tf.truncated_normal_initializer(mean=0, stddev=1))
            b1 = tf.get_variable('b1', shape=[latent_dim],
                                 initializer=tf.truncated_normal_initializer(mean=0, stddev=1))
            e_r = tf.nn.xw_plus_b(edges, w1, b1)

        return e_r

    def run_step(self, sess, is_train, batch):
        """
        :param sess: session to run the batch
        :param is_train: a flag indicate if it is a train batch
        :param batch: a dict containing batch data
        :return: batch result, loss of the batch or logits
        """
        disease_drug_Adj, disease_disease_Adj, drug_drug_Adj, input_disease, input_drug, label = batch
        feed_dict = {
            self.e_p_Adj: np.asarray(disease_drug_Adj),
            self.e_e_Adj: np.asarray(disease_disease_Adj),
            self.p_p_Adj: np.asarray(drug_drug_Adj),
            self.input_disease: np.asarray(input_disease),
            self.input_drug: np.asarray(input_drug),
            self.label: np.asarray(label)
        }
        if is_train:
            global_step, loss, z, grads_vars, _ = sess.run(
                [self.global_step, self.loss, self.z, self.grads_vars, self.train_op], feed_dict)
            return global_step, loss, z, grads_vars
        else:
            z, labels = sess.run([self.z, self.label], feed_dict)
            return z, labels

def create_model(session, Model_class, path):
    # create model, reuse parameters if exists
    model = Model_class()

    ckpt = tf.train.get_checkpoint_state(path)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        print("Created model with fresh parameters.")
        session.run(tf.global_variables_initializer())
    return model

# Import the necessary metrics module from sklearn
from sklearn import metrics

# Define a function to evaluate model predictions using AUROC and AUPR scores
def evaluate2(predict, label):
    # Calculate the Average Precision Score (AUPR)
    aupr = metrics.average_precision_score(y_true=label, y_score=predict)
    # Calculate the Area Under the ROC Curve (AUROC)
    auroc = metrics.roc_auc_score(y_true=label, y_score=predict)
    # Store the evaluation results in a dictionary
    result = {"aupr": aupr, "auroc": auroc}
    return result

# Define a function to perform evaluation using the evaluate2 function
def evaluate(sess, model, name, data, fold_num=0):
    # Print a message indicating the evaluation dataset
    print("evaluate data:{}".format(name))
    # Initialize lists to store model scores and true labels
    scores, labels = [], []
    # Iterate over batches of data using the data iterator
    for batch in data.iter_batch():
        # Run the model to get predictions for the batch
        score, label = model.run_step(sess, False, batch)
        # Append the scores and labels to the respective lists
        scores.append(score)
        labels.append(label)
    # Concatenate scores and labels into arrays
    scores = np.concatenate(scores)
    labels = np.concatenate(labels)
    # Evaluate the model using the evaluate2 function
    result = evaluate2(scores, labels)
    # Extract AUROC and AUPR scores from the evaluation result
    auroc = result['auroc']
    aupr = result['aupr']
    # Return the AUROC and AUPR scores based on the evaluation dataset
    if name == "valid":
        return auroc, aupr
    elif name == "test":
        # Print the final test AUROC and AUPR scores for the fold
        print("fold {} final test auroc :{:>.5f}".format(fold_num + 1, auroc))
        print("fold {} final test aupr :{:>.5f}".format(fold_num + 1, aupr))
        # Optionally save scores and labels to text files
        # np.savetxt("save_txt/scores{}".format(fold_num + 1), scores, delimiter=" ")
        # np.savetxt("save_txt/labels{}".format(fold_num + 1), labels, delimiter=" ")
        return auroc, aupr

# Set up necessary imports and configurations
dataset = "Cdataset"
import torch  # Import PyTorch library
from torch.utils.data import Dataset, DataLoader  # Import PyTorch dataset and dataloader utilities
from torch.utils.data import TensorDataset, DataLoader  # Redundant import, TensorDataset already imported
import tensorflow as tf  # Import TensorFlow library
import tensorflow.compat.v1 as tf  # Import TensorFlow v1 compatibility
tf.disable_v2_behavior()  # Disable TensorFlow v2 behavior

# Loop over each fold in the dataset
for fold_num in range(len(all_train_mask)):
    # Reset TensorFlow graph and set random seeds for reproducibility
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)

    # Prepare data for training, validation, and testing
    train_datas = (disease_disease_Matrix, drug_drug_Matrix, all_train_mask[fold_num], truth_label)
    valid_datas = (disease_disease_Matrix, drug_drug_Matrix, all_test_mask[fold_num], truth_label)
    test_datas = (disease_disease_Matrix, drug_drug_Matrix, all_test_mask[fold_num], truth_label)

    batch_size = 1024 * 3  # Define batch size

    # Initialize batch managers for training, validation, and testing data
    train_manager = BatchManager(train_datas, batch_size, "train")
    valid_manager = BatchManager(valid_datas, batch_size, 'valid')
    test_manager = BatchManager(test_datas, batch_size, "test")

    # Configure TensorFlow session
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True

    steps_per_epoch = train_manager.len_data  # Calculate steps per epoch for training data

    # Create TensorFlow session
    with tf.Session(config=tf_config) as sess:
        ckptpath = "ckpt/{}/{}-fold{}/".format(dataset, dataset, fold_num + 1)  # Checkpoint path
        model = create_model(sess, Model, ckptpath)  # Create or load the model

        print("start training fold {}".format(fold_num + 1))
        loss_list = []  # Initialize a list to store losses during training

        # Training loop
        for i in range(15):  # Assuming 15 epochs
            for batch in train_manager.iter_batch(shuffle=True):  # Iterate over batches of training data
                step, loss, z, grads_vars = model.run_step(sess, True, batch)  # Run a training step
                loss_list.append(loss)  # Append loss to the list

                # Print training progress
                if step % 20 == 0:
                    iteration = step // steps_per_epoch + 1
                    print("epoch:{} step:{}/{}, loss:{:>9.6f}".format(
                        iteration, step % steps_per_epoch, steps_per_epoch, np.mean(loss_list)))
                    loss_list = []  # Reset loss list after printing

            # Re-initialize the batch manager for the next epoch
            train_manager = BatchManager(train_datas, 1024 * 3, "train")

            # Evaluate the model on the validation set
            auroc, aupr = evaluate(sess, model, "valid", valid_manager, fold_num)
            print("fold {} valid auroc :{:>.5f}".format(fold_num + 1, auroc))
            print("fold {} valid aupr :{:>.5f}".format(fold_num + 1, aupr))

        # Evaluate the model on the test set after training
        final_test_auroc, final_test_aupr = evaluate(sess, model, "test", test_manager, fold_num)
        final_all_auroc.append(final_test_auroc)  # Store final test AUROC
        final_all_aupr.append(final_test_aupr)  # Store final test AUPR

        # Print final test results
        print("fold {} final test auroc :{:>.5f}".format(fold_num + 1, final_test_auroc))
        print("fold {} final test aupr :{:>.5f}".format(fold_num + 1, final_test_aupr))

# Calculate and print average AUROC and AUPR across all folds
print("final_avg_auroc :{:>.5f} final_avg_aupr :{:>.5f}".format(np.mean(final_all_auroc),
                                                                np.mean(final_all_aupr)))

import matplotlib.pyplot as plt
import numpy as np

# Example: Assuming auroc_values contains 150 values, grouped by folds (10 folds, each with 15 values)
  # Example AUROC values

# Organize AUROC values into separate lists for each fold
fold_size = 15
num_folds = 10
auroc_values_folds = [auroc_values[i*fold_size : (i+1)*fold_size] for i in range(num_folds)]

# Plotting separate line graphs for each fold
for fold_num, auroc_values_fold in enumerate(auroc_values_folds, start=1):
    epochs = np.arange(1, len(auroc_values_fold) + 1)  # Assuming one AUROC value per epoch
    plt.plot(epochs, auroc_values_fold, label=f'Fold {fold_num} AUROC')

plt.xlabel('Epoch')
plt.ylabel('AUROC')
plt.title('AUROC Growth for Each Fold During Training')
plt.legend()
plt.grid(True)
plt.show()