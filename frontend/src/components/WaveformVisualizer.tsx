import { useEffect, useState } from "react";

const WaveformVisualizer = () => {
  const [bars, setBars] = useState<number[]>(Array(40).fill(0.3));

  useEffect(() => {
    const interval = setInterval(() => {
      setBars(prev =>
        prev.map(() => 0.1 + Math.random() * 0.9)
      );
    }, 150);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center justify-center gap-[3px] h-32">
      {bars.map((height, i) => (
        <div
          key={i}
          className="w-[3px] rounded-full bg-primary/70 transition-all duration-150"
          style={{ height: `${height * 100}%` }}
        />
      ))}
    </div>
  );
};

export default WaveformVisualizer;
