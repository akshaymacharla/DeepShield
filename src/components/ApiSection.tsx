import { Code, Copy, Check, Terminal, Zap, Shield, Key } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const codeExample = `curl -X POST https://api.deepshield.ai/v1/analyze \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: multipart/form-data" \\
  -F "audio=@sample_voice.wav" \\
  -F "sensitivity=0.5"`;

const responseExample = `{
  "status": "complete",
  "verdict": "deepfake",
  "confidence": 94.7,
  "threat_level": "high",
  "features": {
    "mfcc_score": 0.12,
    "pitch_stability": 0.34,
    "spectral_flux": 0.89
  }
}`;

const ApiSection = () => {
  const [copiedReq, setCopiedReq] = useState(false);
  const [copiedRes, setCopiedRes] = useState(false);

  const handleCopy = (text: string, type: "req" | "res") => {
    navigator.clipboard.writeText(text);
    if (type === "req") {
      setCopiedReq(true);
      setTimeout(() => setCopiedReq(false), 2000);
    } else {
      setCopiedRes(true);
      setTimeout(() => setCopiedRes(false), 2000);
    }
  };

  return (
    <section id="api" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">Developer Tools</p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Integrate via API
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Seamlessly integrate DeepShield's deepfake detection into your applications with our RESTful API.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 mb-12">
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-4">
              <Key className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Get API Key</h3>
            <p className="text-sm text-muted-foreground">Sign up and generate your API key from the dashboard in seconds.</p>
          </div>
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-4">
              <Terminal className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Make Requests</h3>
            <p className="text-sm text-muted-foreground">Send audio files via REST API and receive analysis results in real-time.</p>
          </div>
          <div className="glass-card rounded-2xl p-6 text-center">
            <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-4">
              <Zap className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">Scale Freely</h3>
            <p className="text-sm text-muted-foreground">Handle thousands of requests per minute with auto-scaling infrastructure.</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Request */}
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="flex items-center justify-between px-5 py-3 border-b border-border/50">
              <div className="flex items-center gap-2">
                <Code className="w-4 h-4 text-primary" />
                <span className="text-sm font-mono font-medium text-foreground">Request</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleCopy(codeExample, "req")}
                className="h-7 px-2 text-xs"
              >
                {copiedReq ? <Check className="w-3 h-3 text-primary" /> : <Copy className="w-3 h-3" />}
                {copiedReq ? "Copied" : "Copy"}
              </Button>
            </div>
            <pre className="p-5 text-sm font-mono text-muted-foreground overflow-x-auto leading-relaxed">
              <code>{codeExample}</code>
            </pre>
          </div>

          {/* Response */}
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="flex items-center justify-between px-5 py-3 border-b border-border/50">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-accent" />
                <span className="text-sm font-mono font-medium text-foreground">Response</span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleCopy(responseExample, "res")}
                className="h-7 px-2 text-xs"
              >
                {copiedRes ? <Check className="w-3 h-3 text-primary" /> : <Copy className="w-3 h-3" />}
                {copiedRes ? "Copied" : "Copy"}
              </Button>
            </div>
            <pre className="p-5 text-sm font-mono text-muted-foreground overflow-x-auto leading-relaxed">
              <code>{responseExample}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ApiSection;
