import { Shield } from "lucide-react";

const Footer = () => {
  return (
    <footer className="border-t border-border/50 py-12 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/10 border border-primary/30 flex items-center justify-center">
            <Shield className="w-4 h-4 text-primary" />
          </div>
          <span className="font-semibold text-foreground">
            Vox<span className="text-primary">Guard</span>
          </span>
        </div>
        <p className="text-sm text-muted-foreground">
          AI-Powered Deepfake Voice Detection · Digital Forensics
        </p>
        <p className="text-xs text-muted-foreground">
          © 2026 VoxGuard. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
