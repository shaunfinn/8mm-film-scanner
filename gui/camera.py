import cv2
import time
import config



class cameraControl():
	
	def init_capture(self):
		self.camera = cv2.VideoCapture(0)
		self.camera.set(3,1920)
		self.camera.set(4,1080)
		
	def init_writer(self):
		fourcc = cv2.VideoWriter_fourcc(*'FFV1')
		self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (1920,1080))

	def preview_frame(self):
		camera = cv2.VideoCapture(0)
		camera.set(3,1920)
		camera.set(4,1080)
		return_value, image = camera.read()
		cv2.imwrite('preview'+'.png', image)
		print("image_update")
		camera.release()
		
	def grab_10_frames(self):
		camera = cv2.VideoCapture(0)
		for i in range(10):
			return_value, image = camera.read()
			cv2.imwrite('frames/'+str(i)+'.png', image)
			print("image" + str(i))
			time.sleep(0.5)
		camera.release()

	def capture_frame(self):
		#when capturing
		return_value, image = self.camera.read()
		self.out.write(image)
		#cv2.imwrite('frames/'+str(config.frame_cnt)+'.png', image)
		#print("captured frame ", config.frame_cnt)
		
	
	def stop_capture(self):
		self.camera.release()
		self.out.release()
		print("released")



		
	
