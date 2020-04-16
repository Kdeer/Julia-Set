#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"
//#include "gmp.h"


float scale_value(float old_value, float old_max, float old_min, float new_max,
		float new_min) {
	return ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min)
			+ new_min;
}

int main(int argc, char **argv) {

	int my_rank;
	int p; //processors
	int dest = 0; //destination
	int source;
	int height = 500;
	int width = 500;
	double elapsed_time = 0;
 
  if (argc > 1) {
    height = atoi(argv[1]);
    width = atoi(argv[2]);
  }
 
 

	float R = 2; //escape radius

	float cx = -0.8;
	float cy = 0.156;
 
  cx = 0.3;
  cy = -0.4;
  
  cx = -1;
  cy = 0;

	//initialize MPI
	MPI_Status status;
	MPI_Init(&argc, &argv);
	MPI_Barrier(MPI_COMM_WORLD);
	elapsed_time = -1 * MPI_Wtime();
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &p);

	
	//create an output file for each proc
	char f_name[12];
	snprintf(f_name, 12, "out_%d.txt", my_rank);
	FILE *f = fopen(f_name, "w");

	//this strategy just splits rows into chunks and gives a chunk into each processor
	//each chunk has continuous rows
  int m = height/(R*R);
	for (int i = 0; i < height; i++) {
    if(i % p == my_rank){
  		for (int j = 0; j < width; j++) {
  			int ycord = height - 1 - i;
  			//put 0,0 at center
  			int y = ycord - height / 2;
  			int x = j - width / 2;
  
  			//scale coordinates to be between -R and R
  			float zx = scale_value(x, width / 2, -1 * width / 2, R, -1 * R);
  			float zy = scale_value(y, height / 2, -1 * height / 2, R, -1 * R);
        
        //zx = -R + i/m;
        //zy = R - j/m;
  
  			int iteration = 0;
  			int max_iteration = 50;
  
  			while ((zx * zx + zy * zy < R * R) && (iteration < max_iteration)) {
        
          float xtemp = zx * zx - zy * zy + cx;
          float ytemp = 2*zx*zy + cy;
  				zy = ytemp;
  				zx = xtemp;

  				iteration = iteration + 1;
  			}
  			fprintf(f, "%d %d %d\n", i, j, iteration);
  		}
   }
   
   if (i == height - 1 && my_rank == i%p) {
     elapsed_time += MPI_Wtime();
     printf("total elapsed time is %f\n", elapsed_time);
     fclose(f);
   }
   
	}
  
  MPI_Finalize();

}
