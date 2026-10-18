# 1. Grafikus ablakok engedélyezése a gazdagépen
xhost +local:docker

# 2. Docker konténer indítása (a becsatolással)
docker run -it --rm \
  --name ros2_dev \
  --net=host \
  --env="DISPLAY=$DISPLAY" \
  --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --volume="$HOME/ros2_ws:/root/ros2_ws" \
  --device=/dev/video0:/dev/video0 \
  osrf/ros:jazzy-desktop \
  bash



# 1. Lépj be a workspace-be
cd /root/ros2_ws

# 2. Biztos ami biztos, telepítsük a kameracsomagot
apt-get update && apt-get install -y ros-jazzy-v4l2-camera

# 3. Fordítsd le a csomagot
colcon build --packages-select lane_follower_pkg --symlink-install

# 4. Töltsd be a környezetet
source install/setup.bash

# 5. Indítsd el a launch fájllal!
ros2 launch lane_follower_pkg lane_follower.launch.py


