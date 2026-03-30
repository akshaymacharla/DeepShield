import logo from "@/assets/logo.png";

const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 glass-card border-b">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img src={logo} alt="DeepShield AI" className="w-9 h-9 rounded-lg" />
          <span className="font-semibold text-lg text-foreground tracking-tight">
            Deep<span className="text-primary">Shield</span>
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
          <a href="#api" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            API
          </a>
          <a href="#settings" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            Settings
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