import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
import random

class AquaticVisionNode(Node):
    def __init__(self):
        super().__init__('aquatic_vision_node')
        
        self.obstacle_pub = self.create_publisher(String, '/vision/obstacle_status', 10)
        self.diag_pub = self.create_publisher(DiagnosticArray, '/diagnostics', 10)
        
        self.declare_parameter('detection_distance_threshold_m', 3.0)
        self.timer = self.create_timer(0.5, self.process_vision_frame)
        
        self.get_logger().info("Aquatic Vision Obstacle Node Initialized.")

    def process_vision_frame(self):
        # محاكاة قراءة قياس مسافة أقرب عائق مائي بالأمتار
        detected_distance = round(random.uniform(0.5, 10.0), 2)
        threshold = self.get_parameter('detection_distance_threshold_m').get_parameter_value().double_value

        obstacle_state = "CLEAR"
        if detected_distance <= threshold:
            obstacle_state = "OBSTACLE_DETECTED"
            self.get_logger().warn(f"OBSTACLE NEARBY! Distance: {detected_distance}m")

        msg = String()
        msg.data = obstacle_state
        self.obstacle_pub.publish(msg)

        self.publish_diagnostics(detected_distance, obstacle_state)

    def publish_diagnostics(self, distance: float, status_str: str):
        diag_array = DiagnosticArray()
        diag_array.header.stamp = self.get_clock().now().to_msg()

        status = DiagnosticStatus()
        status.name = "Aquatic System: Vision AI"
        status.hardware_id = "Jetson_Orin_Camera"
        status.level = DiagnosticStatus.WARN if status_str == "OBSTACLE_DETECTED" else DiagnosticStatus.OK
        status.message = f"Obstacle State: {status_str}"

        status.values = [
            KeyValue(key="Detected Distance (m)", value=str(distance)),
            KeyValue(key="Obstacle Status", value=status_str)
        ]

        diag_array.status.append(status)
        self.diag_pub.publish(diag_array)

def main(args=None):
    rclpy.init(args=args)
    node = AquaticVisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
