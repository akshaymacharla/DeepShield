import { Copy, Check, Key, Terminal, Zap, AlertTriangle, Circle } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

const endpoints = [
  {
    method: "POST",
    path: "/analyze",
    description: "Analyze an audio file for deepfake detection",
    color: "bg-emerald-500",
  },
  {
    method: "GET",
    path: "/models",
    description: "List all available detection models",
    color: "bg-blue-500",
  },
  {
    method: "GET",
    path: "/status/{id}",
    description: "Get result of an async analysis job",
    color: "bg-blue-500",
  },
  {
    method: "POST",
    path: "/stream",
    description: "Stream live audio for real-time monitoring",
    color: "bg-purple-500",
  },
];

const codeSnippets: Record<string, Record<string, string>> = {
  "/analyze": {
    Python: `import requests

url = "https://api.deepshield.ai/v1/analyze"

with open("voice.wav", "rb") as f:
    response = requests.post(
        url,
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        files={"audio": f},
        data={"sensitivity": 0.5}
    )

print(response.json())`,
    cURL: `curl -X POST https://api.deepshield.ai/v1/analyze \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: multipart/form-data" \\
  -F "audio=@voice.wav" \\
  -F "sensitivity=0.5"`,
    JavaScript: `const formData = new FormData();
formData.append("audio", audioFile);
formData.append("sensitivity", "0.5");

const response = await fetch(
  "https://api.deepshield.ai/v1/analyze",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
    },
    body: formData,
  }
);

const result = await response.json();
console.log(result);`,
    "Node.js": `const fs = require("fs");
const FormData = require("form-data");
const axios = require("axios");

const form = new FormData();
form.append("audio", fs.createReadStream("voice.wav"));
form.append("sensitivity", "0.5");

const { data } = await axios.post(
  "https://api.deepshield.ai/v1/analyze",
  form,
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
      ...form.getHeaders(),
    },
  }
);
console.log(data);`,
  },
  "/models": {
    Python: `import requests

url = "https://api.deepshield.ai/v1/models"
response = requests.get(
    url,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
print(response.json())`,
    cURL: `curl -X GET https://api.deepshield.ai/v1/models \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
    JavaScript: `const response = await fetch(
  "https://api.deepshield.ai/v1/models",
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
    },
  }
);
const models = await response.json();
console.log(models);`,
    "Node.js": `const axios = require("axios");

const { data } = await axios.get(
  "https://api.deepshield.ai/v1/models",
  {
    headers: { Authorization: "Bearer YOUR_API_KEY" },
  }
);
console.log(data);`,
  },
  "/status/{id}": {
    Python: `import requests

job_id = "abc123"
url = f"https://api.deepshield.ai/v1/status/{job_id}"
response = requests.get(
    url,
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)
print(response.json())`,
    cURL: `curl -X GET https://api.deepshield.ai/v1/status/abc123 \\
  -H "Authorization: Bearer YOUR_API_KEY"`,
    JavaScript: `const jobId = "abc123";
const response = await fetch(
  \`https://api.deepshield.ai/v1/status/\${jobId}\`,
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
    },
  }
);
const status = await response.json();
console.log(status);`,
    "Node.js": `const axios = require("axios");
const jobId = "abc123";

const { data } = await axios.get(
  \`https://api.deepshield.ai/v1/status/\${jobId}\`,
  {
    headers: { Authorization: "Bearer YOUR_API_KEY" },
  }
);
console.log(data);`,
  },
  "/stream": {
    Python: `import requests

url = "https://api.deepshield.ai/v1/stream"
with open("live_audio.wav", "rb") as f:
    response = requests.post(
        url,
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        files={"audio": f},
        stream=True
    )
    for chunk in response.iter_lines():
        print(chunk)`,
    cURL: `curl -X POST https://api.deepshield.ai/v1/stream \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -F "audio=@live_audio.wav" \\
  --no-buffer`,
    JavaScript: `const response = await fetch(
  "https://api.deepshield.ai/v1/stream",
  {
    method: "POST",
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
    },
    body: formData,
  }
);

const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  console.log(new TextDecoder().decode(value));
}`,
    "Node.js": `const axios = require("axios");

const { data } = await axios.post(
  "https://api.deepshield.ai/v1/stream",
  form,
  {
    headers: {
      Authorization: "Bearer YOUR_API_KEY",
      ...form.getHeaders(),
    },
    responseType: "stream",
  }
);
data.on("data", (chunk) => console.log(chunk.toString()));`,
  },
};

const languages = ["Python", "cURL", "JavaScript", "Node.js"];

