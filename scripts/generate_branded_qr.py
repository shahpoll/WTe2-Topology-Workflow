import qrcode
from PIL import Image
import os

# Settings
URL = "https://github.com/shahpoll/Quantum-ESPRESSO-WTe2-Topology"
LOGO_PATH = "repo/figures/github_logo.png"
OUTPUT_PATH = "repo/figures/Fig_Repo_QR_Branded.png"

def generate_branded_qr():
    # 1. Generate QR Code (High Error Correction to support logo coverage)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(URL)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    # 2. Add Logo
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        
        # Calculate size (20% of QR width)
        qr_width, qr_height = img_qr.size
        logo_size = int(qr_width * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # Calculate position (Center)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        
        # Paste logo
        # If transparent, we need a white background behind it?
        # GitHub mark is usually black on transparent.
        # Let's create a white square behind it to make it readable over the QR modules
        bg = Image.new('RGB', (logo_size + 4, logo_size + 4), 'white')
        img_qr.paste(bg, (pos[0]-2, pos[1]-2))
        
        # Use simple paste if no alpha, or mask if alpha
        if logo.mode in ('RGBA', 'LA'):
            img_qr.paste(logo, pos, mask=logo)
        else:
            img_qr.paste(logo, pos)
            
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}. Generating standard QR.")
    
    # Save
    if not os.path.exists(os.path.dirname(OUTPUT_PATH)):
        os.makedirs(os.path.dirname(OUTPUT_PATH))
    img_qr.save(OUTPUT_PATH)
    print(f"Saved Branded QR to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_branded_qr()
