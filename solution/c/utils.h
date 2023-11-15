#include <stdio.h>
#include <complex.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

void print_complex(int complex c){
    printf("%d + %di ", (int)creal(c), (int)cimag(c));
}

bool is_complex(int complex c){
    return cimag(c) != 0;
}

int binary(char m){
    if (m == 'y' || m == 'x') return 1;
    else return 0;
    //return (m ^ 105 && m ^ 122);
}

// void test_binary (){
//     int n = 28;
//     char rev_entry[28] = xYxYxXIxYxYxXIxYxYxXIxYYXIXI;
//     for (int i = 0; i < n; i++)                 
//     {
//         int temp = binary(rev_entry[i]);
//         col_val +=  temp << i;
//         rev_bin_entry[i] = temp;
//     }
    
// }

// void test_complex(){
//     float complex dc1 = 3 + 2*I;
//     float complex dc2 = 4 + 1*I;
//     float complex result;

//     result = dc1 + dc2;
//     printf(" %f + %fi \n",  creal(result), cimag(result));

// }

char *strrev(char *str)
{
      char *p1, *p2;

      if (! str || ! *str)
            return str;
      for (p1 = str, p2 = str + strlen(str) - 1; p2 > p1; ++p1, --p2)
      {
            *p1 ^= *p2;
            *p2 ^= *p1;
            *p1 ^= *p2;
      }
      return str;
}

// char* strlwr (char* s) {
//     for (int i = 0; i < strlen(s); ++i)
//         if (s[i] >= 'A' && s[i] <= 'Z')
//             s[i] += 'a' - 'A';
//     return s;
// }

int c_times_in_s (char *s, char c){
    int n = strlen(s);
    int count = 0;
    for (int i = 0; i < n; i++)
    {
        if (s[i] == c){
            count ++;
        }
    }
    return count;
}

// void test_arrays(){
//     char gabriela [] = "GABRIELA";
//     int len = strlen(gabriela);
//     printf("La longitud de la cadena gabriela es %d \n", len);
//     char *rev  = strrev(gabriela);
//     printf(rev);

//     int times = c_times_in_s(gabriela, 'a');

//     printf("\n %d", times);
// }


// Compress an sparse matrix
// int** to_sparse(int **sparseMatrix, int size)
// {
//     // number of columns in compactMatrix (size) must be
//     // equal to number of non - zero elements in
//     // sparseMatrix
//     int **compactMatrix;	
// 	int i;	 
// 	int j;	  
// 	compactMatrix = (int **)malloc(3*sizeof(int*)); 
// 	for (i=0;i<3;i++) 
// 		compactMatrix[i] = (int*)malloc(size*sizeof(int)); 
 
//     // Making of new matrix
//     int k = 0;
//     for (int j = 0; j < size; j++)
//         for (int i = 0; i < 2; i++)
//             if (sparseMatrix[i][j] != 0)
//             {
//                 compactMatrix[0][k] = i;
//                 compactMatrix[1][k] = j%2;
//                 compactMatrix[2][k] = sparseMatrix[i][j];
//                 k++;
//             }
 

//     return compactMatrix;
// }

// void test_to_sparse(){
//     int row1[8] = { 3 , 0, 8, 0, 5, 0,0, -1,  };
//     int row2[8] = { 0 , 1, 0, 1, 0, 1, 9 ,0 };

//     int **sparseMatrix = malloc(2 * sizeof(int*));
//     sparseMatrix[0] = row1;
//     sparseMatrix[1] = row2;

//     int size = 8;
//     int **compactMatrix = to_sparse(sparseMatrix, size);
//     for (int i=0; i<3; i++)
//     {
//         for (int j=0; j<size; j++)
//             printf("%d ", compactMatrix[i][j]);
        
//         printf("\n");
//     }
// }

// //  TODO
// int** to_matrix(int **compactMatrix, int size){
//     int **matrix;	
// 	int i;	 
// 	int j;	  
// 	matrix = (int **)malloc(2*sizeof(int*)); 
// 	for (i=0;i<2;i++) 
// 		matrix[i] = (int*)malloc(size*sizeof(int)); 
    
// }

