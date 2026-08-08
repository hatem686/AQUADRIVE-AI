import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
import random


class ModernHybridCommsNode(Node):

    def __init__(self):
        super().__init__('hybrid_comms_manager')

        self.declare_parameter(
            'attenuation_threshold_db',
            20.0
        )

        self.declare_parameter(
            'check_interval_sec',
            1.0
        )

        self.channel_pub = self.create_publisher(
            String,
            '/comms/active_channel',
            10
        )

        self.diag_pub = self.create_publisher(
            DiagnosticArray,
            '/diagnostics',
            10
        )

        self.active_channel = "FIBER_OPTIC"

        interval = (
            self.get_parameter('check_interval_sec')
            .get_parameter_value()
            .double_value
        )

        self.timer = self.create_timer(
            interval,
            self.comms_monitoring_loop
        )

        self.get_logger().info(
            "Hybrid Comms ROS 2 Node initialized successfully."
        )

    def read_fiber_attenuation(self) -> float:
        return round(
            random.uniform(5.0, 35.0),
            2
        )

    def comms_monitoring_loop(self):

        threshold = (
            self.get_parameter('attenuation_threshold_db')
            .get_parameter_value()
            .double_value
        )

        current_attenuation = (
            self.read_fiber_attenuation()
        )

        if (
            current_attenuation > threshold
            and self.active_channel != "WIRELESS_4G_5G"
        ):

            self.active_channel = "WIRELESS_4G_5G"

            self.get_logger().warn(
                f"HIGH ATTENUATION "
                f"({current_attenuation} dB). "
                f"Switching -> WIRELESS_4G_5G"
            )

        elif (
            current_attenuation <= threshold
            and self.active_channel != "FIBER_OPTIC"
        ):

            self.active_channel = "FIBER_OPTIC"

            self.get_logger().info(
                f"SIGNAL RESTORED "
                f"({current_attenuation} dB). "
                f"Switching -> FIBER_OPTIC"
            )

        msg = String()
        msg.data = self.active_channel

        self.channel_pub.publish(msg)

        self.publish_diagnostics(
            current_attenuation,
            threshold
        )

    def publish_diagnostics(
        self,
        attenuation: float,
        threshold: float
    ):

        diag_array = DiagnosticArray()

        diag_array.header.stamp = (
            self.get_clock().now().to_msg()
        )

        status = DiagnosticStatus()

        status.name = (
            "Aquatic System: Hybrid Comms"
        )

        status.hardware_id = (
            "NvidiaJetson_Comms_v1"
        )

        status.level = (
            DiagnosticStatus.OK
            if self.active_channel == "FIBER_OPTIC"
            else DiagnosticStatus.WARN
        )

        status.message = (
            "Primary Fiber Tether"
            if self.active_channel == "FIBER_OPTIC"
            else "Failover Wireless"
        )

        status.values = [

            KeyValue(
                key="Current Attenuation (dB)",
                value=str(attenuation)
            ),

            KeyValue(
                key="Threshold (dB)",
                value=str(threshold)
            ),

            KeyValue(
                key="Active Channel",
                value=self.active_channel
            )
        ]

        diag_array.status.append(status)

        self.diag_pub.publish(diag_array)


def main(args=None):

    rclpy.init(args=args)

    node = ModernHybridCommsNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()
