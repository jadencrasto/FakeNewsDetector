const severityStyles: Record<string, string> = {
  critical: "bg-scam/10 text-scam border-scam/20",
  high: "bg-suspicious/10 text-suspicious border-suspicious/20",
  medium: "bg-suspicious/10 text-suspicious border-suspicious/20",
  low: "bg-accent/10 text-accent border-accent/20",
};

const SeverityBadge = ({ level }: { level: string }) => (
  <span className={`px-2 py-0.5 rounded-full text-[10px] font-black border uppercase tracking-wider ${severityStyles[level] || severityStyles.low}`}>
    {level}
  </span>
);

export default SeverityBadge;
