import { Shield, Upload, Activity, AlertTriangle, CheckCircle, Mic, FileAudio, Zap, Brain, Waves, ChevronRight, BarChart3, Lock, Eye } from "lucide-react";
import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import WaveformVisualizer from "@/components/WaveformVisualizer";
import AnalysisResult from "@/components/AnalysisResult";
import FeatureCard from "@/components/FeatureCard";
import Navbar from "@/components/Navbar";
import HeroSection from "@/components/HeroSection";
import UploadSection from "@/components/UploadSection";
import HowItWorks from "@/components/HowItWorks";
import StatsSection from "@/components/StatsSection";
import Footer from "@/components/Footer";
import ApiSection from "@/components/ApiSection";
import SettingsSection from "@/components/SettingsSection";
import ScrollToTop from "@/components/ScrollToTop";

export type AnalysisState = "idle" | "uploading" | "analyzing" | "complete";
export type VerdictType = "genuine" | "deepfake" | null;

const Index = () => {
  const [analysisState, setAnalysisState] = useState<AnalysisState>("idle");
  const [verdict, setVerdict] = useState<VerdictType>(null);
  const [confidence, setConfidence] = useState(0);
  const [fileName, setFileName] = useState("");

  const handleFileUpload = useCallback((file: File) => {
    setFileName(file.name);
    setAnalysisState("uploading");
    setVerdict(null);

    setTimeout(() => {
      setAnalysisState("analyzing");

      setTimeout(() => {
        const isDeepfake = Math.random() > 0.5;
        setVerdict(isDeepfake ? "deepfake" : "genuine");
        setConfidence(Math.floor(Math.random() * 15) + 85);
        setAnalysisState("complete");
      }, 2500);
    }, 1000);
  }, []);

  const handleReset = useCallback(() => {
    setAnalysisState("idle");
    setVerdict(null);
    setConfidence(0);
    setFileName("");
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <HeroSection />
      <StatsSection />
      <UploadSection
        analysisState={analysisState}
        verdict={verdict}
        confidence={confidence}
        fileName={fileName}
        onFileUpload={handleFileUpload}
        onReset={handleReset}
      />
      <HowItWorks />
      <section id="features" className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">Capabilities</p>
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Advanced Detection Features
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our system employs multiple layers of analysis to ensure the highest accuracy in deepfake voice detection.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Brain className="w-6 h-6" />}
              title="Neural Pattern Analysis"
              description="Deep learning models trained on thousands of voice samples to identify synthetic speech patterns invisible to the human ear."
            />
            <FeatureCard
              icon={<Waves className="w-6 h-6" />}
              title="Spectral Forensics"
              description="Analyzes frequency distributions, formant structures, and spectral envelopes to detect artifacts of voice synthesis."
            />
            <FeatureCard
              icon={<Activity className="w-6 h-6" />}
              title="Temporal Consistency"
              description="Examines micro-timing patterns, pitch transitions, and prosody for signs of AI-generated speech."
            />
            <FeatureCard
              icon={<Lock className="w-6 h-6" />}
              title="Anti-Spoofing Engine"
              description="Detects replay attacks, voice conversion, and text-to-speech synthesis with multi-model verification."
            />
            <FeatureCard
              icon={<BarChart3 className="w-6 h-6" />}
              title="Confidence Scoring"
              description="Provides granular confidence scores with explainable AI insights into what triggered the detection."
            />
            <FeatureCard
              icon={<Eye className="w-6 h-6" />}
              title="Real-Time Monitoring"
              description="Stream live audio for continuous deepfake monitoring during calls with instant alert notifications."
            />
          </div>
        </div>
      </section>
      <ApiSection />
      <Footer />
      <ScrollToTop />
    </div>
  );
};

export default Index;
