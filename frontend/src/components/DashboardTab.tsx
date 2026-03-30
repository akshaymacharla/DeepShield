import { Activity, ShieldCheck, AlertTriangle, ShieldAlert, History, BarChart3, TrendingUp, Zap } from "lucide-react";

export type ScanRecord = {
  id: string;
  fileName: string;
  verdict: "genuine" | "deepfake" | null;
  confidence: number;
  time: string;
};

interface DashboardTabProps {
  scans?: ScanRecord[];
}

const DashboardTab = ({ scans = [] }: DashboardTabProps) => {
  const deepfakes = scans.filter((s) => s.verdict === "deepfake").length;
  const genuine = scans.filter((s) => s.verdict === "genuine").length;
  
  // Dummy data if empty for demo purposes
  const displayScans = scans.length > 0 ? scans : [
    { id: "1a", fileName: "urgent_ceo_wire_transfer.m4a", verdict: "deepfake", confidence: 99, time: "10:24 AM" },
    { id: "2b", fileName: "client_meeting_recording.wav", verdict: "genuine", confidence: 92, time: "09:12 AM" },
    { id: "3c", fileName: "voicemail_unknown_number.mp3", verdict: "deepfake", confidence: 87, time: "Yesterday" },
  ];

  const totalDisplay = displayScans.length;
  const fakeDisplay = displayScans.filter(s => s.verdict === "deepfake").length;

  return (
    <section id="dashboard" className="py-24 px-6 relative overflow-hidden">
      {/* Background Decorators */}
      <div className="absolute top-40 left-0 w-72 h-72 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-40 right-0 w-96 h-96 bg-accent/5 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="max-w-6xl mx-auto relative z-10">
        <div className="flex flex-col md:flex-row items-center justify-between mb-12">
          <div>
            <p className="text-primary font-mono text-sm tracking-widest uppercase mb-2">Systems Overview</p>
            <h2 className="text-3xl md:text-4xl font-bold text-foreground">
              Verification Dashboard
            </h2>
          </div>
          <div className="mt-4 md:mt-0 glass-card px-6 py-3 rounded-xl flex items-center gap-4 border-primary/20 bg-primary/5">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
            </span>
            <span className="text-sm font-mono text-primary uppercase tracking-wider">System Online</span>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass-card rounded-2xl p-6 relative overflow-hidden group hover:border-primary/40 transition-colors">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Activity className="w-16 h-16 text-primary" />
            </div>
            <p className="text-muted-foreground text-sm font-medium mb-1">Total Scans</p>
            <h3 className="text-4xl font-bold text-foreground mb-4">{totalDisplay}</h3>
            <div className="flex items-center text-xs text-primary font-mono bg-primary/10 w-fit px-2 py-1 rounded inline-flex">
              <TrendingUp className="w-3 h-3 mr-1" />
              +12% vs last week
            </div>
          </div>
          
          <div className="glass-card rounded-2xl p-6 relative overflow-hidden group hover:border-destructive/40 transition-colors">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <ShieldAlert className="w-16 h-16 text-destructive" />
            </div>
            <p className="text-muted-foreground text-sm font-medium mb-1">Deepfakes Blocked</p>
            <h3 className="text-4xl font-bold text-foreground mb-4">{fakeDisplay}</h3>
            <div className="flex items-center text-xs text-destructive font-mono bg-destructive/10 w-fit px-2 py-1 rounded inline-flex">
              {(fakeDisplay / totalDisplay * 100).toFixed(0)}% detection rate
            </div>
          </div>

          <div className="glass-card rounded-2xl p-6 relative overflow-hidden group hover:border-success/40 transition-colors">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <ShieldCheck className="w-16 h-16 text-success" />
            </div>
            <p className="text-muted-foreground text-sm font-medium mb-1">Genuine Audio</p>
            <h3 className="text-4xl font-bold text-foreground mb-4">{totalDisplay - fakeDisplay}</h3>
            <div className="flex items-center text-xs text-success font-mono bg-success/10 w-fit px-2 py-1 rounded inline-flex">
              Verified authentic
            </div>
          </div>

          <div className="glass-card rounded-2xl p-6 relative overflow-hidden group hover:border-accent/40 transition-colors">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Zap className="w-16 h-16 text-accent" />
            </div>
            <p className="text-muted-foreground text-sm font-medium mb-1">Avg Process Time</p>
            <h3 className="text-4xl font-bold text-foreground mb-4">1.2s</h3>
            <div className="flex items-center text-xs text-accent font-mono bg-accent/10 w-fit px-2 py-1 rounded inline-flex">
              Optimal performance
            </div>
          </div>
        </div>

        {/* Recent Scans Table */}
        <div className="glass-card rounded-2xl overflow-hidden border border-secondary">
          <div className="p-6 border-b border-border bg-secondary/20 flex flex-col sm:flex-row justify-between items-center gap-4">
            <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <History className="w-5 h-5 text-primary" />
              Recent Scan Log
            </h3>
            <div className="flex items-center gap-2">
              <button className="px-3 py-1.5 text-xs font-medium bg-secondary text-foreground hover:bg-secondary/80 rounded-md transition-colors">
                Export CSV
              </button>
            </div>
          </div>
          
          <div className="w-full overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-secondary/10 border-b border-border">
                  <th className="px-6 py-4 text-xs font-mono tracking-wider text-muted-foreground uppercase">File Name</th>
                  <th className="px-6 py-4 text-xs font-mono tracking-wider text-muted-foreground uppercase">Analysis Time</th>
                  <th className="px-6 py-4 text-xs font-mono tracking-wider text-muted-foreground uppercase">Verdict</th>
                  <th className="px-6 py-4 text-xs font-mono tracking-wider text-muted-foreground uppercase text-right">Confidence Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {displayScans.map((scan) => (
                  <tr key={scan.id} className="hover:bg-secondary/30 transition-colors group">
                    <td className="px-6 py-4 text-sm text-foreground font-medium flex items-center gap-3">
                      <div className={`p-1.5 rounded-md ${scan.verdict === 'deepfake' ? 'bg-destructive/10 text-destructive' : 'bg-success/10 text-success'}`}>
                        {scan.verdict === 'deepfake' ? <ShieldAlert className="w-4 h-4" /> : <ShieldCheck className="w-4 h-4" />}
                      </div>
                      {scan.fileName}
                    </td>
                    <td className="px-6 py-4 text-sm text-muted-foreground font-mono">
                      {scan.time}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        scan.verdict === 'deepfake' 
                          ? 'bg-[hsl(0,72%,51%,0.15)] text-destructive border border-destructive/20 shadow-[0_0_10px_hsl(0,72%,51%,0.2)]' 
                          : 'bg-[hsl(155,75%,45%,0.15)] text-success border border-success/20 shadow-[0_0_10px_hsl(155,75%,45%,0.2)]'
                      }`}>
                        {scan.verdict === 'deepfake' ? 'DEEPFAKE' : 'GENUINE'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-3">
                        <div className="w-24 h-1.5 bg-secondary rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full ${scan.verdict === 'deepfake' ? 'bg-destructive' : 'bg-success'}`}
                            style={{ width: `${scan.confidence}%` }}
                          />
                        </div>
                        <span className="text-sm font-mono text-foreground">{scan.confidence}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
                
                {scans.length === 0 && (
                  <tr className="bg-secondary/5 border-t border-border/50">
                    <td colSpan={4} className="px-6 py-3 text-xs text-center text-muted-foreground">
                      Showing demonstration data. Upload files to see real history.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DashboardTab;
