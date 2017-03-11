#ndb_store

   ndb_store is a simple Google App Engine Application that allows one to save sensor data vi HTTP GET requests. 

### API

#### Write
For creating a record of the sensor value via '/write' route
 
##### Create datastore entity whose parent is the device.
```bash
http://YOUR_APP_SPOT_URL_HERE/write?devicename=STRING&sensorreading=INT&sensormin=INT&sensormax=INT
```
 
#### Read  
Retrieving saved sensor values via '/read' route 

##### Retrieve all values for a sensor
    ``` http://<your_appspot_address>/read?devicename=<string> ```
##### example
 
 ###### /write
```
http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=244&sensormin=0&sensormax=1024
http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=48&sensormin=0&sensormax=1024
http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=67&sensormin=0&sensormax=1024
http://YOUR_APP_SPOT_URL_HERE/write?devicename=bluto&sensorreading=5&sensormin=0&sensormax=1024
```
 
###### /read 
 request
```
http://YOUR_APP_SPOT_URL_HERE/read?devicename=bluto
``` 
 returns
 ```
 [5,67,48,244]
 ```
 
or return a dictionary that uses timestamp as the key 
request
```
http://YOUR_APP_SPOT_URL_HERE/read-time?devicename=bluto
```
returns
```python
 {datetime.datetime(2014, 1, 24, 20, 16, 17, 559010): 5, datetime.datetime(2014, 1, 24, 20, 16, 38, 818940): 48, datetime.datetime(2014, 1, 24, 20, 15, 54, 543310): 22, datetime.datetime(2014, 1, 24, 20, 16, 10, 965960): 244, datetime.datetime(2014, 1, 24, 20, 16, 24, 399260): 67, datetime.datetime(2014, 1, 24, 20, 16, 1, 335910): 244}
 ```
 
 
 
 
