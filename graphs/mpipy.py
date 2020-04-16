#!/usr/bin/env python


from mpi4py import MPI
import sys
import time
from PIL import Image
import os
import colorsys

comm = MPI.COMM_WORLD
size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
elapsed_time = time.time()

def hsv2rgb(h,s,v):
	#helper function
	#use this one to get results similar to text book
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def colorer_hsv(iterations,max_interations):
	#set hue, saturation and value
	#use this one to get results similar to text book
	s=255
	h=int(255*iterations/max_interations)

	v = 255 if iterations<max_interations else 0

	s=s/255
	h=h/255
	v=v/255

	return hsv2rgb(h,s,v)



def main():
	#get arguments
	in_file_path = sys.argv[1]
	max_interations = 50
	if len(sys.argv)>5:
		max_interations = int(sys.argv[5])
 
	if rank == 0:
		out_file_path = sys.argv[2]
		width = int(sys.argv[3])
		height = int(sys.argv[4])
		img = Image.new( 'RGB', (width,height), "black") # Create a new black image
		pixels = img.load() # Create the pixel map
		
		work=height*width
		work_done=0
		if os.path.exists(in_file_path + str(rank)+".txt"):
	  
			file_path = in_file_path + str(rank)+".txt"
			file_in = open(file_path, "r")
			for line in file_in:
				line_arguments = line.strip().split()
				i=int(line_arguments[0])
				j=int(line_arguments[1])
				iterations=int(line_arguments[2])
	  
				pixels[j,i]=colorer_hsv(iterations,max_interations)
			for s in range(1, size):
				elapsed_time_series = time.time()
				data = comm.recv(source = s, tag=1)
				for d in data:
					j = d[0]
					i = d[1]
					pixels[j,i] = colorer_hsv(d[2],max_interations)

		elapsed_time_series = time.time() - elapsed_time_series
		print("serial time: %s seconds" %elapsed_time_series)
		img.save(out_file_path+".bmp")
		elapsed_time_total = time.time() - elapsed_time
		print("elapsed time total: %s seconds" %elapsed_time_total)
		elapsed_time_parallel = elapsed_time_total - elapsed_time_series
		print("elapsed time parallel: %s seconds" %elapsed_time_parallel)
		f = elapsed_time_series/(elapsed_time_series+elapsed_time_parallel)
		speedup = 1/(f+(1-f)/size)
		print("AMD law speedup:",speedup)
    
	else:
		if os.path.exists(in_file_path + str(rank)+".txt"):
			result = []
			file_path = in_file_path + str(rank)+".txt"
			file_in = open(file_path, "r")
			for line in file_in:
				temp = []
				line_arguments = line.strip().split()
				i=int(line_arguments[0])
				j=int(line_arguments[1])
				iterations=int(line_arguments[2])
				temp.append(j)
				temp.append(i)
				temp.append(iterations)
				result.append(temp)
			comm.send(result, dest=0,tag=1)

			


main()

 