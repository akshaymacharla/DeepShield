# DeepShield - AI Deepfake Voice Detection

DeepShield is a comprehensive forensic tool designed to detect and trace synthetically generated voice audio (deepfakes). It includes a React/Vite web interface and a powerful Python backend neural network.

## Project Structure

This repository is organized logically into two environments:
- \`/frontend/\` - The React user interface built with Vite, Tailwind CSS, and Shadcn UI.
- \`/backend/\` - The Python deep learning models and API endpoints.

---

## 💻 Frontend Setup

The frontend provides an intuitive "clinical obsidian and cyan" interface for real-time and batch verification.

### Requirements
- Node.js (v18+)

### Installation & Running
1. Navigate to the frontend directory:
   \`\`\`bash
   cd frontend
   \`\`\`
2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`
3. Start the development server:
   \`\`\`bash
   npm run dev
   \`\`\`
*(The application will be accessible at (https://deepshield-4tkp.onrender.com/)
Demo-https://youtu.be/_HjykSrMUN8?si=IfTwXc_Qd1LW15eT

---

## 🧠 Backend Setup

The backend handles the actual audio processing, neural network inference, and provides REST API endpoints to support the frontend application.

### Requirements
- Python 3.9+
- pip

### Installation & Running
1. Navigate to the backend directory:
   \`\`\`bash
   cd backend
   \`\`\`
2. *We recommend creating a virtual environment:*
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   \`\`\`
3. Install Python dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. Run the API Server:
   \`\`\`bash
   python app.py
   \`\`\`

---

## Technical Stack & Aesthetics

- **User Interface**: Vite, React, Tailwind CSS, Lucide Icons, Shadcn. Features glass-card depth, micro-animations, and dynamic visual verification tools.
- **API Engine**: Robust Python REST API delivering audio stream processing and waveform spectral forensics.

> **Note on Verification Mode**: In environments where the backend neural net is not running, the frontend operates in a demonstration mode, simulating deepfake detection locally. 

For further details on API integration methods, navigate to the API section inside the frontend interface!
