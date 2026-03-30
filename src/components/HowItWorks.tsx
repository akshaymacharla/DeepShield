import { Upload, Cpu, ShieldCheck } from "lucide-react";

const HowItWorks = () => {
  const steps = [
    {
      icon: <Upload className="w-6 h-6" />,
      step: "01",
      title: "Upload Audio",
      description: "Upload a voice recording or provide a live audio stream for analysis.",
    },
    {
      icon: <Cpu className="w-6 h-6" />,
      step: "02",
      title: "AI Processing",
      description: "Our neural networks analyze spectral patterns, formants, and temporal features.",
    },
    {
      icon: <ShieldCheck className="w-6 h-6" />,
      step: "03",
      title: "Get Results",
      description: "Receive a detailed verdict with confidence score and forensic breakdown.",
    },
  ];

  return (
    <section id="how-it-works" className="py-24 px-6 bg-card/50">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">Workflow</p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            How It Works
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Three simple steps to determine voice authenticity with our AI-powered analysis engine.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((item, index) => (
            <div key={item.step} className="relative">
              {index < steps.length - 1 && (
                <div className="hidden md:block absolute top-12 left-[60%] w-[80%] h-px bg-gradient-to-r from-primary/30 to-transparent" />
              )}
              <div className="glass-card rounded-xl p-8 text-center relative">
                <span className="absolute top-4 right-4 text-4xl font-bold text-primary/10 font-mono">
                  {item.step}
                </span>
                <div className="w-14 h-14 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary mx-auto mb-5">
                  {item.icon}
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{item.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
