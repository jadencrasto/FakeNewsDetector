import { Search, RefreshCcw, Shield, Newspaper } from 'lucide-react';
import { AppMode } from './types';

interface InputSectionProps {
  input: string;
  setInput: (val: string) => void;
  sourceUrl: string;
  setSourceUrl: (val: string) => void;
  loading: boolean;
  onAnalyze: () => void;
  mode: AppMode;
  setMode: (mode: AppMode) => void;
}

const InputSection = ({ input, setInput, sourceUrl, setSourceUrl, loading, onAnalyze, mode, setMode }: InputSectionProps) => {
  const isNews = mode === 'news';

  return (
    <section className="text-center space-y-8">
      <div className="space-y-3">
        <h2 className="text-4xl md:text-5xl font-black text-foreground tracking-tight font-display">
          Stay Safe from{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
            {isNews ? 'Fake News.' : 'Online Fraud.'}
          </span>
        </h2>
        <p className="text-muted-foreground max-w-xl mx-auto text-balance">
          {isNews
            ? 'Paste news headlines or articles. Our AI checks credibility against verified sources.'
            : 'Paste messages, UPI links, or suspicious SMS. Our AI analyzes patterns used in Indian phishing attacks.'}
        </p>
      </div>

      {/* Mode Toggle */}
      <div className="inline-flex items-center bg-secondary rounded-xl p-1 gap-1">
        <button
          onClick={() => setMode('scam')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-bold transition-all ${
            !isNews
              ? 'bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-lg'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <Shield className="w-4 h-4" /> Scam Detection
        </button>
        <button
          onClick={() => setMode('news')}
          className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-bold transition-all ${
            isNews
              ? 'bg-gradient-to-r from-primary to-accent text-primary-foreground shadow-lg'
              : 'text-muted-foreground hover:text-foreground'
          }`}
        >
          <Newspaper className="w-4 h-4" /> News Verification
        </button>
      </div>

      <div className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-2xl blur opacity-20 group-focus-within:opacity-40 transition duration-700" />
        <div className="relative bg-card rounded-2xl border border-border p-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value.slice(0, 5000))}
            placeholder={
              isNews
                ? "Paste news headline or article here...\nExample: 'BREAKING: Shocking celebrity scandal revealed!'"
                : "Paste suspicious message, link, or SMS here...\nExample: 'Congratulations! You won ₹50,000. Click here to claim...'"
            }
            className="w-full h-48 bg-transparent border-none focus:ring-0 focus:outline-none text-lg p-4 text-foreground placeholder:text-muted-foreground/40 resize-none font-body"
          />
          {isNews && (
            <div className="px-4 pb-2">
              <input
                type="url"
                value={sourceUrl}
                onChange={(e) => setSourceUrl(e.target.value)}
                placeholder="Source URL (optional) — e.g. https://news-site.com/article"
                className="w-full bg-secondary/50 border border-border/50 rounded-xl px-4 py-2.5 text-sm text-foreground placeholder:text-muted-foreground/40 focus:outline-none focus:ring-1 focus:ring-primary/50 font-body"
              />
            </div>
          )}
          <div className="flex items-center justify-between p-2 border-t border-border/50">
            <span className="text-xs font-mono text-muted-foreground px-2 tabular-nums">
              {input.length} / 5000 characters
            </span>
            <button
              onClick={onAnalyze}
              disabled={loading || !input.trim()}
              className="bg-gradient-to-r from-primary to-accent hover:opacity-90 disabled:opacity-40 text-primary-foreground px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-all active:scale-95 shadow-lg shadow-primary/20 cursor-pointer disabled:cursor-not-allowed"
            >
              {loading ? (
                <><RefreshCcw className="w-4 h-4 animate-spin" /> Analyzing...</>
              ) : (
                <><Search className="w-4 h-4" /> {isNews ? 'Verify News' : 'Analyze for Scams'}</>
              )}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default InputSection;
