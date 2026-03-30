import { CheckCircle, AlertTriangle, FileAudio, Activity, Waves, Brain, MessageSquare, ThumbsUp, ThumbsDown, Send, X, Download, Eye } from "lucide-react";
import { useState, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts";
import type { VerdictType } from "@/pages/Index";

interface AnalysisResultProps {
  verdict: VerdictType;
  confidence: number;
  fileName: string;
}

const AnalysisResult = ({ verdict, confidence, fileName }: AnalysisResultProps) => {
  const isGenuine = verdict === "genuine";
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);
  const [userVerdict, setUserVerdict] = useState<"agree" | "disagree" | null>(null);
  const [userComment, setUserComment] = useState("");
  const [actualLabel, setActualLabel] = useState<"genuine" | "deepfake" | "">("");
  const [sensitivity, setSensitivity] = useState(0.5);

  // Simulated forensic data
  const forensicData = useMemo(() => {
    const syntheticScore = isGenuine ? confidence : 100 - confidence;
    const aiScore = isGenuine ? 100 - confidence : confidence;
    return {
      duration: (Math.random() * 8 + 2).toFixed(2),
      pitchMag: Math.floor(Math.random() * 3000 + 500),
      aiConfidence: confidence,
      threat: isGenuine ? "NONE" : "DEEPFAKE DETECTED",
      observation: isGenuine
        ? "[OK] Voice displays natural organic variance and noise profile"
        : "[ALERT] Synthetic artifacts detected in spectral and temporal domains",
      syntheticPct: aiScore.toFixed(1),
      organicPct: syntheticScore.toFixed(1),
    };
  }, [isGenuine, confidence]);

  const featureBreakdown = useMemo(() => [
    { name: "MFCC", value: isGenuine ? Math.floor(Math.random() * 30 + 15) : Math.floor(Math.random() * 40 + 30), color: "hsl(var(--primary))" },
    { name: "Pitch\nStability", value: isGenuine ? Math.floor(Math.random() * 20 + 70) : 100, color: "hsl(var(--accent))" },
    { name: "Spectral\nFlux", value: isGenuine ? Math.floor(Math.random() * 20 + 10) : Math.floor(Math.random() * 30 + 20), color: "hsl(var(--primary))" },
    { name: "Chroma\nPattern", value: isGenuine ? Math.floor(Math.random() * 25 + 15) : Math.floor(Math.random() * 40 + 30), color: "hsl(var(--primary))" },
    { name: "Zero\nCrossing", value: isGenuine ? Math.floor(Math.random() * 20 + 60) : 100, color: "hsl(var(--accent))" },
  ], [isGenuine]);

  // Simulated waveform data
  const waveformBars = useMemo(() => Array.from({ length: 60 }, () => Math.random()), []);

  // Simulated spectrogram rows
  const spectrogramData = useMemo(() =>
    Array.from({ length: 20 }, () =>
      Array.from({ length: 40 }, () => Math.random())
    ), []);

  const handleSubmitFeedback = () => {
    if (!userVerdict) {
      toast.error("Please indicate whether you agree or disagree with the result.");
      return;
    }
    if (userVerdict === "disagree" && !actualLabel) {
      toast.error("Please select what you believe the correct classification is.");
      return;
    }
    console.log("Feedback submitted:", { userVerdict, actualLabel, userComment, originalVerdict: verdict, confidence });
    setFeedbackSubmitted(true);
    toast.success("Thank you! Your feedback has been recorded and will help improve our model.");
  };

  const handleDownloadReport = () => {
    toast.success("Report downloaded — Report_" + Math.floor(Math.random() * 999999).toString().padStart(6, "0") + ".pdf");
  };

  return (
    <div className="space-y-6">
      {/* Main Verdict Banner */}
      <div className={`relative overflow-hidden p-8 rounded-2xl border-2 text-center ${
        isGenuine
          ? "bg-success/5 border-success/30"
          : "bg-destructive/5 border-destructive/30"
      }`}>
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full border text-xs font-bold uppercase tracking-widest mb-4 ${
          isGenuine
            ? "bg-success/10 border-success/30 text-success"
            : "bg-destructive/10 border-destructive/30 text-destructive"
        }`}>
          {isGenuine ? "Genuine Voice" : "Deepfake Detected"}
        </div>
        <h3 className={`text-3xl md:text-4xl font-black flex items-center justify-center gap-3 ${isGenuine ? "text-success" : "text-destructive"}`}>
          {isGenuine ? <CheckCircle className="w-8 h-8" /> : <AlertTriangle className="w-8 h-8" />}
          {isGenuine ? "GENUINE VOICE" : "DEEPFAKE DETECTED"}
        </h3>
        <p className={`mt-3 text-sm font-mono tracking-wider ${isGenuine ? "text-success/80" : "text-destructive/80"}`}>
          {forensicData.syntheticPct}% AI SYNTHETIC • {forensicData.organicPct}% HUMAN ORGANIC
        </p>
      </div>

      {/* Two Column Layout */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-4">
          {/* Audio Waveform Preview */}
          <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <FileAudio className="w-4 h-4 text-muted-foreground" />
                <span className="text-xs font-mono text-muted-foreground">{fileName}</span>
              </div>
            </div>
            <div className="flex items-end justify-center gap-[2px] h-16 mb-2">
              {waveformBars.map((h, i) => (
                <div
                  key={i}
                  className="w-1 rounded-full bg-primary/60"
                  style={{ height: `${Math.max(h * 100, 8)}%` }}
                />
              ))}
            </div>
            <div className="flex justify-between text-[10px] text-muted-foreground font-mono">
              <span>0:00</span>
              <span>0:{forensicData.duration.split('.')[0].padStart(2, '0')}</span>
            </div>
          </div>

          {/* Sensitivity Slider */}
          <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-foreground">Sensitivity</span>
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 rounded bg-secondary border border-border/50 text-xs font-mono text-foreground">{sensitivity.toFixed(1)}</span>
              </div>
            </div>
            <input
              type="range"
              min="0.3"
              max="0.8"
              step="0.1"
              value={sensitivity}
              onChange={(e) => setSensitivity(parseFloat(e.target.value))}
              className="w-full accent-primary"
            />
            <div className="flex justify-between text-[10px] text-muted-foreground font-mono mt-1">
              <span>0.3</span>
              <span>0.8</span>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "DURATION", value: `${forensicData.duration}s` },
              { label: "PITCH/MAG", value: `${forensicData.pitchMag} Hz` },
              { label: "AI CONF %", value: `${forensicData.aiConfidence}%` },
              { label: "THREAT", value: forensicData.threat },
            ].map((stat) => (
              <div key={stat.label} className="p-3 rounded-lg bg-secondary/40 border border-border/50">
                <p className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider mb-1">{stat.label}</p>
                <p className={`text-sm font-bold font-mono ${
                  stat.label === "THREAT"
                    ? isGenuine ? "text-success" : "text-destructive"
                    : "text-foreground"
                }`}>{stat.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-4">
          {/* AI Forensic Observation */}
          <div className="p-4 rounded-xl bg-accent/5 border border-accent/20">
            <h4 className="text-sm font-bold text-primary uppercase tracking-wider mb-2">AI Forensic Observation:</h4>
            <p className="text-sm text-muted-foreground">{forensicData.observation}</p>
          </div>

          {/* Feature Analysis Breakdown Chart */}
          <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
            <h4 className="text-sm font-bold text-foreground text-center mb-4">Feature Analysis Breakdown</h4>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={featureBreakdown} barCategoryGap="20%">
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  domain={[0, 100]}
                  tick={{ fontSize: 10, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--secondary))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                    fontSize: "12px",
                    color: "hsl(var(--foreground))"
                  }}
                />
                <Bar dataKey="value" radius={[4, 4, 0, 0]} label={{ position: "top", fontSize: 10, fill: "hsl(var(--foreground))" }}>
                  {featureBreakdown.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Report Download */}
          <button
            onClick={handleDownloadReport}
            className="w-full flex items-center justify-between p-3 rounded-lg bg-secondary/30 border border-border/50 hover:border-primary/30 transition-colors group"
          >
            <span className="text-sm font-mono text-muted-foreground">Report_{Math.floor(Math.random() * 999999).toString().padStart(6, "0")}.pdf</span>
            <span className="flex items-center gap-1 text-xs font-semibold text-primary">
              <Download className="w-3.5 h-3.5" />
              1.5 KB
            </span>
          </button>
        </div>
      </div>

      {/* Spectrogram */}
      <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
        <div className="flex items-center gap-2 mb-3">
          <Eye className="w-4 h-4 text-primary" />
          <h4 className="text-sm font-bold text-foreground">Mel Spectrogram</h4>
        </div>
        <div className="rounded-lg overflow-hidden bg-background">
          <div className="grid" style={{ gridTemplateRows: `repeat(${spectrogramData.length}, 4px)` }}>
            {spectrogramData.map((row, ri) => (
              <div key={ri} className="flex">
                {row.map((val, ci) => (
                  <div
                    key={ci}
                    className="flex-1"
                    style={{
                      backgroundColor: `hsl(${280 - val * 240}, ${70 + val * 30}%, ${20 + val * 50}%)`,
                    }}
                  />
                ))}
              </div>
            ))}
          </div>
          <div className="flex justify-between text-[9px] text-muted-foreground font-mono px-1 mt-1">
            <span>0</span><span>1.0</span><span>2.0</span><span>3.0</span><span>4.0</span><span>5.0s</span>
          </div>
        </div>
      </div>

      {/* Waveform Amplitude */}
      <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
        <h4 className="text-sm font-bold text-foreground text-center mb-3">Waveform (Amplitude)</h4>
        <div className="h-20 flex items-center">
          <svg viewBox="0 0 600 80" className="w-full h-full" preserveAspectRatio="none">
            <path
              d={`M 0 40 ${waveformBars.map((v, i) => `L ${i * 10} ${40 - v * 35}`).join(' ')} L 600 40`}
              fill="none"
              stroke="hsl(var(--primary))"
              strokeWidth="1.5"
            />
            <path
              d={`M 0 40 ${waveformBars.map((v, i) => `L ${i * 10} ${40 + v * 35}`).join(' ')} L 600 40`}
              fill="none"
              stroke="hsl(var(--primary))"
              strokeWidth="1.5"
              opacity="0.5"
            />
          </svg>
        </div>
      </div>

      {/* Results Table */}
      <div className="rounded-xl overflow-hidden border border-border/50">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-secondary/50">
              <th className="text-left p-3 font-bold text-foreground">File</th>
              <th className="text-left p-3 font-bold text-foreground">Verdict</th>
              <th className="text-left p-3 font-bold text-foreground">Conf</th>
              <th className="text-left p-3 font-bold text-foreground">Time</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t border-border/30">
              <td className="p-3 font-mono text-muted-foreground text-xs">{fileName}</td>
              <td className={`p-3 font-bold font-mono text-xs uppercase ${isGenuine ? "text-success" : "text-destructive"}`}>
                {isGenuine ? "GENUINE" : "DEEPFAKE DETECTED"}
              </td>
              <td className="p-3 font-mono text-foreground text-xs">{confidence}%</td>
              <td className="p-3 font-mono text-muted-foreground text-xs">00:{forensicData.duration.split('.')[0].padStart(2, '0')}</td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Feedback Section */}
      {!feedbackOpen && !feedbackSubmitted && (
        <Button
          variant="outline"
          className="w-full gap-2 border-border/50 text-muted-foreground hover:text-foreground"
          onClick={() => setFeedbackOpen(true)}
        >
          <MessageSquare className="w-4 h-4" />
          Disagree with the result? Provide feedback to improve our model
        </Button>
      )}

      {feedbackSubmitted && (
        <div className="p-5 rounded-xl border border-success/20 bg-success/5 text-center space-y-2">
          <CheckCircle className="w-8 h-8 text-success mx-auto" />
          <p className="text-sm font-semibold text-success">Feedback Recorded</p>
          <p className="text-xs text-muted-foreground">
            Your input has been logged and will be used in the next model retraining cycle to improve detection accuracy.
          </p>
        </div>
      )}

      {feedbackOpen && !feedbackSubmitted && (
        <div className="p-5 rounded-xl border border-primary/20 bg-primary/5 space-y-5 animate-fade-in">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-primary" />
              <h4 className="text-sm font-semibold text-foreground">Feedback Loop — Help Train the Model</h4>
            </div>
            <button onClick={() => setFeedbackOpen(false)} className="text-muted-foreground hover:text-foreground transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>
          <p className="text-xs text-muted-foreground">
            Your feedback is valuable. It will be used as labeled training data to retrain and improve the detection model.
          </p>
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Do you agree with this result?</p>
            <div className="flex gap-3">
              <button
                onClick={() => { setUserVerdict("agree"); setActualLabel(""); }}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                  userVerdict === "agree"
                    ? "border-success/50 bg-success/10 text-success"
                    : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-success/30"
                }`}
              >
                <ThumbsUp className="w-4 h-4" /> Yes, accurate
              </button>
              <button
                onClick={() => setUserVerdict("disagree")}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                  userVerdict === "disagree"
                    ? "border-destructive/50 bg-destructive/10 text-destructive"
                    : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-destructive/30"
                }`}
              >
                <ThumbsDown className="w-4 h-4" /> No, incorrect
              </button>
            </div>
          </div>
          {userVerdict === "disagree" && (
            <div className="space-y-2 animate-fade-in">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">What is the correct classification?</p>
              <div className="flex gap-3">
                <button
                  onClick={() => setActualLabel("genuine")}
                  className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                    actualLabel === "genuine" ? "border-success/50 bg-success/10 text-success" : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-success/30"
                  }`}
                >Genuine Voice</button>
                <button
                  onClick={() => setActualLabel("deepfake")}
                  className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                    actualLabel === "deepfake" ? "border-destructive/50 bg-destructive/10 text-destructive" : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-destructive/30"
                  }`}
                >Deepfake Voice</button>
              </div>
            </div>
          )}
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Additional comments (optional)</p>
            <textarea
              value={userComment}
              onChange={(e) => setUserComment(e.target.value)}
              placeholder="e.g. I know the speaker personally, this is their real voice..."
              className="w-full h-20 px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 text-sm text-foreground placeholder:text-muted-foreground/50 resize-none focus:outline-none focus:border-primary/50 transition-colors"
            />
          </div>
          <Button onClick={handleSubmitFeedback} className="w-full gap-2" disabled={!userVerdict}>
            <Send className="w-4 h-4" /> Submit Feedback
          </Button>
        </div>
      )}
    </div>
  );
};

export default AnalysisResult;
