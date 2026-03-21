import { Search, RefreshCcw } from 'lucide-react';

interface InputSectionProps {
  input: string;
  setInput: (val: string) => void;
  loading: boolean;
  onAnalyze: () => void;
}

const InputSection = ({ input, setInput, loading, onAnalyze }: InputSectionProps) => (
  <section className="text-center space-y-8">
    <div className="space-y-3">
      <h2 className="text-4xl md:text-5xl font-black text-foreground tracking-tight font-display">
        Stay Safe from{' '}
        <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">
          Online Fraud.
        </span>
      </h2>
      <p className="text-muted-foreground max-w-xl mx-auto text-balance">
        Paste messages, UPI links, or suspicious SMS. Our AI analyzes patterns used in Indian phishing attacks.
      </p>
    </div>

    <div className="relative group">
      <div className="absolute -inset-1 bg-gradient-to-r from-primary to-accent rounded-2xl blur opacity-20 group-focus-within:opacity-40 transition duration-700" />
      <div className="relative bg-card rounded-2xl border border-border p-2">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value.slice(0, 5000))}
          placeholder="Paste suspicious message, link, or SMS here...&#10;Example: 'Congratulations! You won ₹50,000. Click here to claim...'"
          className="w-full h-48 bg-transparent border-none focus:ring-0 focus:outline-none text-lg p-4 text-foreground placeholder:text-muted-foreground/40 resize-none font-body"
        />
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
              <><Search className="w-4 h-4" /> Analyze Now</>
            )}
          </button>
        </div>
      </div>
    </div>
  </section>
);

export default InputSection;
