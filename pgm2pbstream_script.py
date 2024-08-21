import contextlib
import os
import shutil
import signal
import subprocess
import time

from config import PROJECT_PATH


@contextlib.contextmanager
def managed_subprocess(command, shell=True):
    process = subprocess.Popen(command, shell=shell, preexec_fn=os.setsid)
    try:
        yield process
    finally:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except:
            return


def clean_ros_environment():
    def run_command(cmd):
        try:
            subprocess.run(
                cmd, shell=True, check=True, stderr=subprocess.PIPE, text=True
            )
            print(f"Successfully executed: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {cmd}")
            print(f"Error: {e.stderr}")

    run_command("rosnode kill /laserMapping")

    time.sleep(2)

    # 检查并终止 ROS 相关进程
    ros_processes = ["roscore", "rosmaster", "rosout"]
    for proc in ros_processes:
        run_command(f"killall {proc}")
        time.sleep(1)

        # 如果还在运行，则强制终止
        run_command(f"killall -9 {proc}")

    print("ROS environment cleanup completed.")


def rosbag2pcd(input_file_path: str, output_file_path: str, ros_type: str):
    # input_file_path: pgm_folder
    # output_file_path: pbstream
    pgm_folder_name = input_file_path.split("/")[-1]
    tmp_pgm_folder_path = os.path.join(
        f"/home/breeze/Desktop/workplace/unimap_pgm2pbstream/workplace/PGM/{pgm_folder_name}"
    )
    print("copying...")
    shutil.copy(input_file_path, tmp_pgm_folder_path)
    os.chdir("/home/breeze/Desktop/workplace/unimap_pgm2pbstream")

    print("transformer set up")
    command1 = f'docker exec pgm2pbstream /bin/bash -c "roslaunch ogm2pgbm ogm2pgbm.launch map_file:=/root/workspace/lobby/map.yaml record:=true"'
    command2 = f'docker exec pgm2pbstream /bin/bash -c "roslaunch cartographer_ros ogm2pgbm_my_robot.launch bag_filename:=/root/.ros/ogm2pgbm_sensordata.bag"'
    command3 = f'docker exec pgm2pbstream /bin/bash -c "cp /root/.ros/ogm2pgbm_sensordata.bag /root/.ros/ogm2pgbm_sensordata.bag.pbstream /root/workspace/"'

    with managed_subprocess(command1) as proc1:
        print("transforming...")
        with managed_subprocess(command2) as proc2:
            proc2.wait()
            with managed_subprocess(command3) as proc3:
                proc3.wait()
    time.sleep(2)
    clean_ros_environment()
    print("transform finished!")

    os.chdir(PROJECT_PATH)
    shutil.copy(tmp_pgm_folder_path, output_file_path)
    print({"status": "Success", "message": "Success"})
    return {"status": "Success", "message": "Success"}
