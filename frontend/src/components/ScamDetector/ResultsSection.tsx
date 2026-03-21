import { motion } from 'framer-motion';
import { ShieldAlert, ShieldCheck, AlertTriangle, AlertCircle, CheckCircle2, Link2, Newspaper } from 'lucide-react';
import { AnalysisResult, AppMode } from './types';
import RiskMeter from './RiskMeter';
import SeverityBadge from './SeverityBadge';
import { toast } from 'sonner';

interface ResultsSectionProps {
  result: AnalysisResult;
  onReset: () => void;
  mode: AppMode;
}

const classificationConfig: Record<string, { icon: typeof ShieldAlert; label: string; title: string; classes: string }> = {
  scam: {
    icon: ShieldAlert,
    label: 'SCAM',
    title: 'Highly Likely a Scam',
    classes: 'bg-scam/10 border-scam/20 text-scam',
  },
  suspicious: {
    icon: AlertTriangle,
    label: 'SUSPICIOUS',
    title: 'Proceed with Caution',
    classes: 'bg-suspicious/10 border-suspicious/20 text-suspicious',
  },
  safe: {
    icon: ShieldCheck,
    label: 'SAFE',
    title: 'Looks Safe to Us',
    classes: 'bg-safe/10 border-safe/20 text-safe',
  },
  verified: {
    icon: CheckCircle2,
    label: 'VERIFIED',
    title: 'News Appears Credible',
    classes: 'bg-safe/10 border-safe/20 text-safe',
  },
  unverified: {
    icon: AlertTriangle,
    label: 'UNVERIFIED',
    title: 'Could Not Verify This News',
    classes: 'bg-suspicious/10 border-suspicious/20 text-suspicious',
  },
  false: {
    icon: ShieldAlert,
    label: 'FALSE',
    title: 'Likely Fake News',
    classes: 'bg-scam/10 border-scam/20 text-scam',
  },
};

const ResultsSection = ({ result, onReset, mode }: ResultsSectionProps) => {
  const config = classificationConfig[result.classification] || classificationConfig.safe;
  const Icon = config.icon;
  const isNews = mode === 'news';
  const scoreLabel = isNews ? 'Credibility' : 'Risk Score';

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="space-y-6"
    >
      <div className="bg-card border border-border rounded-3xl p-8 overflow-hidden relative">
        <div className="absolute top-0 right-0 -mr-20 -mt-20 h-60 w-60 rounded-full bg-primary/5 blur-3xl" />
        <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
          <RiskMeter score={result.risk_score} label={scoreLabel} />
          <div className="flex-1 text-center md:text-left space-y-4">
            <div className="space-y-2">
              <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border text-xs font-black uppercase tracking-widest ${config.classes}`}>
                <Icon className="w-3 h-3" />
                {config.label}
              </div>
              <h3 className="text-2xl font-bold text-foreground font-display">{config.title}</h3>
              <p className="text-xs text-muted-foreground tabular-nums">
                Analysis completed in {result.analysis_time_ms}ms
              </p>
            </div>
            <div className="flex flex-wrap justify-center md:justify-start gap-3">
              <button
                onClick={onReset}
                className="px-4 py-2 rounded-xl bg-secondary hover:bg-secondary/80 text-secondary-foreground text-sm font-bold transition-colors"
              >
                {isNews ? 'Verify Another' : 'Analyze Another'}
              </button>
              <button
                onClick={() => toast.success(isNews ? 'Reported as fake news. Thank you!' : 'Reported as scam. Thank you!')}
                className="px-4 py-2 rounded-xl border border-scam/30 text-scam hover:bg-scam/10 text-sm font-bold transition-colors"
              >
                {isNews ? 'Report as Fake' : 'Report as Scam'}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-surface border border-border rounded-2xl p-6">
          <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" /> {isNews ? 'Credibility Indicators' : 'Risk Indicators'}
          </h4>
          <div className="space-y-3">
            {result.indicators.map((ind, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
                className="p-3 rounded-xl bg-background border border-border flex flex-col gap-2"
              >
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-foreground uppercase">{ind.type}</span>
                  <SeverityBadge level={ind.severity} />
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">{ind.description}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="bg-surface border border-border rounded-2xl p-6">
          <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> {isNews ? 'Verification Notes' : 'Safety Steps'}
          </h4>
          <ul className="space-y-3">
            {result.recommendations.map((rec, i) => (
              <motion.li
                key={i}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1, ease: [0.16, 1, 0.3, 1] }}
                className="flex gap-3 p-3 rounded-xl bg-primary/5 border border-primary/10 text-sm text-muted-foreground"
              >
                <span className="shrink-0">{rec.split(' ')[0]}</span>
                <span>{rec.split(' ').slice(1).join(' ')}</span>
              </motion.li>
            ))}
          </ul>
        </div>
      </div>

      {(result.urls_found?.length ?? 0) > 0 && (
        <div className="bg-surface border border-border rounded-2xl p-6">
          <h4 className="text-sm font-bold text-muted-foreground uppercase tracking-widest mb-4 flex items-center gap-2">
            <Link2 className="w-4 h-4" /> {isNews ? 'Sources Found' : 'Suspicious URLs Detected'}
          </h4>
          <div className="space-y-2">
            {result.urls_found?.map((url, i) => (
              <div key={i} className="flex items-center gap-2 p-3 rounded-xl bg-scam/5 border border-scam/10 text-sm text-scam font-mono break-all">
                <AlertCircle className="w-4 h-4 shrink-0" />
                {url}
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.section>
  );
};

export default ResultsSection;
