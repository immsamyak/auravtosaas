import os
import django
import sys

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from apps.fitting.models import AIAvatarModel
from django.core.files import File

# Clear existing avatars if any
# AIAvatarModel.objects.all().delete()

poses = [
    {'file': 'person_pose_1_1787805281017.jpg', 'name': 'Person 1', 'gender': 'MALE'},
    {'file': 'person_pose_2_1787805296588.jpg', 'name': 'Person 2', 'gender': 'MALE'},
    {'file': 'person_pose_3_1787805308792.jpg', 'name': 'Person 3', 'gender': 'MALE'},
    {'file': 'person_pose_4_1787805320702.jpg', 'name': 'Person 4', 'gender': 'FEMALE'},
    {'file': 'person_pose_5_1787805333398.jpg', 'name': 'Person 5', 'gender': 'FEMALE'},
]

vtos_dir = os.path.join(os.path.dirname(__file__), 'vtos')

for pose in poses:
    path = os.path.join(vtos_dir, pose['file'])
    if os.path.exists(path):
        if not AIAvatarModel.objects.filter(name=pose['name']).exists():
            with open(path, 'rb') as f:
                avatar = AIAvatarModel(name=pose['name'], gender=pose['gender'], is_active=True)
                avatar.image.save(pose['file'], File(f), save=True)
                print(f"Created AI Avatar: {pose['name']}")
        else:
            print(f"AI Avatar {pose['name']} already exists.")
    else:
        print(f"File not found: {path}")

print("Done creating AI Avatars.")
