## Steps:

```
git clone https://github.com/oschan77/lscm_unimap_pgm2pbstream.git
```

```
./autorun.sh
```

```
roslaunch ogm2pgbm ogm2pgbm.launch map_file:=/root/workspace/lobby/map.yaml record:=true
```

```
roslaunch cartographer_ros ogm2pgbm_my_robot.launch bag_filename:=/root/.ros/ogm2pgbm_sensordata.bag
```

```
cp /root/.ros/ogm2pgbm_sensordata.bag /root/.ros/ogm2pgbm_sensordata.bag.pbstream /root/workspace/
```

```
sudo chown ubuntu ./*
```