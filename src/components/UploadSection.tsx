import { Upload, FileAudio, Mic, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useCallback, useRef } from "react";
import type { AnalysisState, VerdictType } from "@/pages/Index";
import AnalysisResult from "./AnalysisResult";

interface UploadSectionProps {
  analysisState: AnalysisState;
  verdict: VerdictType;
  confidence: number;
  fileName: string;
  onFileUpload: (file: File) => void;
  onReset: () => void;
}

const UploadSection = ({ analysisState, verdict, confidence, fileName, onFileUpload, onReset }: UploadSectionProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) onFileUpload(file);
  }, [onFileUpload]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFileUpload(file);
  }, [onFileUpload]);

  return (
    <section id="analyze" className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">Voice Analysis</p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Upload & Analyze Audio
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Upload a voice recording to determine if it's genuine or synthetically generated.
          </p>
        </div>

        {analysisState === "idle" ? (
          <div
            className="glass-card rounded-2xl p-12 text-center cursor-pointer hover:border-primary/30 transition-all duration-300 group"
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              className="hidden"
              onChange={handleFileChange}
            />
            <div className="w-20 h-20 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-6 group-hover:scale-105 transition-transform">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              Drop audio file here or click to browse
            </h3>
            <p className="text-sm text-muted-foreground mb-6">
              Supports WAV, MP3, M4A, FLAC, OGG — Max 50MB
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button variant="hero" size="lg">
                <FileAudio className="w-4 h-4" />
                Upload File
              </Button>
              <div className="relative flex items-center gap-3 px-5 py-3 rounded-xl border border-dashed border-accent/30 bg-accent/5">
                <Mic className="w-4 h-4 text-accent" />
                <span className="text-sm font-medium text-accent">Record Live</span>
                <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest bg-accent/15 border border-accent/25 text-accent">
                  Coming Soon
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="glass-card rounded-2xl p-8">
            {analysisState === "uploading" && (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-6 animate-pulse">
                  <Upload className="w-7 h-7 text-primary" />
                </div>
                <p className="text-foreground font-medium mb-2">Uploading {fileName}...</p>
                <div className="w-64 mx-auto h-1.5 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full animate-pulse" style={{ width: "60%" }} />
                </div>
              </div>
            )}

            {analysisState === "analyzing" && (
              <div className="text-center py-12">
                <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-6 pulse-glow">
                  <svg className="w-7 h-7 text-primary animate-spin" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" strokeDasharray="30 70" />
                  </svg>
                </div>
                <p className="text-foreground font-medium mb-1">Analyzing Voice Patterns</p>
                <p className="text-sm text-muted-foreground font-mono">Running neural network inference...</p>
                <div className="flex justify-center gap-1 mt-6">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className="w-1.5 h-8 bg-primary/40 rounded-full"
                      style={{
                        animation: `waveform 1s ease-in-out ${i * 0.15}s infinite`,
                      }}
                    />
                  ))}
                </div>
              </div>
            )}

            {analysisState === "complete" && verdict && (
              <div>
                <AnalysisResult verdict={verdict} confidence={confidence} fileName={fileName} />
                <div className="flex justify-center mt-8">
                  <Button variant="heroOutline" onClick={onReset}>
                    <RotateCcw className="w-4 h-4" />
                    Analyze Another File
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </section>
  );
};

export default UploadSection;
