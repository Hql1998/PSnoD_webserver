from predictor.kmer import kmer_featurization
import pandas as pd
import numpy as np


#Tanimoto系数
def tanimoto_coeffcient(x1, x2):
    return (x1 * x2).sum() / ((x1 * x1).sum() + (x2 * x2).sum() - (x1 * x2).sum())


def load_disease_sim(disease_sim_path):

    disease_sim_graph_df = pd.read_csv(disease_sim_path, header=0, index_col=0)
    return disease_sim_graph_df


def load_snoRNA_sim(seq_sim_path):

    seq_simlarity_df = pd.read_csv(seq_sim_path, header=0, index_col=0)
    seq_simlarity_df.index = seq_simlarity_df.index.map(int)
    seq_simlarity_df.columns = seq_simlarity_df.columns.map(int)

    return seq_simlarity_df


def load_snoRNA_feature(seq_feature_path):

    seq_simlarity_df = pd.read_csv(seq_feature_path, header=None, index_col=0)

    return seq_simlarity_df


def compute_snoRNA_4mer(seq):

    extract_feature_obj = kmer_featurization(4)
    kmer_feature = extract_feature_obj.obtain_kmer_feature_for_one_sequence(seq, write_number_of_occurrences=False)

    return kmer_feature


def compute_self_sim(seq_feature_list):

    length = len(seq_feature_list)
    if length == 1:
        return np.array([1])
    else:
        seq_simlarity = np.zeros((length, length))
        for i in range(length-1):
            for j in range(1, length):
                sim_ij = tanimoto_coeffcient(seq_feature_list[j], seq_feature_list[i])
                seq_simlarity[j, i] = sim_ij
                seq_simlarity[i, j] = sim_ij
        di = np.diag_indices(length)
        seq_simlarity[di] = 1
        return seq_simlarity


def compute_sim_against_benchmark(seq_feature_list, benchmark_feature_list):

    length = len(seq_feature_list)
    benchmark_length = len(benchmark_feature_list)
    seq_sim = np.zeros((length, benchmark_length))
    for i in range(length):
        for j in range(benchmark_length):
            seq_sim[i, j] = tanimoto_coeffcient(seq_feature_list[i], benchmark_feature_list.iloc[j, :])

    return seq_sim


def load_relation_matrix(relation_matrix_path):

    relationship_matrix_df = pd.read_csv(relation_matrix_path, header=0, index_col=0)
    relationship_matrix_df.columns = relationship_matrix_df.columns.map(int)

    return relationship_matrix_df


def append_zeros_cols(matrix_df, seq_head_list):

    length = len(seq_head_list)
    disease_num = matrix_df.shape[0]
    tem_df = pd.DataFrame(np.zeros((disease_num, length)), index=matrix_df.index, columns=seq_head_list)

    return pd.concat([matrix_df, tem_df], axis=1)


def compose_seq_sim(benchmark_seq_sim_df, seq_against_bench_sim_np, seq_self_sim_np, seq_head_list):

    seq_against_bench_sim_df = pd.DataFrame(seq_against_bench_sim_np, index=seq_head_list, columns=benchmark_seq_sim_df.columns)
    seq_self_sim_df = pd.DataFrame(seq_self_sim_np, index=seq_head_list, columns=seq_head_list)
    temp_df_1 = pd.concat([benchmark_seq_sim_df, seq_against_bench_sim_df], axis=0)
    temp_df_2 = pd.concat([seq_against_bench_sim_df, seq_self_sim_df], axis=1).transpose()

    return pd.concat([temp_df_1, temp_df_2], axis=1)

def compose_matrix(disease_sim_df, seq_sim_processed_df, relation_matrix_zeroed_df):

    temp_df1 = pd.concat((disease_sim_df, relation_matrix_zeroed_df), axis=1)
    temp_df2 = pd.concat((relation_matrix_zeroed_df.transpose(), seq_sim_processed_df), axis=1)
    need_complete_matrix = pd.concat((temp_df1, temp_df2), axis=0).astype(np.float)

    a_mask = pd.DataFrame(np.ones((disease_sim_df.shape)), index=disease_sim_df.index, columns=disease_sim_df.index)
    b_mask = pd.DataFrame(np.ones((seq_sim_processed_df.shape)), index=seq_sim_processed_df.index, columns=seq_sim_processed_df.index)

    temp_mask = pd.concat((a_mask, relation_matrix_zeroed_df), axis=1)
    temp1_mask = pd.concat((relation_matrix_zeroed_df.transpose(), b_mask), axis=1)
    matrix_mask = pd.concat((temp_mask, temp1_mask), axis=0).astype(np.float)

    return need_complete_matrix, matrix_mask