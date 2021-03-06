#!/usr/bin/env python3
'''
This script runs the algorithm, prints the results, and checks 
that the representation of the call tree matches the one that is 
"scraped" from the cube_dump output.
'''

if __name__ == '__main__':
    from sys import argv
    import calltree as ct
    from cube_file_utils import get_cube_dump_w_text
    
    cube_dump_w_text = get_cube_dump_w_text(argv[1])
    call_tree_lines = ct.get_call_tree_lines(cube_dump_w_text)
    calltree = ct.calltree_from_lines(call_tree_lines)
    max_len = ct.get_max_len(calltree)
    calltree_repr = ct.calltree_to_string(calltree, max_len)
    print("Tree Representation:")
    print(calltree_repr)
    
    import pandas as pd
    data = ct.get_fpath_vs_id(calltree)
    df = pd.DataFrame(data, columns=['Cnode ID', 'Full Callpath'])
    print("Cnode ID vs. Full Callpath dictionary:")
    print(df)
    
    df = ct.calltree_to_df(calltree)
    print("Dataframe representation of the Call Tree:")
    print(df)
    
    # testing that the tree representation matches the one in the 
    # cube_dump output
    import re
    reference = (re.sub(
        '[|-]', '', '\n'.join([
            re.sub('\s*\[\s*\(\s*id=([0-9]+).*$', '\g<1>', line)
            for line in ct.get_call_tree_lines(cube_dump_w_text)
        ])))
    
    calltree_repr = (re.sub('[\-:]', '',
                            ct.calltree_to_string(calltree, 0)).replace(
                                '|', ' ').replace('   ', '  '))
    
    for i, (linea, lineb) in enumerate(
            zip(reference.split('\n'), calltree_repr.split('\n'))):
        assert linea == lineb, f" Line {i}: '{linea}' != '{lineb}'"
    print("Tree representation test: OK")
