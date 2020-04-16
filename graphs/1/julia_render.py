'''
Requires PIL library to run , use pip to install
to run navigate to file location and 
type: python julia_render.py [path to input file] [output image name] [width] [height] [max iterations]
Expected file type should have following for each line (also assumes that (0,0) is at top left corner)
x_cord y_cord iteration  
'''
import sys
from PIL import Image
import os
import colorsys
import time
def colorer_black_wihte(iterations,max_interations):
	if iterations == max_interations:
		return (0,0,0)#black
	return (255,255,255)

def colorer_xmas_color(iterations,max_interations):
	step=(int)(max_interations/5)
	if iterations <= step*0:
		return (4,2,150)#blue
	elif iterations <= step*2:
		return (161,25,10)#red
	elif iterations <= step*3:
		return (137,156,163)#silver
	elif iterations <= step*4:
		return (140,126,55)#gold
	elif iterations <= step*5:
		return (7,125,45)#green
	return (4,2,150)

def colorer_blue_green(iterations,max_interations):
	step=(int)(max_interations/5)
	if iterations <= step*0:
		return (47,79,79)
	elif iterations <= step*2:
		return (0,128,128)
	elif iterations <= step*3:
		return (0,139,139)
	elif iterations <= step*4:
		return (0,255,255)
	elif iterations <= step*5:
		return (0,206,209)
	elif iterations <= step*6:
		return (64,224,208)
	elif iterations <= step*7:
		return (72,209,204)
	elif iterations <= step*8:
		return (32,178,170)
	elif iterations <= step*9:
		return (224,255,255)

	return (4,2,150)

def colorer_green_grade(iterations,max_interations):
	step=(int)(250/max_interations)
	return (148,iterations*step,230)
def colorer_red_grade(iterations,max_interations):
	step=(int)(250/max_interations)
	return (iterations*step,150,230)

def colorer_blue_grade(iterations,max_interations):
	step=(int)(250/max_interations)
	return (150,230,iterations*step)

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
	out_file_path = sys.argv[2]
	width = int(sys.argv[4])
	height = int(sys.argv[3])
	max_interations = 50
	if len(sys.argv)>5:
		max_interations = int(sys.argv[5])

	img = Image.new( 'RGB', (width,height), "black") # Create a new black image
	pixels = img.load() # Create the pixel map
	
	#print(max_interations)
	outNum = 0
	work=height*width
	work_done=0
	while os.path.exists(in_file_path + str(outNum)+".txt"):

		file_path = in_file_path + str(outNum)+".txt"
		file_in = open(file_path, "r")
		for line in file_in:
			#get coordinates and number of iterations before escape
			line_arguments = line.strip().split()
			i=int(line_arguments[0])
			j=int(line_arguments[1])
			iterations=int(line_arguments[2])

			# color each pixel based of iterations before escape use one of the colorer functions from above
			pixels[j,i]=colorer_hsv(iterations,max_interations) # change colorer function (choose from one above) to get different results 
			#pixels[j,i]=colorer_blue_green(iterations,max_interations)
			work_done+=1
			per=work_done/work*100;

			if(per%5==0):
				print(per,"%")
		outNum += 1
	#img.show()
	img.save(out_file_path+".png")

start_time = time.time()
main()
print("time spend: %s seconds" %(time.time() - start_time))


