import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SITLFailoverTester(Node):
    def __init__(self):
        super().__init__('sitl_failover_tester')
        self.pub = self.create_publisher(String, '/comms/active_channel', 10)
        self.timer = self.create_timer(4.0, self.inject_signal_drop)
        self.step = 0

    def inject_signal_drop(self):
        msg = String()
        if self.step % 2 == 0:
            msg.data = "FIBER_OPTIC"
            self.get_logger().info("[SIMULATION] Fiber Optic: STABLE")
        else:
            msg.data = "WIRELESS_4G_5G"
            self.get_logger().warn("[SIMULATION] Fiber Optic: FAULT INJECTED!")
        self.pub.publish(msg)
        self.step += 1

def main(args=None):
    rclpy.init(args=args)
    node = SITLFailoverTester()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
