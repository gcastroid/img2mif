from PIL import Image 
import sys

# read the arguments
img_file = sys.argv[1]
out_file = sys.argv[2]

# read the image
image = Image.open(img_file)
pixels = image.load()
h_pixels, v_pixels = image.size

# calc the number of address bits and the memory depth
h_bits = (h_pixels - 1).bit_length()
v_bits = (v_pixels - 1).bit_length()
addr_bits = h_bits + v_bits
depth = pow(2, int(addr_bits))
data_bits = 12

# print the image resolution 
print("Number of hor pixels:", h_pixels)
print("Number of vert pixels:", v_pixels)

# Create the .mif output file 
mif = open(out_file, "w")

# MIF header 
# number of data bits
mif.write("width = ")
mif.write(str(data_bits))
mif.write(";\n") 
# number of addresses
mif.write("depth = ")
mif.write(str(depth))
mif.write(";\n") 
# radix
mif.write("address_radix = hex;\n")
mif.write("data_radix = hex;\n\n")
mif.write("content begin\n\n")
line = 0

# write each address value with the pixels
for i in range(v_pixels): # number of vertical pixels 
   for j in range(h_pixels): # number of horizontal pixels 

      # read the RGB888 and convert to RGB444
      r,g,b = pixels[j,i]
      r = r & (0xf<<4)
      g = g & (0xf<<4)
      b = b & (0xf<<4)
      r = r << 4
      b = b >> 4
      rgb = r | g | b

      # write the address line and data value
      mif.write(str(hex(line)[2:]))
      mif.write(": ") 
      mif.write(str(hex(rgb)[2:]))
      mif.write(";\n")

      # just print the actual value
      print("address:", hex(line))
      print("(r, g, b) = ", pixels[j,i])
      print("rgb444:", hex(rgb))
      print("\n")
      line += 1

# complete the rest of the addresses with 0s 
# if they were not filled
mif.write("\n")
if line < depth:
   mif.write("[")
   mif.write(str(hex(line)[2:]))
   mif.write("..")
   mif.write(str(hex(depth-1)[2:]))
   mif.write("]: 000;\n\n") 

# end of file
mif.write("end;")

# close file
mif.close()

# output message
print(".mif file generated, bye!\n")