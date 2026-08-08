import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from mavros_msgs.srv import SetMode
from mavros_msgs.msg import State

class PixhawkFailoverBridge(Node):
    def __init__(self):
        super().__init__('pixhawk_failover_bridge')
        
        self.comms_sub = self.create_subscription(
            String, '/comms/active_channel', self.comms_callback, 10)
        self.obstacle_sub = self.create_subscription(
            String, '/vision/obstacle_status', self.obstacle_callback, 10)
        self.mavros_state_sub = self.create_subscription(
            State, '/mavros/state', self.mavros_state_callback, 10)
        
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        
        self.current_channel = "FIBER_OPTIC"
        self.pixhawk_connected = False
        self.obstacle_detected = False

    def mavros_state_callback(self, msg: State):
        self.pixhawk_connected = msg.connected

    def obstacle_callback(self, msg: String):
        if msg.data == "OBSTACLE_DETECTED" and not self.obstacle_detected:
            self.obstacle_detected = True
            self.get_logger().warn("Vision Alert: Obstacle close! Switching Pixhawk to BRAKE/HOLD.")
            self.trigger_pixhawk_mode('HOLD')
        elif msg.data == "CLEAR":
            self.obstacle_detected = False

    def comms_callback(self, msg: String):
        previous_channel = self.current_channel
        self.current_channel = msg.data

        # 1. حالة الانقطاع: التحويل إلى وضع الانتظار عند فقدان الألياف
        if previous_channel == "FIBER_OPTIC" and self.current_channel == "WIRELESS_4G_5G":
            self.get_logger().warn("Fiber Link Broken! Switching to Failover Wireless & Hold.")
            self.trigger_pixhawk_mode('HOLD')

        # 2. حالة الاستعادة الآلية: العودة إلى الوضع الذاتي عند استقرار الاتصال
        elif previous_channel == "WIRELESS_4G_5G" and self.current_channel == "FIBER_OPTIC":
            if not self.obstacle_detected:
                self.get_logger().info("Fiber Link Restored & Route Clear! Resuming AUTO Navigation.")
                self.trigger_pixhawk_mode('AUTO')

    def trigger_pixhawk_mode(self, custom_mode: str):
        if not self.pixhawk_connected or not self.set_mode_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error("Pixhawk unavailable for mode change!")
            return
        req = SetMode.Request()
        req.custom_mode = custom_mode
        self.set_mode_client.call_async(req)

def main(args=None):
    rclpy.init(args=args)
    node = PixhawkFailoverBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
