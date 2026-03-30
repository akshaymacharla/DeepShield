import { CheckCircle, AlertTriangle, FileAudio, Activity, Waves, Brain } from "lucide-react";
import type { VerdictType } from "@/pages/Index";

interface AnalysisResultProps {
  verdict: VerdictType;
  confidence: number;
  fileName: string;
}

const AnalysisResult = ({ verdict, confidence, fileName }: AnalysisResultProps) => {
  const isGenuine = verdict === "genuine";

  return (
    <div className="space-y-6">
      {/* Verdict Header */}
      <div className={`flex items-center gap-4 p-6 rounded-xl border ${
        isGenuine
          ? "bg-success/5 border-success/20"
          : "bg-destructive/5 border-destructive/20"
      }`}>
        <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${
          isGenuine ? "bg-success/10" : "bg-destructive/10"
        }`}>
          {isGenuine ? (
            <CheckCircle className="w-7 h-7 text-success" />
          ) : (
            <AlertTriangle className="w-7 h-7 text-destructive" />
          )}
        </div>
        <div className="flex-1">
          <h3 className={`text-xl font-bold ${isGenuine ? "text-success" : "text-destructive"}`}>
            {isGenuine ? "Genuine Voice Detected" : "Deepfake Voice Detected"}
          </h3>
          <p className="text-sm text-muted-foreground">
            {isGenuine
              ? "This voice recording appears to be from a real human speaker."
              : "This voice recording shows signs of AI generation or voice cloning."}
          </p>
        </div>
        <div className="text-right">
          <p className={`text-3xl font-bold font-mono ${isGenuine ? "text-success" : "text-destructive"}`}>
            {confidence}%
          </p>
          <p className="text-xs text-muted-foreground">Confidence</p>
        </div>
      </div>

      {/* File info */}
      <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-secondary/50">
        <FileAudio className="w-4 h-4 text-muted-foreground" />
        <span className="text-sm font-mono text-muted-foreground">{fileName}</span>
      </div>

      {/* Analysis Metrics */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { icon: <Activity className="w-4 h-4" />, label: "Spectral Analysis", value: isGenuine ? "Normal" : "Anomaly", status: isGenuine },
          { icon: <Waves className="w-4 h-4" />, label: "Formant Structure", value: isGenuine ? "Natural" : "Synthetic", status: isGenuine },
          { icon: <Brain className="w-4 h-4" />, label: "Neural Score", value: isGenuine ? "0.12" : "0.89", status: isGenuine },
        ].map((metric) => (
          <div key={metric.label} className="p-4 rounded-lg bg-secondary/30 border border-border/50">
            <div className="flex items-center gap-2 mb-2 text-muted-foreground">
              {metric.icon}
              <span className="text-xs">{metric.label}</span>
            </div>
            <p className={`text-sm font-semibold ${metric.status ? "text-success" : "text-destructive"}`}>
              {metric.value}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnalysisResult;
