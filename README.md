# Real-Time Haptic Teleoperation using Novint Falcon and MoveIt Servo (ROS2)

A high-frequency teleoperation node that converts Novint Falcon haptic input into real-time Cartesian velocity commands for robotic manipulation using MoveIt Servo.

---

## 🚀 Overview

This project implements a **real-time control interface** between a Novint Falcon haptic device and a robotic manipulator via ROS2.

The system reads 3D positional input from the Falcon, processes it through normalization and filtering, and publishes velocity commands to:

```
/servo_node/delta_twist_cmds
```

This enables **smooth, intuitive teleoperation** of a robotic arm using MoveIt Servo.

---

## ⚙️ Key Features

* Real-time haptic teleoperation (200 Hz control loop)
* Direct integration with MoveIt Servo
* Cartesian velocity control using `TwistStamped`
* Input normalization from device workspace to robot workspace
* Deadzone filtering to eliminate drift and noise
* Firmware handling and device initialization for Novint Falcon

---

## 🧠 System Pipeline

```
Novint Falcon Input
        ↓
libnifalcon (C++ Interface)
        ↓
Position Normalization [-0.06, 0.06] → [-1, 1]
        ↓
Deadzone Filtering
        ↓
Velocity Scaling (Max: 0.2 m/s)
        ↓
ROS2 Publisher (/servo_node/delta_twist_cmds)
        ↓
MoveIt Servo → Robot Motion
```

---

## 🧪 Technical Highlights

* Implements a **200 Hz real-time control loop** for responsive teleoperation
* Uses **TwistStamped commands** for compatibility with MoveIt Servo
* Applies **workspace normalization** to map Falcon input to robot motion space
* Introduces **deadzone filtering** to suppress unintended motion
* Integrates **low-level hardware control (libnifalcon)** with ROS2 middleware

---

## 📦 Dependencies

* ROS2 (Foxy / Humble)
* MoveIt Servo
* libnifalcon
* geometry_msgs

---

## 🔧 Setup

### Install Dependencies

```bash
sudo apt-get update
sudo apt-get install build-essential cmake libusb-1.0-0-dev
```

---

### Install libnifalcon

```bash
git clone https://github.com/libnifalcon/libnifalcon
cd libnifalcon
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```

---

### Configure USB Permissions

```bash
sudo nano /etc/udev/rules.d/99-novint.rules
```

Add:

```
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="cb48", MODE="0666"
```

Reload:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

### Build ROS2 Workspace

```bash
colcon build
source install/setup.bash
```

---

## ▶️ Usage

### Run the Falcon Teleoperation Node

```bash
ros2 run falcon_interface falcon_servo_node
```

Ensure MoveIt Servo is running and subscribed to:

```
/servo_node/delta_twist_cmds
```

---

## 📐 Control Details

### Workspace Mapping

* Falcon range: `[-0.06, 0.06] meters`
* Normalized to: `[-1, 1]`
* Scaled to velocity: `±0.2 m/s`

---

### Deadzone Filtering

* Threshold: `0.05`
* Prevents drift from small unintended inputs

---

## 🎥 Demo

### Haptic Teleoperation + Control + Testing using Panda Arm

*https://www.youtube.com/watch?v=pp2FSn9sudI&list=PLwUycyXYUfwRI-hcJVh3UcAR0WU5qAu_A&index=1*

### VR Integration
https://youtube.com/shorts/qAZyyxqJ7i8

> Demonstrates smooth end-effector tracking, intuitive control, and stable interaction under continuous input.

---

## 👤 Author

Bhargava Ram Malladi
Robotics Engineer | ROS2 | Manipulation | Real-Time Control
