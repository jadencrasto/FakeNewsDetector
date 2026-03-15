import { Search, Shield, Users } from 'lucide-react';

const stats = [
  { label: 'Total Scans', value: '1.2M+', icon: Search },
  { label: 'Scams Blocked', value: '840K', icon: Shield },
  { label: 'Users Protected', value: '250K+', icon: Users },
];

const StatsSection = () => (
  <section className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-12 border-t border-border">
    {stats.map(({ label, value, icon: Icon }) => (
      <div key={label} className="relative overflow-hidden rounded-2xl bg-surface border border-border p-6 transition-all hover:border-primary/50 group">
        <div className="absolute top-0 right-0 -mr-4 -mt-4 h-24 w-24 rounded-full bg-primary/10 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
        <Icon className="w-6 h-6 text-primary mb-4" />
        <div className="text-3xl font-black tracking-tight text-foreground tabular-nums font-display">{value}</div>
        <div className="text-sm font-semibold text-muted-foreground uppercase tracking-wider">{label}</div>
      </div>
    ))}
  </section>
);

export default StatsSection;
