from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import time

token = 'Paste Your Token'

g_url = 'http://api.giscle.ml'

frame = 0

def extract_data(args):
    print(time.time() - t)
    print(args)
    for key in args['Output'].keys():
        if key != 'total_person':
            x,y,h,w = (args['Output'][str(key)])
            x,y,h,w = int(x),int(y),int(h),int(w)
            cv2.rectangle(frame, (x,y),(x+h,y+w), (255,255,255))

    cv2.imshow("frame",frame)

socketio = SocketIO(g_url, 80, LoggingNamespace)

socketio.emit('authenticate', {'token': token})

cam = cv2.VideoCapture(0)

frame_count = 1

while True:
    global t
    t = time.time()
    ret, frame = cam.read()
    if not ret:
        continue
    frame = cv2.resize(frame, (900, 600))
    encoded, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer)
    encoded_frame = encoded_frame.decode('utf-8')
    socketio.emit('count_people', {'data': encoded_frame})
    socketio.on('response', extract_data)
    socketio.wait(0.0001)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

socketio.disconnect()
cam.release()
