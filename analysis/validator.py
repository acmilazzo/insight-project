#Methods to validate results

import pandas
import string
import json

def create_output_string( similarity_values, norm_df, mat1, mat2):
    out_string = similarity_values.to_string(header=False, index=False)
    shared_col_list = norm_df.ix[[mat1, mat2 ]].dropna(axis=1).columns
    shared_string = ' '.join(shared_col_list)
    out_string = out_string + ' ' + shared_string
    return out_string

def validate_distance_similarities(norm_df, similarity_df, validation_file, output_file):
    inobj = open( validation_file, 'r' )
    validation_data = json.load( inobj )
    outobj = open( output_file, 'w' )
    for material_class in validation_data.keys():
        material_list = validation_data[material_class]
        
        while len(material_list) > 1:
            popped = material_list.pop()
            for i in xrange(0,len(material_list)):
                
                if similarity_df[(similarity_df.mat1 == material_list[i]) 
                   & (similarity_df.mat2 == popped)].empty:
                    if similarity_df[(similarity_df.mat1 == popped) 
                       & (similarity_df.mat2 == material_list[i])].empty:
                           print 'empty set'
                    else: 
                        similarity_values = similarity_df[(similarity_df.mat1 == popped) & (similarity_df.mat2 == material_list[i])]
                        out_string = create_output_string( similarity_values, norm_df, popped, material_list[i])
                        outobj.write( out_string + '\n')
                else:
                     similarity_values = similarity_df[(similarity_df.mat1 == material_list[i]) & (similarity_df.mat2 == popped)]
                     out_string = create_output_string( similarity_values, norm_df, popped, material_list[i])
                     outobj.write( out_string + '\n')
    outobj.close()
    return 0
