import logo from "@/assets/logo.png";

const Footer = () => {
  return (
    <footer className="border-t border-border/50 py-12 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <img src={logo} alt="DeepShield AI" className="w-8 h-8 rounded-lg" />
          <span className="font-semibold text-foreground">
            Deep<span className="text-primary">Shield</span>
          </span>
        </div>
        <p className="text-sm text-muted-foreground">
          AI-Powered Deepfake Voice Detection · Digital Forensics
        </p>
        <p className="text-xs text-muted-foreground">
          © 2026 DeepShield. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;
