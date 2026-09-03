import os
import sys
import platform
import socket
import urllib.request
import urllib.error
import json
import uuid

def verify_license():
    # If we are just collecting static files during Docker build, skip license check
    if len(sys.argv) > 1 and sys.argv[1] == 'collectstatic':
        return
        
    try:
        from dotenv import load_dotenv
        # Find .env at project root (backend/.env)
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        load_dotenv(env_path)
    except ImportError:
        pass

    license_key = os.environ.get('AURA_LICENSE_KEY')
    if not license_key:
        print("\n\033[91m[CRITICAL ERROR] AURA_LICENSE_KEY is missing from environment variables!\033[0m")
        print("Please purchase a valid license from CodeCanyon and add it to your .env file.")
        sys.exit(1)

    # Gather machine specs for tracking
    machine_info = {
        "os": platform.system() + " " + platform.release(),
        "hostname": socket.gethostname(),
        "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                        for ele in range(0,8*6,8)][::-1])
    }

    # API Endpoint
    # We now strictly ping the live Hostinger License Validation Server
    default_url = "https://license.alvicsxinfo.tech/api/verify"
    api_url = os.environ.get('LICENSE_SERVER_URL', default_url)
    
    data = json.dumps({
        "key": license_key,
        "machineInfo": machine_info
    }).encode('utf-8')

    req = urllib.request.Request(api_url, data=data, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'Aura-Licensing-Client/1.0'
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            if not result.get("valid"):
                print(f"\n\033[91m[LICENSE REVOKED] {result.get('message', 'Invalid License')}\033[0m")
                sys.exit(1)
            else:
                # Valid license, continue booting
                pass
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("\n\033[91m[LICENSE REVOKED] Your AURA license is invalid, revoked, or expired.\033[0m")
            print("Please contact support or purchase a new key on CodeCanyon.")
            sys.exit(1)
        else:
            print(f"\n\033[93m[WARNING] License server returned HTTP {e.code}. Assuming offline grace period.\033[0m")
    except Exception as e:
        # If server is completely unreachable, we block execution for strict piracy control
        print(f"\n\033[91m[LICENSE SERVER OFFLINE] Could not reach the license validation server at {api_url}.\033[0m")
        print("AURA cannot boot without an active internet connection to verify your purchase.")
        print(f"Error details: {e}")
        sys.exit(1)
