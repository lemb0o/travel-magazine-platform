from .models import Image, Video
from common.miscellaneous import get_file_path


def create_image(img, target, target_img_name):
    img = Image(image=img, target=target)
    img._meta.get_field('image').upload_to = get_file_path(target_img_name)
    img.save()
    return True
    # target_ct = ContentType.objects.get_for_model(target)
    # if CreateImageForm(images).is_valid():
    #     img = Image(target_tmp=target_name, images=images, target=target)
    #     img.save()
    #     return True
    # else: return False


def create_video(vid, target, target_vid_name):
    vid = Video(video=vid, target=target)
    vid._meta.get_field('video').upload_to = get_file_path(target_vid_name)
    vid.save()
    return True
