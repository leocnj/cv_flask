# cv_flask

A Flask App for demoing openface's face processing CV capabilities

1. build a docker image by using

      `docker build -t cv_flask --file cv_flask.dockerfile`
   - note that the built image is large, more than 10 GB

2. run docker

      `docker run -it -p 5000:5000 cv_flask bash`

3. start Flask

   3.1 image
   
   `python app.py`

   - visit `localhost:5000` to use existing images; you can find sample images under images/
   - visit `localhost:5000/webrtc` to use your webcam to capture images
   - note: use Chrome's **incognito** mode to avoid Flask caching static images

   3.2  video

   `python app_video.py`

   - visit `localhost:5000` to use existing .mp4 videos; you can find sample videos under videos/
   - please try short videos to obtain results in a prompt way