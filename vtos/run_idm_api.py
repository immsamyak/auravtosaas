import os
import shutil
from gradio_client import Client, handle_file

def run_idm_vton_api():
    print("Connecting to free Hugging Face IDM-VTON API...")
    try:
        client = Client("yisol/IDM-VTON")
    except Exception as e:
        print("Failed to connect to API:", e)
        return

    base_dir = "/Users/saamyak/COllege Project/Aura/vtos"
    result_dir = os.path.join(base_dir, "result_api")
    os.makedirs(result_dir, exist_ok=True)
    
    persons = [
        "person_pose_1_1787805281017.jpg",
        "person_pose_2_1787805296588.jpg",
        "person_pose_3_1787805308792.jpg",
        "person_pose_4_1787805320702.jpg",
        "person_pose_5_1787805333398.jpg"
    ]
    
    garments = [
        ("garment_1_1787805345957.jpg", "blue denim jacket"),
        ("garment_2_1787805358598.jpg", "yellow hoodie"),
        ("garment_3_1787805369676.jpg", "green knitted sweater"),
        ("garment_4_1787805383479.jpg", "black leather jacket"),
        ("garment_5_1787805395715.jpg", "white button-up shirt")
    ]
    
    total = len(persons) * len(garments)
    count = 1
    
    for p_idx, person in enumerate(persons, 1):
        if p_idx != 2:
            count += len(garments)
            continue
        for g_idx, (garment, desc) in enumerate(garments, 1):
            print(f"\n--- Processing Pair {count}/{total} via API ---")
            print(f"Person {p_idx}: {person}")
            print(f"Garment {g_idx}: {garment} ({desc})")
            
            p_path = os.path.join(base_dir, person)
            g_path = os.path.join(base_dir, garment)
            
            output_name = f"idm_vton_p{p_idx}_g{g_idx}.jpg"
            output_path = os.path.join(result_dir, output_name)
            
            if os.path.exists(output_path):
                print(f"Skipping pair {count} because {output_path} already exists.")
                count += 1
                continue
            
            try:
                # Call the Hugging Face Gradio API
                result = client.predict(
                    dict={"background": handle_file(p_path), "layers": [], "composite": None},
                    garm_img=handle_file(g_path),
                    garment_des=desc,
                    is_checked=True, # Use auto-generated mask
                    is_checked_crop=False, # Use auto-crop
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )
                
                # The API returns a tuple where the first element is the output image path
                output_image_path = result[0]
                
                output_name = f"idm_vton_p{p_idx}_g{g_idx}.jpg"
                output_path = os.path.join(result_dir, output_name)
                
                shutil.copy(output_image_path, output_path)
                print(f"Success! Saved as {output_path}")
            except Exception as e:
                print(f"Error on pair {count}: {e}")
            
            count += 1

if __name__ == "__main__":
    run_idm_vton_api()

