import os
import django
import glob
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.fitting.models import AIAvatarModel

def run():
    print("Seeding AI Avatars...")
    # Clear existing to prevent duplicates during dev
    AIAvatarModel.objects.all().delete()
    
    avatar_dir = '/Users/saamyak/.gemini/antigravity-ide/brain/94cd3e40-311f-4484-a309-032f2976c250'
    files = glob.glob(f"{avatar_dir}/ai_model_*.jpg")
    
    for fpath in files:
        filename = os.path.basename(fpath)
        # Parse ai_model_female_1_1787194454999.jpg
        parts = filename.split('_')
        gender = 'FEMALE' if parts[2] == 'female' else 'MALE'
        num = parts[3]
        name = f"Professional Model {num}"
        
        with open(fpath, 'rb') as f:
            avatar = AIAvatarModel(
                name=name,
                gender=gender
            )
            avatar.image.save(filename, File(f), save=True)
            print(f"Created {name} ({gender})")
            
if __name__ == '__main__':
    run()