const ApiSection = () => {
  const [selectedEndpoint, setSelectedEndpoint] = useState("/analyze");
  const [selectedLang, setSelectedLang] = useState("Python");
  const [copied, setCopied] = useState(false);

  const currentCode = codeSnippets[selectedEndpoint]?.[selectedLang] ?? "";

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const selectedEp = endpoints.find((e) => e.path === selectedEndpoint);

  return (
    <section id="api" className="py-24 px-6">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="text-center mb-16">
          <p className="text-primary font-mono text-sm tracking-widest uppercase mb-3">
            Developer Tools
          </p>
          <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
            Integrate via API
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Seamlessly integrate DeepShield's deepfake detection into your
            applications with our RESTful API.
          </p>
        </div>

        {/* Step Cards */}
        <div className="grid lg:grid-cols-3 gap-6 mb-10">
          {[
            { icon: <Key className="w-6 h-6 text-primary" />, title: "Get API Key", desc: "Sign up and generate your API key from the dashboard in seconds." },
            { icon: <Terminal className="w-6 h-6 text-primary" />, title: "Make Requests", desc: "Send audio files via REST API and receive analysis results in real-time." },
            { icon: <Zap className="w-6 h-6 text-primary" />, title: "Scale Freely", desc: "Handle thousands of requests per minute with auto-scaling infrastructure." },
          ].map((card) => (
            <div key={card.title} className="glass-card rounded-2xl p-6 text-center">
              <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center mx-auto mb-4">
                {card.icon}
              </div>
              <h3 className="text-lg font-semibold text-foreground mb-2">{card.title}</h3>
              <p className="text-sm text-muted-foreground">{card.desc}</p>
            </div>
          ))}
        </div>

        {/* API Explorer */}
        <div className="glass-card rounded-2xl overflow-hidden border border-border/50">

          {/* Auth Warning */}
          <div className="flex items-start gap-3 px-5 py-4 bg-yellow-500/10 border-b border-yellow-500/20">
            <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-yellow-400">Authentication Required</p>
              <p className="text-xs text-muted-foreground mt-0.5">
                Pass your API key in the{" "}
                <code className="text-yellow-400 bg-yellow-500/10 px-1 rounded">
                  Authorization: Bearer
                </code>{" "}
                header with every request.
              </p>
            </div>
          </div>

          <div className="flex min-h-[420px]">

            {/* Sidebar */}
            <div className="w-64 flex-shrink-0 border-r border-border/50 p-4 flex flex-col gap-1">
              <p className="text-xs font-mono text-muted-foreground uppercase tracking-widest mb-3 px-2">
                Endpoints
              </p>
              {endpoints.map((ep) => (
                <button
                  key={ep.path}
                  onClick={() => setSelectedEndpoint(ep.path)}
                  className={`w-full text-left px-3 py-3 rounded-xl transition-all duration-200 group ${
                    selectedEndpoint === ep.path
                      ? "bg-primary/10 border border-primary/20"
                      : "hover:bg-white/5 border border-transparent"
                  }`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <span className={`text-xs font-bold px-1.5 py-0.5 rounded text-white ${ep.color}`}>
                      {ep.method}
                    </span>
                    <span className="text-sm font-mono text-foreground">{ep.path}</span>
                  </div>
                  <p className="text-xs text-muted-foreground leading-relaxed">{ep.description}</p>
                </button>
              ))}
            </div>

            {/* Code Panel */}
            <div className="flex-1 flex flex-col">

              {/* Endpoint title */}
              <div className="flex items-center gap-3 px-5 py-3 border-b border-border/50">
                <span className={`text-xs font-bold px-2 py-1 rounded text-white ${selectedEp?.color}`}>
                  {selectedEp?.method}
                </span>
                <span className="text-sm font-mono text-foreground">{selectedEndpoint}</span>
                <span className="text-xs text-muted-foreground">— {selectedEp?.description}</span>
              </div>

              {/* Language Tabs */}
              <div className="flex items-center gap-1 px-5 py-3 border-b border-border/50">
                {languages.map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setSelectedLang(lang)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                      selectedLang === lang
                        ? "bg-primary text-white"
                        : "text-muted-foreground hover:text-foreground hover:bg-white/5"
                    }`}
                  >
                    {lang}
                  </button>
                ))}
                <div className="ml-auto">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleCopy}
                    className="h-7 px-2 text-xs"
                  >
                    {copied ? (
                      <Check className="w-3 h-3 text-primary mr-1" />
                    ) : (
                      <Copy className="w-3 h-3 mr-1" />
                    )}
                    {copied ? "Copied" : "Copy"}
                  </Button>
                </div>
              </div>

              {/* Code */}
              <div className="flex-1 p-5 overflow-auto">
                <div className="flex items-center gap-2 mb-3 text-xs text-muted-foreground font-mono">
                  <span className="text-primary">{">"}_</span>
                  <span>
                    {selectedLang === "Python"
                      ? "client.py"
                      : selectedLang === "cURL"
                      ? "terminal"
                      : selectedLang === "JavaScript"
                      ? "client.js"
                      : "client.js"}
                  </span>
                </div>
                <pre className="text-sm font-mono text-muted-foreground leading-relaxed whitespace-pre-wrap">
                  <code>{currentCode}</code>
                </pre>
              </div>
            </div>
          </div>

          {/* Status Bar */}
          <div className="flex items-center gap-2 px-5 py-2.5 border-t border-border/50 bg-white/[0.02]">
            <Circle className="w-2 h-2 fill-emerald-400 text-emerald-400" />
            <span className="text-xs font-mono text-muted-foreground">
              DeepShield API v1.0 · <span className="text-emerald-400">Operational</span>
            </span>
          </div>
        </div>

      </div>
    </section>
  );
};

export default ApiSection;