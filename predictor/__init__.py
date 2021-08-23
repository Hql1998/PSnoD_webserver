import os
from predictor.prepare import *
from predictor.BNNR import bnnr


DISEASE_SIM_PATH = os.path.join(os.path.dirname(__file__), "disease_sim_graph_filtered.csv")
BENCHMARK_FEATURE_PATH = os.path.join(os.path.dirname(__file__), "snoRNA_4mer.csv")
BENCHMARK_SIM_PATH = os.path.join(os.path.dirname(__file__), "snoRNA_4mer_similarity.csv")
RELATION_MATRIX_PATH = os.path.join(os.path.dirname(__file__), "relationship_matrix_filtered.csv")
MESH_MAP_PATH = os.path.join(os.path.dirname(__file__), "mesh_id_map.tsv")

BNNR_ALPHA = 0.1
BNNR_BETA = 30

def predict_snoRNAs(fasta_list):
    seq_head_list = []
    seq_feature_list = []
    for i in fasta_list:
        seq_head_list.append(i[0])
        seq_feature_list.append(compute_snoRNA_4mer(i[1]))

    benchmark_feature_df = load_snoRNA_feature(BENCHMARK_FEATURE_PATH)
    seq_self_sim_np = compute_self_sim(seq_feature_list)
    seq_against_bench_sim_np = compute_sim_against_benchmark(seq_feature_list, benchmark_feature_df)
    mesh_map = pd.read_csv(MESH_MAP_PATH, delimiter="\t", header=0, index_col=0)

    disease_sim_df = load_disease_sim(DISEASE_SIM_PATH)
    benchmark_sim_df = load_snoRNA_sim(BENCHMARK_SIM_PATH)
    relation_matrix_df = load_relation_matrix(RELATION_MATRIX_PATH)
    # print(disease_sim_df.shape)
    # print(benchmark_sim_df.shape)

    relation_matrix_zeroed_df = append_zeros_cols(relation_matrix_df, seq_head_list)
    # print("relation_matrix_zeroed_df", relation_matrix_zeroed_df.shape)
    seq_sim_processed_df = compose_seq_sim(benchmark_sim_df, seq_against_bench_sim_np, seq_self_sim_np, seq_head_list)
    # print("seq_sim_processed_df", seq_sim_processed_df.shape)

    matrix_need_to_complete, matrix_mask = compose_matrix(disease_sim_df, seq_sim_processed_df, relation_matrix_zeroed_df)
    # print("matrix_need_to_complete", matrix_need_to_complete.shape)
    matrix_completed, iterations = bnnr(matrix_need_to_complete.to_numpy(), matrix_mask.to_numpy(), alpha=BNNR_ALPHA, beta=BNNR_BETA)
    matrix_completed = pd.DataFrame(matrix_completed, index=matrix_mask.index, columns=matrix_mask.columns)
    target_sim = matrix_completed.loc[disease_sim_df.index, seq_head_list]
    # print("target_sim", target_sim.shape)
    target_sim.index = mesh_map.loc[target_sim.index]

    return target_sim



