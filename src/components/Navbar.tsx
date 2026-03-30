import { Shield } from "lucide-react";

const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 glass-card border-b">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-primary/10 border border-primary/30 flex items-center justify-center">
            <Shield className="w-5 h-5 text-primary" />
          </div>
          <span className="font-semibold text-lg text-foreground tracking-tight">
            Vox<span className="text-primary">Guard</span>
          </span>
        </div>
        <div className="hidden md:flex items-center gap-8">
          <a href="#analyze" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Analyze
          </a>
          <a href="#how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            How It Works
          </a>
          <a href="#features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Features
          </a>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-success/10 border border-success/20 text-success text-xs font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
            System Online
          </span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
