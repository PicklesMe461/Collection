import machine
from machine import Pin, ADC
import time

# Create ADC objects for the QRD sensors
qrdA = ADC(Pin(26))
qrdB = ADC(Pin(27))

# Array to get cluster
qrdA_vals = []
qrdB_vals = []

# Cluster element delay
cluster_delay 	= 0.1
# Cluster size
cluster_size = 35


# qrd.read_u16() > 

# Function for filtered readings
def filter():
    cluster_sum_A = 0
    cluster_sum_B = 0
    avs_A = []
    avs_B = []
    change_A = 0
    change_B = 0
    list_size = 320
    data_list = []
    counter = 0


    for i in range(cluster_size):
        qrdA_vals.append(qrdA.read_u16())
        qrdB_vals.append(qrdB.read_u16())
        cluster_sum_A += qrdA_vals[i]
        cluster_sum_B += qrdB_vals[i]
        time.sleep(cluster_delay)
    avs_A.append(cluster_sum_A/cluster_size)
    avs_B.append(cluster_sum_B/cluster_size)
    counter = counter + 1
    print(counter, " A: ", avs_A[0] , "B: ", avs_B[0])

    while True:
        qrdA_vals.pop(0)
        qrdB_vals.pop(0)
        qrdA_vals.append(qrdA.read_u16())
        qrdB_vals.append(qrdB.read_u16())
        cluster_sum_A = sum(qrdA_vals)
        cluster_sum_B = sum(qrdB_vals)
        avs_A.append(cluster_sum_A/cluster_size)
        avs_B.append(cluster_sum_B/cluster_size)
        print( counter ," A: ", avs_A[0] , "B: ", avs_B[0])
        counter = counter + 1
        data_list.append([avs_A[0], avs_B[0]])
        data_logA.write(str(avs_A[0])+",")
        data_logB.write(str(avs_B[0])+",")
        change_A = abs(avs_A[0] - avs_A[1])
        change_B = abs(avs_B[0] - avs_B[1])
        #print("Change A: ", change_A, "Change B: ", change_B)
        avs_A.pop(0)
        avs_B.pop(0)
        if len(data_list) >= list_size:
            print("################################################")
            print("Data list: ")
            print("\n")
            print(data_list)
            data_logA.close()
            data_logB.close()

            break
        
        time.sleep(cluster_delay)
        
#file.write(str(value)+",")

data_logA=open("logA.csv","w")
data_logB=open("logB.csv","w")
filter()


