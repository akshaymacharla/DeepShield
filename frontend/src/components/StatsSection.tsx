const StatsSection = () => {
  const stats = [
    { value: "98.7%", label: "Detection Accuracy" },
    { value: "<2s", label: "Analysis Time" },
    { value: "50K+", label: "Voices Analyzed" },
    { value: "99+", label: "Languages Supported" },
  ];

  return (
    <section className="py-12 px-6 border-y border-border/50">
      <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
        {stats.map((stat) => (
          <div key={stat.label} className="text-center">
            <p className="text-3xl md:text-4xl font-bold gradient-text mb-1">{stat.value}</p>
            <p className="text-sm text-muted-foreground">{stat.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default StatsSection;
