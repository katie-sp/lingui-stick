# lingui-stick

* The model notebook contains code for running the YOLOv8 image segmentation model; it's just a few lines! Below it is my first attempt, where I used a Torch Mask RCNN model that I'm more comfortable with, but which yielded worse results.

* The API script contains my first attempt at creating a Modal API to move images from Wix to my model, and then to return the labeled images to Wix. I was unsuccessful so far with the latter part of the process, but I am actively trying to figure it out and fix it in the future!

* Runs contains some real, labeled images that represent the kinds of images I would expect a typical LinguiStick user to upload and learn from. You can check them out (or run the notebook on your own images and get your own labeled copies!)
