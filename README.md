# Project Title

Aerial/Satellite Imagery Retrieval

### Prerequisites

python3.6+

## Running the tests

$python3 retrieval_system.py latitude1 longtitude1 latitude2 longtitude2

### Break down into end to end tests
We provide several coordinates and corresponding result.  
Semi-result was made up by tiles and result was cropped by right bounding box.

Tech building, Northwestern University  
42.058536, -87.677060, 42.057120, -87.674897  
$python3 retrieval_system.py 42.058536 -87.677060 42.057120 -87.674897

ChinaTown, Chicago   
41.855250, -87.638077, 41.847162, -87.629216  
$python3 retrieval_system.py 41.855250 -87.638077 41.847162 -87.629216  
![ChinaTown]https://raw.github.com/Linco1n3/Aerial-Imagery-Retrieval/blob/master/ChinaTown.png

Coco Bango, Cancun   
21.132749, -86.747619, 21.131900, -86.746629   
$python3 retrieval_system.py 21.132749 -86.747619 21.131900 -86.746629   

Mosque, Istanbul    
41.006036, 28.975990, 41.004792, 28.977462    
$python3 retrieval_system.py 41.006036 28.975990 41.004792 28.977462  


## Authors

* **Yifan Le** 
* **Zhonghan Li**
* **Yunan Wu**
