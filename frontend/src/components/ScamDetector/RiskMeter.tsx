import { motion } from 'framer-motion';

interface RiskMeterProps {
  score: number;
  label?: string;
}

const RiskMeter = ({ score, label = 'Risk Score' }: RiskMeterProps) => {
  const getColor = () => {
    if (score > 60) return 'text-scam';
    if (score > 30) return 'text-suspicious';
    return 'text-safe';
  };

  return (
    <div className="relative w-40 h-40 flex items-center justify-center shrink-0">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="70" fill="transparent" stroke="currentColor" strokeWidth="12" className="text-border" />
        <motion.circle
          cx="80" cy="80" r="70" fill="transparent" stroke="currentColor" strokeWidth="12"
          strokeDasharray={440}
          initial={{ strokeDashoffset: 440 }}
          animate={{ strokeDashoffset: 440 - (440 * score) / 100 }}
          transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
          className={getColor()}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-4xl font-black text-foreground tabular-nums font-display">{score}</span>
        <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">{label}</span>
      </div>
    </div>
  );
};

export default RiskMeter;
