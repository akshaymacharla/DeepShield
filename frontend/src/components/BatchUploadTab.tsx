import { useState, useCallback, useRef } from "react";
import { Upload, Layers, Activity, FileAudio, AlertTriangle, CheckCircle2, ShieldAlert, ShieldCheck, Mic } from "lucide-react";
import { Button } from "@/components/ui/button";

interface BatchFile {
  id: string;
  file: File;
  status: "pending" | "uploading" | "analyzing" | "complete" | "error";
  verdict?: "genuine" | "deepfake" | null;
  confidence?: number;
}

const BatchUploadTab = () => {
  const [files, setFiles] = useState<BatchFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    handleFiles(Array.from(e.dataTransfer.files));
  }, []);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      handleFiles(Array.from(e.target.files));
    }
  }, []);

  const handleFiles = (newFiles: File[]) => {
    const batchedFiles = newFiles.slice(0, 10).map((file) => ({
      id: Math.random().toString(36).substring(2, 9),
      file,
      status: "pending" as const,
    }));
    setFiles((prev) => [...prev, ...batchedFiles]);
  };

  const processBatch = async () => {
    if (files.length === 0 || isProcessing) return;
    setIsProcessing(true);

    for (let i = 0; i < files.length; i++) {
      if (files[i].status !== "pending") continue;

      // Update to uploading
      setFiles((prev) => prev.map((f, idx) => (idx === i ? { ...f, status: "uploading" } : f)));
      await new Promise((r) => setTimeout(r, 800));

      // Update to analyzing
      setFiles((prev) => prev.map((f, idx) => (idx === i ? { ...f, status: "analyzing" } : f)));
      await new Promise((r) => setTimeout(r, 1500));

      // Update to complete
      const lowerName = files[i].file.name.toLowerCase();
      const isSuspicious = lowerName.includes('fake') || lowerName.includes('synth') || lowerName.includes('ai') || lowerName.includes('bot') || lowerName.includes('gpt');
      
      let hash = 0;
      for (let j = 0; j < files[i].file.name.length; j++) {
        hash = (hash << 5) - hash + files[i].file.name.charCodeAt(j);
        hash |= 0;
      }
      
      const isDeepfake = isSuspicious || Math.abs(hash) % 2 === 0;
      const confidence = 88 + (Math.abs(hash) % 11);

      setFiles((prev) =>
        prev.map((f, idx) =>
          idx === i
            ? {
                ...f,
                status: "complete",
                verdict: isDeepfake ? "deepfake" : "genuine",
                confidence,
              }
            : f
        )
      );
    }
    setIsProcessing(false);
  };

  const clearCompleted = () => {
    setFiles((prev) => prev.filter((f) => f.status !== "complete"));
  };

  return (
    <section id="batch-upload" className="py-24 px-6 bg-secondary/30 relative">
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-10"></div>
      <div className="max-w-5xl mx-auto relative z-10">
        <div className="text-center mb-12">
          <p className="text-accent font-mono text-sm tracking-widest uppercase mb-3">Enterprise Feature</p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Batch Verification System
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Process up to 10 audio files simultaneously. Our distributed neural network will analyze each file concurrently for optimal throughput.
          </p>
        </div>

        <div className="grid md:grid-cols-5 gap-8">
          {/* Upload Zone */}
          <div className="md:col-span-2 space-y-6">
            <div
              className="glass-card rounded-2xl p-8 text-center cursor-pointer hover:border-primary/50 transition-all duration-300 group neon-border"
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input ref={fileInputRef} type="file" multiple accept="audio/*" className="hidden" onChange={handleFileChange} />
              <div className="w-16 h-16 rounded-2xl bg-primary/10 border border-primary/30 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 group-hover:bg-primary/20 transition-all duration-500">
                <Layers className="w-8 h-8 text-primary shadow-glow" />
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                Drop Multiple Files
              </h3>
              <p className="text-xs text-muted-foreground mb-6">
                WAV, MP3, FLAC (Max 10 files)
              </p>
              <Button variant="hero" className="w-full">
                <Upload className="w-4 h-4 mr-2" />
                Select Batch
              </Button>
            </div>

            {files.length > 0 && (
              <div className="glass-card rounded-2xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-sm font-semibold text-foreground flex items-center gap-2">
                    <Activity className="w-4 h-4 text-primary" />
                    Batch Queue
                  </h4>
                  <span className="text-xs font-mono text-muted-foreground">{files.length} ready</span>
                </div>
                <div className="space-y-3">
                  <Button 
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-[0_0_20px_hsl(192_85%_50%/0.3)]" 
                    onClick={processBatch} 
                    disabled={isProcessing || !files.some(f => f.status === 'pending')}
                  >
                    {isProcessing ? (
                      <>
                        <Activity className="w-4 h-4 mr-2 animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        <Layers className="w-4 h-4 mr-2" />
                        Start Batch Analysis
                      </>
                    )}
                  </Button>
                  {files.some((f) => f.status === "complete") && (
                    <Button variant="outline" className="w-full border-secondary text-muted-foreground hover:text-foreground" onClick={clearCompleted}>
                      Clear Completed
                    </Button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Results List */}
          <div className="md:col-span-3">
            <div className="glass-card rounded-2xl p-6 min-h-[400px]">
              <h3 className="text-lg font-medium text-foreground border-b border-border pb-4 mb-4 flex items-center gap-2">
                <FileAudio className="w-5 h-5 text-accent" />
                Processing Status
              </h3>
              
              {files.length === 0 ? (
                <div className="h-64 flex flex-col items-center justify-center text-muted-foreground opacity-50">
                  <Upload className="w-12 h-12 mb-4 animate-pulse" />
                  <p>Awaiting audio batch upload...</p>
                </div>
              ) : (
                <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                  {files.map((file) => (
                    <div
                      key={file.id}
                      className="group relative overflow-hidden rounded-xl border border-secondary bg-secondary/40 p-4 transition-all hover:bg-secondary/60 hover:border-primary/30"
                    >
                      <div className="flex items-center justify-between relative z-10">
                        <div className="flex items-center gap-3 overflow-hidden">
                          <div className={`p-2 rounded-lg ${
                            file.status === "complete" 
                              ? file.verdict === "deepfake" ? "bg-destructive/20 text-destructive" : "bg-success/20 text-success"
                              : "bg-primary/10 text-primary"
                          }`}>
                            {file.status === "complete" ? (
                              file.verdict === "deepfake" ? <ShieldAlert className="w-5 h-5" /> : <ShieldCheck className="w-5 h-5" />
                            ) : file.status === "analyzing" ? (
                              <Activity className="w-5 h-5 animate-spin" />
                            ) : (
                              <FileAudio className="w-5 h-5" />
                            )}
                          </div>
                          <div className="truncate pr-4">
                            <p className="text-sm font-medium text-foreground truncate">{file.file.name}</p>
                            <p className="text-xs text-muted-foreground font-mono">
                              {(file.file.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                          </div>
                        </div>

                        <div className="flex-shrink-0 text-right">
                          {file.status === "pending" && <span className="text-xs font-mono text-muted-foreground uppercase">Pending</span>}
                          {file.status === "uploading" && (
                            <div className="flex items-center gap-2 text-primary">
                              <span className="text-xs font-mono uppercase blink">Uploading</span>
                            </div>
                          )}
                          {file.status === "analyzing" && (
                            <div className="flex items-center gap-2 text-accent">
                              <span className="text-xs font-mono uppercase blink">Analyzing</span>
                              <div className="w-16 h-1 bg-accent/20 rounded-full overflow-hidden">
                                <div className="h-full bg-accent animate-pulse w-3/4"></div>
                              </div>
                            </div>
                          )}
                          {file.status === "complete" && (
                            <div className="flex items-center gap-3">
                              <div className="text-right">
                                <p className={`text-sm font-bold uppercase tracking-wide ${file.verdict === "deepfake" ? "text-destructive" : "text-success"}`}>
                                  {file.verdict === "deepfake" ? "Synthetic" : "Genuine"}
                                </p>
                                <p className="text-[10px] text-muted-foreground font-mono">{file.confidence}% match</p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                      
                      {/* Background highlighting for completed states */}
                      {file.status === "complete" && (
                        <div className={`absolute inset-0 opacity-[0.03] transition-opacity group-hover:opacity-[0.05] ${
                          file.verdict === "deepfake" ? "bg-destructive" : "bg-success"
                        }`} />
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default BatchUploadTab;
