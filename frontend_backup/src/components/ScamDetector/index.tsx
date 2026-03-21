import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { AnalysisResult } from './types';
import Header from './Header';
import InputSection from './InputSection';
import ResultsSection from './ResultsSection';
import StatsSection from './StatsSection';
import Footer from './Footer';

const ScamDetector = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const analyzeScam = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input }),
      });
      if (!response.ok) throw new Error('Network error');
      const data = await response.json();
      setResult(data);
    } catch {
      toast.error('Failed to connect to analysis engine. Please try again.');
      // Fallback demo result for UI testing
      setResult({
        risk_score: 85,
        classification: 'scam',
        indicators: [
          { type: 'urgency', severity: 'high', description: 'Contains urgency keywords designed to pressure quick action' },
          { type: 'financial_lure', severity: 'critical', description: 'Promises unrealistic monetary rewards (₹50,000)' },
          { type: 'suspicious_link', severity: 'high', description: 'Contains unverified external URL' },
        ],
        recommendations: [
          '🚫 DO NOT click any links in the message',
          '🚫 DO NOT share personal or banking information',
          '📱 Block the sender immediately',
          '🔒 Report to cybercrime.gov.in',
        ],
        urls_found: ['http://scam.com'],
        analysis_time_ms: 15,
        timestamp: new Date().toISOString(),
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setInput('');
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-body selection:bg-primary/30">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-12 space-y-12">
        <InputSection input={input} setInput={setInput} loading={loading} onAnalyze={analyzeScam} />
        <AnimatePresence mode="wait">
          {result && <ResultsSection result={result} onReset={handleReset} />}
        </AnimatePresence>
        <StatsSection />
      </main>
      <Footer />
    </div>
  );
};

export default ScamDetector;
