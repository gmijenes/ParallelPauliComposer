#include "utils.h"
#include <omp.h>

void pauli_composer(char *entry_lwr, int n, bool is_complex, char init_entry_real,  unsigned int *col, char *real){
    
    char *rev_entry = malloc(n*sizeof(char));
    rev_entry = strcpy(rev_entry, entry_lwr);
    rev_entry = strrev(rev_entry);
    int *rev_bin_entry = malloc(n*sizeof(int)); 

    int col_val = 0;
    for (int i = 0; i < n; i++)                 
    {
        int temp = binary(rev_entry[i]);
        col_val +=  temp << i;
        rev_bin_entry[i] = temp;
    }
    
    
    col[0] = col_val;
    real[0] = init_entry_real;
    
    int i, j, p, disp;
    
    #pragma omp parallel shared(i,p,real,disp,col, rev_entry,is_complex), private(j)
    {
    for (i = 0; i < n; ){
        int id = omp_get_thread_num();
        if (id == 0){
            p = 1<<i; 
            disp = (rev_bin_entry[i] == 0) ? p: -p; 
        }
        #pragma omp barrier
        #pragma omp for private(j)
        for ( j = 0; j < p; j++)
        { 
            col[p + j] = col[0 + j] + disp; 
            if (rev_entry[i]=='i' || rev_entry[i]=='x'){
                real[p + j] = real[0 + j]; 
            } 
            else{
                if (real[0 + j] == '1') {
                    real[p + j] = '0';
                } else {
                    real[p + j] = '1';
                }
            }
        
        }
        if (id == 0){
            i++;
        }
        #pragma omp barrier
    }}
    free(rev_bin_entry);
    free(rev_entry);
}
