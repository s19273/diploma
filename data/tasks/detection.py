import os
from datetime import datetime

import torch
from celery import shared_task
from data.core.utils import get_formatted_date
from data.models.image import ImageModel
from data.models.log_item import LogItem
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw
from rest_framework.generics import get_object_or_404


def static_vars(**kwargs):
    def set_statics(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return set_statics


@static_vars(device=None, mtcnn=None, prev_detected=0)
@shared_task
def detection(uuid, cur_session_id):

    image = get_object_or_404(ImageModel, uuid=uuid)

    if detection.device is None:
        print('Setting up PyTorch...')
        detection.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        detection.mtcnn = MTCNN(keep_all=True, device=detection.device)
        print(f'PyTorch working on a device: {detection.device}')

    imageName = image.image.open("r")  # path
    filepath = f"./mediafiles/{imageName}"
    frame = Image.open(filepath)

    boxes, _ = detection.mtcnn.detect(frame)
    boxes = [] if boxes is None else boxes
    frame_draw = frame.copy()
    draw = ImageDraw.Draw(frame_draw)
    faces = 0
    for box in boxes:
        faces = faces + 1
        draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)

    frame_draw.save(filepath)

    # get last log object for current session
    last_log = LogItem.objects.filter(
        image__session__session_id=cur_session_id
    ).last()
    last_faces_number = 0 if last_log == None else last_log.faces_number

    if faces != last_faces_number:
        datetime_now = datetime.now()
        time_string = get_formatted_date(datetime_now)
        eventInfo = f"[{time_string}] Detected faces: {faces}"

        LogItem.objects.create(
            faces_number=faces,
            message=eventInfo,
            image=image
        )

        detection.prev_detected = faces
        return f"\n\n{eventInfo}\n"
    else:
        image.delete()
        os.remove(filepath)
        return "\n\nNo changes detected\n"
