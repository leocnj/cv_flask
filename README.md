# cv_flask

A Flask App for demoing openface's face processing CV capabilities

1. Installations on host
   - openface
     - use [this repo](https://github.com/leocnj/docker-images) to build a docker image named as `openface_v1.0`
     - Flask App will use the built docker to do facial CV processing
   - FFMPEG
     - openface saves the videos with visualizations in .AVI format. For showing in browsers, need convert it to .mp4 by using FFMPEG
   - Flask
2. CV demo for image inputs
   - `python app.py`
   - visit `127.0.0.1:5000` to use existing images; you can find sample images under images/
   - visit `127.0.0.1:5000/webrtc` to use your webcam to capture images
     - note: use Chrome's **incognito** mode to avoid Flask caching static images
3. CV demo for video (.mp4) inputs
   - `python app_video.py`
   - visit `127.0.0.1:5000` to use existing .mp4 videos; you can find sample videos under videos/
   - please try short videos to obtain results in a prompt way
