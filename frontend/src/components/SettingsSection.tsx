import { useState } from "react";
import { Settings, Bell, Shield, Volume2, Sliders, Moon, Sun } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";

const SettingsSection = () => {
  const { toast } = useToast();
  const [darkMode, setDarkMode] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [autoAnalyze, setAutoAnalyze] = useState(false);
  const [sensitivity, setSensitivity] = useState([0.5]);
  const [audioPreprocess, setAudioPreprocess] = useState(true);
  const [realTimeAlerts, setRealTimeAlerts] = useState(false);

  const handleSave = () => {
    toast({
      title: "Settings Saved",
      description: "Your preferences have been updated successfully.",
    });
  };

  return (
    <section id="settings" className="py-24 px-6">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">Configuration</p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Settings
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Customize your DeepShield experience and detection preferences.
          </p>
        </div>

        <div className="grid gap-6">
          {/* Appearance */}
          <div className="glass-card rounded-xl p-6 border">
            <div className="flex items-center gap-3 mb-6">
              {darkMode ? <Moon className="w-5 h-5 text-primary" /> : <Sun className="w-5 h-5 text-primary" />}
              <h3 className="text-lg font-semibold text-foreground">Appearance</h3>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-foreground">Dark Mode</Label>
                <p className="text-sm text-muted-foreground">Use dark theme for the interface</p>
              </div>
              <Switch checked={darkMode} onCheckedChange={setDarkMode} />
            </div>
          </div>

          {/* Detection Settings */}
          <div className="glass-card rounded-xl p-6 border">
            <div className="flex items-center gap-3 mb-6">
              <Sliders className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold text-foreground">Detection</h3>
            </div>
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <Label className="text-foreground">Detection Sensitivity</Label>
                    <p className="text-sm text-muted-foreground">Higher values catch more but may increase false positives</p>
                  </div>
                  <span className="text-sm font-mono text-primary">{sensitivity[0].toFixed(2)}</span>
                </div>
                <Slider value={sensitivity} onValueChange={setSensitivity} min={0.1} max={1.0} step={0.05} className="w-full" />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-foreground">Auto-Analyze on Upload</Label>
                  <p className="text-sm text-muted-foreground">Automatically start analysis when a file is uploaded</p>
                </div>
                <Switch checked={autoAnalyze} onCheckedChange={setAutoAnalyze} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-foreground">Audio Preprocessing</Label>
                  <p className="text-sm text-muted-foreground">Apply noise reduction before analysis</p>
                </div>
                <Switch checked={audioPreprocess} onCheckedChange={setAudioPreprocess} />
              </div>
            </div>
          </div>

          {/* Notifications */}
          <div className="glass-card rounded-xl p-6 border">
            <div className="flex items-center gap-3 mb-6">
              <Bell className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold text-foreground">Notifications</h3>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-foreground">Email Notifications</Label>
                  <p className="text-sm text-muted-foreground">Receive analysis results via email</p>
                </div>
                <Switch checked={notifications} onCheckedChange={setNotifications} />
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-foreground">Real-Time Alerts</Label>
                  <p className="text-sm text-muted-foreground">Get instant alerts for deepfake detections</p>
                </div>
                <Switch checked={realTimeAlerts} onCheckedChange={setRealTimeAlerts} />
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <Button onClick={handleSave} className="px-8">
              Save Settings
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default SettingsSection;
