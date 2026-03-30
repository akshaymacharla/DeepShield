import { CheckCircle, AlertTriangle, FileAudio, Activity, Waves, Brain, MessageSquare, ThumbsUp, ThumbsDown, Send, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
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

  const handleSubmitFeedback = () => {
    if (!userVerdict) {
      toast.error("Please indicate whether you agree or disagree with the result.");
      return;
    }
    if (userVerdict === "disagree" && !actualLabel) {
      toast.error("Please select what you believe the correct classification is.");
      return;
    }
    // Simulate sending feedback for model retraining
    console.log("Feedback submitted:", { userVerdict, actualLabel, userComment, originalVerdict: verdict, confidence });
    setFeedbackSubmitted(true);
    toast.success("Thank you! Your feedback has been recorded and will help improve our model.");
  };

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

          {/* Agree / Disagree */}
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
                <ThumbsUp className="w-4 h-4" />
                Yes, accurate
              </button>
              <button
                onClick={() => setUserVerdict("disagree")}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                  userVerdict === "disagree"
                    ? "border-destructive/50 bg-destructive/10 text-destructive"
                    : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-destructive/30"
                }`}
              >
                <ThumbsDown className="w-4 h-4" />
                No, incorrect
              </button>
            </div>
          </div>

          {/* Correct label selection (shown on disagree) */}
          {userVerdict === "disagree" && (
            <div className="space-y-2 animate-fade-in">
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">What is the correct classification?</p>
              <div className="flex gap-3">
                <button
                  onClick={() => setActualLabel("genuine")}
                  className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                    actualLabel === "genuine"
                      ? "border-success/50 bg-success/10 text-success"
                      : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-success/30"
                  }`}
                >
                  Genuine Voice
                </button>
                <button
                  onClick={() => setActualLabel("deepfake")}
                  className={`flex-1 px-4 py-3 rounded-lg border text-sm font-medium transition-all ${
                    actualLabel === "deepfake"
                      ? "border-destructive/50 bg-destructive/10 text-destructive"
                      : "border-border/50 bg-secondary/30 text-muted-foreground hover:border-destructive/30"
                  }`}
                >
                  Deepfake Voice
                </button>
              </div>
            </div>
          )}

          {/* Comment */}
          <div className="space-y-2">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Additional comments (optional)</p>
            <textarea
              value={userComment}
              onChange={(e) => setUserComment(e.target.value)}
              placeholder="e.g. I know the speaker personally, this is their real voice..."
              className="w-full h-20 px-4 py-3 rounded-lg bg-secondary/30 border border-border/50 text-sm text-foreground placeholder:text-muted-foreground/50 resize-none focus:outline-none focus:border-primary/50 transition-colors"
            />
          </div>

          <Button
            onClick={handleSubmitFeedback}
            className="w-full gap-2"
            disabled={!userVerdict}
          >
            <Send className="w-4 h-4" />
            Submit Feedback
          </Button>
        </div>
      )}
    </div>
  );
};

export default AnalysisResult;
