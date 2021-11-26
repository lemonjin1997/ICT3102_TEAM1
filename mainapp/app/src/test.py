from timeit import timeit
import statistics

total_time = 0
test_data = []
for x in range(50):
    tmp_time = 0
    tmp_time = timeit("insert_ping(staff_id, beacon_mac, RSSI)", 'from crud.crud import insert_ping;  staff_id = "123"; beacon_mac = "E1C328D7D152"; RSSI = "-51"; ', number=1)
    total_time += tmp_time
    print("time take for ", x+1 ," run :" ,tmp_time)
    test_data.append(tmp_time)
average_time = total_time/50

print("min: ", min(test_data))
print("max: ", max(test_data))
print("mode: " , statistics.mode(test_data))
print("median: " , statistics.median(test_data))
print("total time: ", total_time)
print("average time: ", average_time)
