
#Handle data and calculate similaries
import pandas
import time
import scipy
import scipy.stats as stats


def read_data_w_index( filename ):
    orig_dataframe = pandas.read_csv( filename, index_col=0, 
                                     skip_blank_lines=True )
    return orig_dataframe
    

    
def normalize_input( input_dataframe ):
    df_zscore = (input_dataframe - input_dataframe.mean())
                              /input_dataframe.std(ddof=0)
    feature_num_dict = {}
    index_vals = list(df_zscore.index.values)
    for rownum in xrange(1,(len(df_zscore.index))):
        num_features = len( df_zscore.ix[rownum].dropna() )
        if num_features in feature_num_dict:
            feature_num_dict[num_features].append(index_vals[rownum])
        else:
            feature_num_dict[num_features] = []
            feature_num_dict[num_features].append(index_vals[rownum])
    #prune from data set from materials w/no shared feature values
    normalized_dataframe = df_zscore.drop( feature_num_dict[0] )
    return normalized_dataframe 
    
#Function takes in and computes similarity on all pairwise comparisons of
#materials. Output is used in subsequent similarity statistical 
#measures culling materials that share 2 or greater features
def extract_similarities_orig( input_dataframe, output_filename, subset_vals = 0):
    from sklearn.metrics.pairwise import cosine_similarity
    out_obj = open( output_filename, 'w')
    index_list = list( input_dataframe.index )
    index_subset = []
    if subset_vals > 0:
        index_subset = index_list[0:subset_vals]
    else:
        index_subset = index_list     
    
    while len(index_subset) > 1:
        popped = index_subset.pop()
        for i in xrange(0,len(index_subset)):
            newlist = [popped, index_subset[i]]
            newdf = input_dataframe.ix[newlist].dropna(axis=1)     
            if not newdf.empty:
                col_len = len(newdf.columns) 
                if( col_len >1):
                    result_list = map(list, newdf.values )
                    cosine_result = cosine_similarity( result_list[0],
                                                      result_list[1] )
                    euclidean_result = scipy.spatial.distance.euclidean(
                                                        result_list[0], 
                                                        result_list[1])
                    names = list(newdf.index)
                    cvs_line = names[0] + ',' + names[1] 
                               + ',' + str(cosine_result[0][0]) + 
                               ',' + str(euclidean_result) + 
                               ',' + str(col_len)
                    out_obj.write( cvs_line + '\n')
    return


def extract_similarities_mod( zscore_dataframe, sim_dataframe, output_file):
    outobj = open( output_file, 'w')
    len_index = len(sim_dataframe.index)
    for rownum in xrange(1,len_index):
        pairwise_vals = sim_dataframe.ix[rownum].values
        if int(pairwise_vals[4]) > 2:
            euclid_dist = calculate_normalized_euclidean_measures(pairwise_vals[3], pairwise_vals[4])
            [tau, p_value] = calculate_kendall_tau( zscore_dataframe, pairwise_vals[0], pairwise_vals[1])
            out_string = pairwise_vals[0] + ',' + pairwise_vals[1] + ',' + str(pairwise_vals[2]) + ',' + str(pairwise_vals[3]) + ',' + str(pairwise_vals[4]) + ',' + str(euclid_dist) + ',' +  str(tau) + ',' + str(p_value) + '\n'
            outobj.write( out_string ) 
    outobj.close() 
    return

    
#Function takes calculated euclidean distances between materials and 
#divides by number of shared features.    
def calculate_normalized_euclidean_measures( euclidean_score, shared_feature_num ):
    return euclidean_score/shared_feature_num
    
def calculate_kendall_tau(zscore_dataframe, material1, material2):
    row_vals = zscore_dataframe.ix[[ material1, material2]].dropna(axis=1).values
    tau,p_value = stats.kendalltau(row_vals[0], row_vals[1])
    return [tau, p_value]
    
#Set first two columns to the material names for output
def transform_to_long_form( input_df, output_file ):
    outobj = open( output_file, 'w' )
    len_index = len(input_df.index)
    outobj.write( 'material1,material2,type,value,pvalue\n')
    for rownum in range(1,len_index):
        pairwise_vals = input_df.ix[rownum].values
        outstring1 = pairwise_vals[0] + ',' + pairwise_vals[1] + ',' +  'cosine_sprse' + ',' + str(pairwise_vals[2]) + ',' + 'NaN' + '\n'
        outstring2 = pairwise_vals[0] + ',' + pairwise_vals[1] + ',' +  'n_euclid_sprse' + ',' + str(pairwise_vals[5]) + ',' + 'NaN' + '\n'
        outstring3 = pairwise_vals[0] + ',' + pairwise_vals[1] + ',' +  'num_feat_sprse' + ',' + str(pairwise_vals[4]) + ',' + 'NaN' + '\n'
        outstring4 = pairwise_vals[0] + ',' + pairwise_vals[1] + ',' +  'ktau_sprse' + ',' + str(pairwise_vals[6]) + ',' + str(pairwise_vals[7]) + '\n'
        outobj.write( outstring1 )
        outobj.write( outstring2 )
        outobj.write( outstring3 )
        outobj.write( outstring4 )
    outobj.close()
    return
