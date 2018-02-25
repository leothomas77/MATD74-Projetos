from PIL import Image
import numpy as np
from random import randint


#Esta implementação trabalha com imagens em grayscale para facilitar a implementacao
#trabalhar com cores é trivial
#Definição Algoritmo
#Recebe imagem de entrada
#Recebe um K de entrada
#Sorting da imagem (heapsort) como array 1D
#randomiza de modo nao decrescente os K centroides posicionados como cores da imagem
#Computa os pontos medios entre cada K centroide e agrupa os pixels no array mudando suas cores para as do ponto medio equivalente


#custom struct
p_type = [('c', int),('x', int),('y', int)]

path = input("Insert path to image: ")
im = Image.open(path).convert('L') # grayscale conversion

k_list = []
K = input("Insert number of centroids (K) or space to automatic detection of centroids: ")

if K != " ":
    K = int(K)
    k_list = np.empty(K)
else:
    #color histogram based centroids
    histogram = im.histogram()
    max_frequence = np.amax(histogram)
    threshold = 0.5
    print ("Max is:", max_frequence)
    print ("Min is:", np.amin(histogram))

    for i, value in enumerate(histogram):
        if (value >= max_frequence * threshold ):
            k_list.append(value)
    
    K = len(k_list)
    print ("Automatic generated K is:", K)
#convert to grayscale and then to numpy array
im_arr = np.array(im)
rows, cols = im_arr.shape
dim = rows * cols

#custom dtype
custom_arr = np.empty((dim), dtype=p_type)

for x in range(0, rows):
    for y in range(0, cols):
        custom_arr[x * cols + y] = (im_arr[x, y], x, y)

sorted_arr = np.sort(custom_arr, order='c')
minColor = sorted_arr[0]['c']
maxColor = sorted_arr[len(sorted_arr) - 1]['c']

#randomize centroids with values between minColor and maxColor
for i in range(K):
	k_list[i] = np.random.uniform(minColor, maxColor)

#to np.array
k_arr = np.array(k_list)
sorted_k = np.sort(k_arr)

j = 0
for i in range(K):
    if i < K - 1:
        medium = int((sorted_k[i] + sorted_k[i+1])/2)
    else:
        medium = sorted_k[i]
    iterate = True
    while(iterate and j < dim):
        if sorted_arr[j]['c'] <= medium:
            sorted_arr[j]['c'] = medium
            j = j + 1
        else:
            iterate = False

final = np.empty((rows, cols), dtype=int)
for i in range(dim):
    x = sorted_arr[i]['x']
    y = sorted_arr[i]['y']
    c = sorted_arr[i]['c']
    final[x,y] = c
         

save_path = input("insert save path: ")         
seg = Image.fromarray(np.uint8(final))
seg.save(save_path)
seg.close()
