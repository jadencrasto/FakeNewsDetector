import { Shield, ExternalLink } from 'lucide-react';

const Header = () => (
  <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl">
    <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg shadow-primary/20">
          <Shield className="text-primary-foreground w-6 h-6" />
        </div>
        <div>
          <h1 className="text-lg font-black text-foreground leading-none font-display">AI Scam Detector</h1>
          <p className="text-[11px] text-muted-foreground font-semibold tracking-widest uppercase">Stay Safe from Online Scams</p>
        </div>
      </div>
      <a
        href="https://cybercrime.gov.in"
        target="_blank"
        rel="noopener noreferrer"
        className="text-xs font-bold text-primary hover:text-accent transition-colors flex items-center gap-1 uppercase tracking-wider"
      >
        Report Fraud <ExternalLink className="w-3 h-3" />
      </a>
    </div>
  </header>
);

export default Header;
