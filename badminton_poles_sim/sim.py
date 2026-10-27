import math
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import Image, CameraInfo
from visualization_msgs.msg import Marker, MarkerArray

class Sim(Node):
    def __init__(self):
        super().__init__('badminton_poles_sim')
        for k,v in [('robot_x',-4.0),('robot_y',0.0),('robot_yaw',0.0),('pole_spacing',6.1),('pole_height',1.55),('camera_height',0.8),('hfov_deg',100.0)]: self.declare_parameter(k,v)
        self.x=self.p('robot_x'); self.y=self.p('robot_y'); self.yaw=self.p('robot_yaw')
        self.markers=self.create_publisher(MarkerArray,'/field_markers',10)
        self.image=self.create_publisher(Image,'/sim_camera/image_raw',10)
        self.info=self.create_publisher(CameraInfo,'/sim_camera/camera_info',10)
        self.create_subscription(PoseWithCovarianceStamped,'/initialpose',self.pose,10)
        self.create_timer(0.2,self.tick)
    def p(self,k): return self.get_parameter(k).value
    def pose(self,msg):
        if msg.header.frame_id and msg.header.frame_id != 'map':
            self.get_logger().warning('Initial pose must use map frame'); return
        p=msg.pose.pose; self.x=p.position.x; self.y=p.position.y
        q=p.orientation; self.yaw=math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z))
    def marker(self,i,typ,x,y,z,sx,sy,sz,color,yaw=0.0):
        m=Marker(); m.header.frame_id='map'; m.header.stamp=self.get_clock().now().to_msg(); m.ns='scene'; m.id=i; m.type=typ; m.action=Marker.ADD
        m.pose.position.x=float(x); m.pose.position.y=float(y); m.pose.position.z=float(z); m.pose.orientation.z=math.sin(yaw/2); m.pose.orientation.w=math.cos(yaw/2)
        m.scale.x=float(sx); m.scale.y=float(sy); m.scale.z=float(sz); m.color.r,m.color.g,m.color.b,m.color.a=color
        return m
    def tick(self):
        d=self.p('pole_spacing')/2; h=self.p('pole_height')
        arr=MarkerArray(); arr.markers=[self.marker(0,Marker.CUBE,-3.35,0,-0.03,13.4,6.1,0.05,(0.09,0.37,0.23,1)),self.marker(1,Marker.CYLINDER,0,d,h/2,0.08,0.08,h,(0.92,0.92,0.92,1)),self.marker(2,Marker.CYLINDER,0,-d,h/2,0.08,0.08,h,(0.92,0.92,0.92,1)),self.marker(3,Marker.CUBE,0,0,1.1,0.025,2*d,0.8,(0.85,0.85,0.85,0.32)),self.marker(4,Marker.CUBE,self.x,self.y,0.18,0.6,0.45,0.36,(0.1,0.35,0.95,1),self.yaw),self.marker(5,Marker.ARROW,self.x,self.y,0.42,0.9,0.08,0.08,(1.,0.35,0.,1),self.yaw)]
        self.markers.publish(arr)
        w,h_img=640,480; f=w/(2*math.tan(math.radians(self.p('hfov_deg'))/2)); cx=w/2; cy=h_img/2
        img=np.zeros((h_img,w,3),dtype=np.uint8); img[:h_img//2]=(105,105,105); img[h_img//2:]=(45,100,55)
        for yy in [d,-d]:
            dx=-self.x; dy=yy-self.y
            forward=math.cos(self.yaw)*dx+math.sin(self.yaw)*dy; left=-math.sin(self.yaw)*dx+math.cos(self.yaw)*dy
            if forward<=0.1: continue
            u=round(cx-f*left/forward); top=round(cy-f*(h-self.p('camera_height'))/forward); bottom=round(cy+f*self.p('camera_height')/forward); width=max(2,round(f*0.08/forward))
            if -width <= u < w+width:
                cv2.rectangle(img,(u-width//2,max(-1000,top)),(u+width//2,min(2000,bottom)),(235,235,235),-1)
        stamp=self.get_clock().now().to_msg(); out=Image(); out.header.stamp=stamp; out.header.frame_id='sim_camera_optical'; out.height=h_img; out.width=w; out.encoding='bgr8'; out.step=w*3; out.data=img.tobytes(); self.image.publish(out)
        info=CameraInfo(); info.header=out.header; info.width=w; info.height=h_img; info.distortion_model='plumb_bob'; info.d=[0.0]*5; info.k=[f,0.,cx,0.,f,cy,0.,0.,1.]; info.r=[1.,0.,0.,0.,1.,0.,0.,0.,1.]; info.p=[f,0.,cx,0.,0.,f,cy,0.,0.,0.,1.,0.]; self.info.publish(info)

def main():
    rclpy.init(); node=Sim()
    try: rclpy.spin(node)
    finally: node.destroy_node(); rclpy.shutdown()
if __name__=='__main__': main()
