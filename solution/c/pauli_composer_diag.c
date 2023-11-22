#include "utils.h"
#include <omp.h>

void pauli_composer(char *entry_lwr, int n, char init_entry, char *values){
    
    char *rev_entry = malloc(n*sizeof(char));
    rev_entry = strcpy(rev_entry, entry_lwr);
    rev_entry = strrev(rev_entry);
    int *rev_bin_entry = malloc(n*sizeof(int)); 
    
    for (int i = 0; i < n; i++)                 
    {
        int temp = binary(rev_entry[i]);
        rev_bin_entry[i] = temp;
    }
    
    values[0] = init_entry;
    
    int i, j, p;
    #pragma omp parallel shared(i,p,values, rev_entry), private(j)
    {
    for (i = 0; i < n; ){
        int id = omp_get_thread_num();
        if (id == 0){
            p = 1<<i; 
        }
        
        #pragma omp barrier
        #pragma omp for private(j)
        for ( j = 0; j < p; j++)
        {
            if (rev_entry[i]=='i'){
                values[p + j] = values[0 + j]; 
            } 
            else{
                if (values[0 + j] == '1') {
                    values[p + j] = '0';
                } else {
                    values[p + j] = '1';
                }
            }
        }
        
        if (id == 0){
            i++;
        }
        #pragma omp barrier
    }
    }
    free(rev_bin_entry);
    free(rev_entry);
}
