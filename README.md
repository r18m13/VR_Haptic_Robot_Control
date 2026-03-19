# Real-Time Robotic Manipulation with Haptic Teleoperation and VR Control

An end-to-end teleoperation system enabling **low-latency, high-precision robotic manipulation** using a Novint Falcon haptic device and immersive VR interface, integrated with ROS2-based control pipelines.

---

## 🚀 Overview

This project implements a **real-time human-in-the-loop robotic manipulation system** that bridges haptic input, VR visualization, and robot control.

The system allows an operator to intuitively control a robotic arm using a **3-DOF haptic device**, with motion mapped into robot workspace coordinates and executed through a ROS2 control pipeline.

Key capabilities include:

* Real-time teleoperation with motion scaling
* Low-latency control loop for stable manipulation
* VR-based visualization and interaction (Unity OpenXR)
* Modular ROS2 architecture for extensibility and deployment

---

## 🎥 Demo

### Haptic Teleoperation + Control + Testing using Panda Arm

*https://www.youtube.com/watch?v=pp2FSn9sudI&list=PLwUycyXYUfwRI-hcJVh3UcAR0WU5qAu_A&index=1*


> Demonstrates smooth end-effector tracking, intuitive control, and stable interaction under continuous input.

---

## 🧠 System Architecture

The system is designed as a **modular, distributed robotics pipeline**:

```
Novint Falcon (Haptic Input)
        ↓
C++ Interface (libnifalcon)
        ↓
ROS2 Node (Input Processing)
        ↓
Control Mapping + Motion Scaling
        ↓
Robot Control Pipeline (ROS2)
        ↓
URDF Robot Model (Gazebo / Real Robot)
        ↑
Unity VR Interface (ROS-TCP Connector)
```

### Core Components

* **Haptic Interface Layer**

  * Reads 3D positional input from Falcon device
  * Converts raw input into usable control signals

* **Control Mapping Layer**

  * Applies motion scaling and coordinate transformations
  * Ensures stable and intuitive operator control

* **ROS2 Middleware**

  * Handles communication between perception, control, and visualization
  * Enables modular and scalable system design

* **VR Interface (Unity OpenXR)**

  * Provides immersive visualization of robot state
  * Enables interactive teleoperation feedback loop

---

## ⚙️ Key Features

* Real-time haptic teleoperation using Novint Falcon
* Low-latency control pipeline for responsive manipulation
* Motion scaling for precision control in constrained workspaces
* ROS2-based modular system design
* VR integration for immersive robot interaction
* URDF-based robot modeling and simulation in Gazebo

---

## 🧪 Technical Highlights

* Designed a **real-time control loop** for continuous teleoperation
* Implemented **motion scaling strategies** to stabilize operator input
* Integrated **C++ hardware interface (libnifalcon)** with ROS2 nodes
* Built a **distributed control architecture** across VR, ROS2, and simulation
* Achieved **low-latency response suitable for real-time manipulation tasks**
* Structured system for **simulation-to-hardware transfer**

---

## 📁 Repository Structure

```
├── src/
│   ├── falcon_interface/        # C++ interface for Novint Falcon
│   ├── robot_control/           # ROS2 control and teleoperation nodes
│   ├── vr_interface/            # Unity + ROS TCP integration
│
├── urdf/                        # Robot descriptions (URDF/XACRO)
├── meshes/                      # STL and mesh assets
├── launch/                      # ROS2 launch files
├── config/                      # Configuration files
└── README.md
```

---

## 🔧 Setup

### Prerequisites

* Ubuntu (20.04+ recommended)
* ROS2 (Foxy / Humble)
* Unity (for VR interface)
* Novint Falcon device

---

### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install build-essential cmake libusb-1.0-0-dev
```

---

### 2. Install libnifalcon

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

### 3. Configure USB Permissions

```bash
sudo nano /etc/udev/rules.d/99-novint.rules
```

Add:

```bash
SUBSYSTEM=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="cb48", MODE="0666"
```

Reload rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

---

### 4. Build ROS2 Workspace

```bash
colcon build
source install/setup.bash
```

---

## ▶️ Usage

### Start Falcon Interface

```bash
ros2 run falcon_interface falcon_node
```

### Launch Robot Simulation

```bash
ros2 launch robot_control simulation.launch.py
```

### Start VR Interface

* Open Unity project
* Enable ROS-TCP Connector
* Run the teleoperation scene

---

## 🔬 Applications

* Teleoperation for manipulation tasks
* Human-in-the-loop robotics systems
* Remote robotic control in hazardous environments
* VR-based robotic training and simulation

---

## 🔬 Future Work

* Integration with MoveIt2 for advanced motion planning
* Visual servoing using real-time perception feedback
* Deployment on physical robotic arm (UR5e)
* Force feedback modeling for enhanced haptics
* Multi-modal perception integration

---

## 📌 Key Takeaways

This project demonstrates:

* End-to-end robotics system integration
* Real-time control system design
* Human-robot interaction via haptics and VR
* Scalable ROS2-based architecture

---

## 👤 Author

Bhargava Ram Malladi
Robotics Engineer | Autonomous Systems | Manipulation | Perception

---
