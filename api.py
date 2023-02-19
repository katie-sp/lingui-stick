import modal
import os

OUTPUT_DIR = "/tmp/"

image = (
    modal.Image.debian_slim()
    .run_commands(
        "apt-get install -y libgl1-mesa-glx libglib2.0-0 wget")
    .pip_install("ultralytics")
)

stub = modal.Stub("lingui-stick", image=image)

if stub.is_inside():
    import cv2
    from ultralytics import YOLO
    import requests
    from io import BytesIO
    from PIL import Image
    
stub.sv = modal.SharedVolume()

@stub.function(shared_volumes={"/images": stub.sv}, timeout=600)
def detect_objects(image_path):
    
    # download model
    model = YOLO("yolov8n.pt")
    cats = model.names    # dictionary mapping IDs to category names (e.g. 0: person)
    
    # get image
    #response = requests.get(image_path)
    #image = Image.open(BytesIO(response.content))
    #image = np.asarray(image)

    # run YOLO on image
    #os.system("ln -s /runs/detect/predict /images")
    results = model.predict(source=image_path)#, save=True, save_txt=True)

    # Create mp4 of result
    out_image = results[0].orig_img[:,:,::-1]
    #out_image = Image.fromarray(out_image)
    #out_image.show()
    #out_image.save("/images/test.jpg")
    #os.system("ls -ltr /images/test")
    return out_image


@stub.local_entrypoint
def main(image_path: str = "https://images.squarespace-cdn.com/content/v1/5e1b73fb6eeb973ee1becfc4/1592675020070-2CPPWG2J34ZWURFKJC6P/custom-restaurant-tables-david-stine+4.jpg"):
    out_fn = detect_objects.call(image_path)
    print(f"writing results to {out_fn}")
    
@stub.webhook
def RUN(image_path: str = "https://images.squarespace-cdn.com/content/v1/5e1b73fb6eeb973ee1becfc4/1592675020070-2CPPWG2J34ZWURFKJC6P/custom-restaurant-tables-david-stine+4.jpg"):
    #return "HELLO?"
    return detect_objects.call(image_path)
   