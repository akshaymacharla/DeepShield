import { Button } from "@/components/ui/button";
import { Shield, ChevronRight } from "lucide-react";
import WaveformVisualizer from "./WaveformVisualizer";

const HeroSection = () => {
  return (
    <section className="relative pt-32 pb-20 px-6 overflow-hidden">
      {/* Background grid pattern */}
      <div className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(hsl(var(--primary)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--primary)) 1px, transparent 1px)`,
          backgroundSize: '60px 60px',
        }}
      />
      {/* Radial glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] rounded-full opacity-20"
        style={{ background: 'radial-gradient(ellipse, hsl(192 85% 50% / 0.12) 0%, hsl(265 70% 60% / 0.05) 40%, transparent 70%)' }}
      />

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 mb-8">
              <Shield className="w-3.5 h-3.5 text-primary" />
              <span className="text-xs font-medium text-primary tracking-wide">AI-POWERED VOICE FORENSICS</span>
            </div>

            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-[1.1] mb-6">
              <span className="text-foreground">Detect</span>{" "}
              <span className="gradient-text">Deepfake</span>
              <br />
              <span className="text-foreground">Voice Calls</span>
            </h1>

            <p className="text-lg text-muted-foreground leading-relaxed mb-10 max-w-lg">
              Advanced AI system that analyzes voice recordings to detect synthetic speech,
              voice cloning, and AI-generated audio with high accuracy.
            </p>

            <div className="flex flex-wrap gap-4">
              <Button variant="hero" size="lg" className="group" onClick={() => document.getElementById('analyze')?.scrollIntoView({ behavior: 'smooth' })}>
                Start Analysis
                <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Button>
              <Button variant="heroOutline" size="lg" onClick={() => document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' })}>
                Learn More
              </Button>
            </div>
          </div>

          <div className="hidden lg:block">
            <div className="relative">
              <div className="glass-card rounded-2xl p-8 glow-border">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-3 h-3 rounded-full bg-destructive/60" />
                  <div className="w-3 h-3 rounded-full bg-warning/60" />
                  <div className="w-3 h-3 rounded-full bg-success/60" />
                  <span className="ml-2 text-xs font-mono text-muted-foreground">voice_analysis.wav</span>
                </div>
                <WaveformVisualizer />
                <div className="mt-6 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                    <span className="text-xs font-mono text-primary">ANALYZING...</span>
                  </div>
                  <span className="text-xs font-mono text-muted-foreground">00:04.32 / 00:12.00</span>
                </div>
              </div>
              {/* Floating accent */}
              <div className="absolute -bottom-4 -right-4 w-24 h-24 rounded-2xl bg-primary/5 border border-primary/10 float-animation" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
