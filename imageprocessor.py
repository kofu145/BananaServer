import yolov5
class ImageProcessor:
    def __init__(self):
        self.model = yolov5.load('./best.pt')
        # set model parameters
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 100  # maximum number of detections per image
        self.model.names = ['Compost (Biodegradable)',
                       'Recycle (cardboard)',
                       'Recycle (glass)',
                       'Recycle (metal)',
                       'Recycle (paper)',
                       'Recycle (plastic)']

    def process_image(self, img):

        # perform inference
        #results = model(img, size=640)

        # inference with test time augmentation
        results = self.model(img, size=640, augment=True)

        # parse results
        predictions = results.pred[0]
        boxes = predictions[:, :4] # x1, y1, x2, y2
        scores = predictions[:, 4]
        categories = predictions[:, 5]
        labels = ['biodegradable', 'cardboard', 'glass', 'metal', 'paper', 'plastic']

        print(labels[int(categories[0])])
        results.print()

        # show detection bounding boxes on image

        # save results into "results/" folder
        results.save(save_dir='results/')

