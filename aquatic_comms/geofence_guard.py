import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
from mavros_msgs.srv import SetMode

class GeofenceGuardNode(Node):
    def __init__(self):
        super().__init__('geofence_guard_node')
        
        # حدود المنطقة المسموح للمركبة بالتحرك داخلها (مثال)
        self.declare_parameter('max_lat', 36.8000)
        self.declare_parameter('min_lat', 36.7000)
        self.declare_parameter('max_lon', 3.2000)
        self.declare_parameter('min_lon', 3.1000)

        self.gps_sub = self.create_subscription(
            NavSatFix, '/mavros/global_position/global', self.gps_callback, 10)
        self.set_mode_client = self.create_client(SetMode, '/mavros/set_mode')
        
        self.get_logger().info("Geofence Guard Active.")

    def gps_callback(self, msg: NavSatFix):
        lat = msg.latitude
        lon = msg.longitude

        max_lat = self.get_parameter('max_lat').value
        min_lat = self.get_parameter('min_lat').value
        max_lon = self.get_parameter('max_lon').value
        min_lon = self.get_parameter('min_lon').value

        if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
            self.get_logger().error(f"GEOFENCE BREACHED! Lat: {lat}, Lon: {lon}. Triggering RTL!")
            self.trigger_rtl_mode()

    def trigger_rtl_mode(self):
        if self.set_mode_client.wait_for_service(timeout_sec=1.0):
            req = SetMode.Request()
            req.custom_mode = 'RTL'  # Return To Launch (العودة إلى نقطة الانطلاق)
            self.set_mode_client.call_async(req)

def main(args=None):
    rclpy.init(args=args)
    node = GeofenceGuardNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
