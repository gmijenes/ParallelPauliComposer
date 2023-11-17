#include <stdio.h>
#include <omp.h>

int main() {
    int num_threads = 16; // Número de hilos que deseas utilizar
    omp_set_num_threads(num_threads);

    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        printf("Hola desde el hilo %d\n", thread_id);
    }

    return 0;
}
