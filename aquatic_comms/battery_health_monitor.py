import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState
from mavros_msgs.srv import SetMode

class BatteryHealthMonitor(Node):
    def __init__(self):
        super().__init__('battery_health_monitor')
        
        self.declare_parameter('critical_battery_percentage', 0.15) # 15%
        self.battery_sub = self.create_subscription(
            BatteryState, '/mavros/battery', self.battery_callback, 10)
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        
        self.emergency_triggered = False
        self.get_logger().info("Battery Health Monitor Active.")

    def battery_callback(self, msg: BatteryState):
        critical_threshold = self.get_parameter('critical_battery_percentage').value
        
        if msg.percentage <= critical_threshold and not self.emergency_triggered:
            self.emergency_triggered = True
            self.get_logger().fatal(f"CRITICAL BATTERY LEVEL ({int(msg.percentage * 100)}%)! Returning to Shore.")
            self.trigger_rtl_mode()

    def trigger_rtl_mode(self):
        if self.set_mode_client.wait_for_service(timeout_sec=1.0):
            req = SetMode.Request()
            req.custom_mode = 'RTL'
            self.set_mode_client.call_async(req)

def main(args=None):
    rclpy.init(args=args)
    node = BatteryHealthMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
