import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge
import cv2

from lane_follower_pkg.lane_detector import LaneDetector


class LaneFollowerNode(Node):
    def __init__(self):
        super().__init__('lane_follower_node')

        self.declare_parameter('show_gui', True)
        self.declare_parameter('lower_hsv', [13, 55, 70])
        self.declare_parameter('upper_hsv', [30, 255, 255])

        lower_hsv = self.get_parameter('lower_hsv').value
        upper_hsv = self.get_parameter('upper_hsv').value

        self.bridge = CvBridge()
        self.detector = LaneDetector(lower_hsv=lower_hsv, upper_hsv=upper_hsv)

        self.image_sub = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10
        )


        self.error_pub = self.create_publisher(Float32, '/lane_error', 10)
        self.annotated_pub = self.create_publisher(Image, '/annotated_image', 10)

        self.get_logger().info(
            f"Savdetektalo ROS 2 Node elindult! HSV tartomany: {lower_hsv} -> {upper_hsv}"
        )

    def image_callback(self, msg: Image):
        try:
            cv_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"cv_bridge konverzios hiba: {e}")
            return

        error, annotated_frame, mask = self.detector.process_frame(cv_frame)

        error_msg = Float32()
        error_msg.data = float(error)
        self.error_pub.publish(error_msg)

        annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding='bgr8')
        annotated_msg.header = msg.header
        self.annotated_pub.publish(annotated_msg)

        if self.get_parameter('show_gui').value:
            cv2.imshow("Lane Tracking Debug Feed", annotated_frame)
            cv2.imshow("Mask", mask)
            cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = LaneFollowerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
