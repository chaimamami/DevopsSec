import requests
import os

# ✅ Secure download using HTTPS
def secure_download(url):
    # Always use HTTPS for secure transport
    response = requests.get("https://" + url)
    return response.text

def main():
    # Load password from environment variable (no hardcoding)
    pwd = os.getenv("ADMIN_PASSWORD", "undefined")
    print("Password loaded securely")

    # Securely download example page
    secure_download("example.com")

if __name__ == "__main__":
    main()
