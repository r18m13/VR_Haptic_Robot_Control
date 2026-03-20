#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>

#include <iostream>
#include <csignal>
#include <array>
#include <memory>

#include "falcon/core/FalconDevice.h"
#include "falcon/firmware/FalconFirmwareNovintSDK.h"
#include "falcon/kinematic/FalconKinematicStamper.h"

using namespace libnifalcon;

bool run_app = true;

void sigproc(int)
{
    run_app = false;
}

// Falcon workspace limits (meters)
const double FALCON_MIN = -0.06;
const double FALCON_MAX =  0.06;

// Max robot velocity (m/s)
const double MAX_VEL = 0.2;

// Deadzone to prevent drift
const double DEADZONE = 0.05;

// Normalize [-0.06, 0.06] → [-1, 1]
double normalize(double val)
{
    double norm = (val - FALCON_MIN) / (FALCON_MAX - FALCON_MIN);
    norm = norm * 2.0 - 1.0;
    return norm;
}

// Apply deadzone
double applyDeadzone(double val)
{
    if (std::abs(val) < DEADZONE)
        return 0.0;
    return val;
}

int main(int argc, char** argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("falcon_servo_node");

    auto pub = node->create_publisher<geometry_msgs::msg::TwistStamped>(
        "/servo_node/delta_twist_cmds", 10);

    signal(SIGINT, sigproc);
#if !defined(WIN32)
    signal(SIGQUIT, sigproc);
#endif

    std::unique_ptr<FalconDevice> falcon(new FalconDevice());

    if(!falcon->open(0))
    {
        RCLCPP_ERROR(node->get_logger(), "Could not open Falcon device");
        return 1;
    }

    falcon->setFalconFirmware<FalconFirmwareNovintSDK>();

    if(!falcon->isFirmwareLoaded())
    {
        for(int i = 0; i < 10; ++i)
        {
            if(falcon->loadFirmware(10, false))
                break;
        }

        if(!falcon->isFirmwareLoaded())
        {
            RCLCPP_ERROR(node->get_logger(), "Firmware load failed");
            return 1;
        }
    }

    falcon->setFalconKinematic<FalconKinematicStamper>();

    std::array<double, 3> position;

    rclcpp::Rate rate(200);  // High frequency for servoing

    RCLCPP_INFO(node->get_logger(), "Falcon → MoveIt Servo node started");

    while (rclcpp::ok() && run_app)
    {
        if(!falcon->runIOLoop())
            continue;

        position = falcon->getPosition();

        // Normalize
        double nx = applyDeadzone(normalize(position[0]));
        double ny = applyDeadzone(normalize(position[1]));
        double nz = applyDeadzone(normalize(position[2]));

        // Scale to velocity
        geometry_msgs::msg::TwistStamped msg;
        msg.header.stamp = node->get_clock()->now();
        msg.header.frame_id = "base_link";

        msg.twist.linear.x = nx * MAX_VEL;
        msg.twist.linear.y = ny * MAX_VEL;
        msg.twist.linear.z = nz * MAX_VEL;

        // No rotation for now
        msg.twist.angular.x = 0.0;
        msg.twist.angular.y = 0.0;
        msg.twist.angular.z = 0.0;

        pub->publish(msg);

        rclcpp::spin_some(node);
        rate.sleep();
    }

    rclcpp::shutdown();
    return 0;
}