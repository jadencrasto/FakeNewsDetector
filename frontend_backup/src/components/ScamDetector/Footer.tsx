const Footer = () => (
  <footer className="max-w-4xl mx-auto px-4 py-12 text-center space-y-4">
    <p className="text-muted-foreground text-sm">
      Protecting Indians from UPI fraud, phishing, and online scams.
    </p>
    <div className="flex justify-center gap-6 text-xs font-bold text-muted-foreground/60 uppercase tracking-widest">
      <a href="#" className="hover:text-primary transition-colors">Privacy Policy</a>
      <a href="#" className="hover:text-primary transition-colors">Terms of Service</a>
      <a href="https://cybercrime.gov.in" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
        Cybercrime Portal
      </a>
    </div>
  </footer>
);

export default Footer;
