FROM ros:humble-ros-base

# تثبيت الاعتمادات المطلوبة لـ MAVROS وحزم التشخيص
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    wget \
    ros-humble-mavros \
    ros-humble-mavros-extras \
    ros-humble-diagnostic-msgs \
    && rm -rf /var/lib/apt/lists/*

# تنزيل قواعد بيانات GeographicLib المعتمدة لـ MAVROS
RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh \
    && chmod +x install_geographiclib_datasets.sh \
    && ./install_geographiclib_datasets.sh \
    && rm install_geographiclib_datasets.sh

# إعداد مساحة العمل وبناء الحزمة
WORKDIR /ros2_ws/src/aquatic_comms
COPY . .

WORKDIR /ros2_ws
RUN . /opt/ros/humble/setup.sh && colcon build --symlink-install

# تهيئة البيئة عند دخول الحاوية
ENTRYPOINT ["/bin/bash", "-c", "source /ros2_ws/install/setup.bash && exec \"$@\"", "--"]
CMD ["ros2", "launch", "aquatic_comms", "aquatic_system.launch.py"]
