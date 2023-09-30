#include "utils.h"
#include <omp.h>

//  Pauli Composer
//  x (char *)     = string that defines the Pauli matrix, i.e: XXXX
//  weight (double) = coefficient that multiplies the matrix
void pauli_composer(char *entry_lwr, int n, bool is_complex, float init_entry_real, float init_entry_img, int *col, float *real, float* img){
    //  Reverse entry
    char *rev_entry = malloc(n*sizeof(char));
    rev_entry = strcpy(rev_entry, entry_lwr);
    rev_entry = strrev(rev_entry);
    int *rev_bin_entry = malloc(n*sizeof(int)); // ---------------------------------> Hint:  se puede guardad bit a bit 

    // //  Compute first column k(0)
    int col_val = 0;
    for (int i = 0; i < n; i++)                 
    {
        int temp = binary(rev_entry[i]);
        col_val +=  temp << i;
        rev_bin_entry[i] = temp;
    }
    
    
    col[0] = col_val;
    real[0] = init_entry_real;

    if(is_complex){
        img[0] = init_entry_img;
    }
    
    int i, j, p, disp;
    //  Now that everything is prepared, compute the following elements
    #pragma omp parallel shared(i,p,real, img,disp,col, rev_entry,is_complex), private(j)
    {
    for (i = 0; i < n; ){
        int id = omp_get_thread_num();
        if (id == 0){
            p = 1<<i; // left-shift of bits ('1' (1) << 2 = '100' (4))        
            disp = (rev_bin_entry[i] == 0) ? p: -p; // displacements
        }
        
        #pragma omp barrier
        #pragma omp for  private(j)
    //     // #pragma omp parallel for 
        for ( j = 0; j < p; j++)
        {
            // int num = omp_get_num_threads();
            // int id = omp_get_thread_num();
            // printf("La cantidad de hilos activos es: %d, yo soy el hilo %d analizando la posicion %d, p es %d \n", num, id, j, p);
            // //  compute new columns
            col[p + j] = col[0 + j] + disp; 
            //printf("Proceso:%d ---> valor de i:%d, valor de p:%d, valor de j:%d \n",omp_get_thread_num(), i,p,j);
            //  store new entries using the old ones
            if(is_complex){
                if (rev_entry[i]=='i' || rev_entry[i]=='x'){
                    img[p + j] = img[0 + j]; // castear
                } 
                else{
                    img[p + j] = 0 - img[0 + j];
                }
            }
            else{
                if (rev_entry[i]=='i' || rev_entry[i]=='x'){
                    real[p + j] = real[0 + j]; 
                } 
                else{
                    real[p + j] = 0 - real[0 + j];
                }
            }
        }
        
        if (id == 1){
            i++;
        }
        #pragma omp barrier
    }
    }
    free(rev_bin_entry);
    free(rev_entry);
}
