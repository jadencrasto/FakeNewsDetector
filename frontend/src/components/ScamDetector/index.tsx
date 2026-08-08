import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { AnalysisResult, AppMode } from './types';
import Header from './Header';
import InputSection from './InputSection';
import ResultsSection from './ResultsSection';
import StatsSection from './StatsSection';
import AnalyticsDashboard from './AnalyticsDashboard';
import Footer from './Footer';

const ScamDetector = () => {
  const [input, setInput] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [mode, setMode] = useState<AppMode>('scam');

  const analyze = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const endpoint = mode === 'news'
        ? 'http://localhost:5000/api/verify-news'
        : 'http://localhost:5000/api/analyze';

      const body = mode === 'news'
        ? { text: input, ...(sourceUrl.trim() && { url: sourceUrl.trim() }) }
        : { input };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      if (!response.ok) throw new Error('Network error');
      const data = await response.json();
      setResult({
        ...data,
        risk_score: data.risk_score ?? data.credibility_score ?? 0,
        indicators: data.indicators ?? [],
        recommendations: data.recommendations ?? [],
        urls_found: data.urls_found ?? [],
      });
    } catch {
      toast.error('Failed to connect to analysis engine. Showing demo result.');
      if (mode === 'news') {
        setResult({
          risk_score: 30,
          classification: 'unverified',
          indicators: [
            { type: 'sensationalism', severity: 'high', description: 'Headline uses clickbait language and sensational claims' },
            { type: 'no_source', severity: 'medium', description: 'No credible source attribution found' },
            { type: 'emotional_language', severity: 'medium', description: 'Uses emotionally charged words to provoke reaction' },
          ],
          recommendations: [
            '🔍 Cross-check with trusted news sources like PTI, NDTV, or BBC',
            '🔗 Look for the original source or press release',
            '📅 Check the date — old news is often recirculated',
            '🧠 Be skeptical of headlines that seem too shocking',
          ],
          urls_found: [],
          analysis_time_ms: 12,
          timestamp: new Date().toISOString(),
        });
      } else {
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
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setInput('');
    setSourceUrl('');
  };

  const handleModeChange = (newMode: AppMode) => {
    if (newMode !== mode) {
      setMode(newMode);
      handleReset();
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-body selection:bg-primary/30">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-12 space-y-12">
        <InputSection
          input={input}
          setInput={setInput}
          sourceUrl={sourceUrl}
          setSourceUrl={setSourceUrl}
          loading={loading}
          onAnalyze={analyze}
          mode={mode}
          setMode={handleModeChange}
        />
        <AnimatePresence mode="wait">
          {result && <ResultsSection result={result} onReset={handleReset} mode={mode} />}
        </AnimatePresence>
        <StatsSection />
        <AnalyticsDashboard />
      </main>
      <Footer />
    </div>
  );
};

export default ScamDetector;
