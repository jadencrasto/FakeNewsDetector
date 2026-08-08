import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, Shield, Activity } from 'lucide-react';
import { PieChart, Pie, Cell, LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Skeleton } from '@/components/ui/skeleton';

interface AnalyticsData {
  total_scans: number;
  scams_detected: number;
  detection_rate: number;
  avg_risk_score: number;
  classification_breakdown: { name: string; value: number }[];
  scans_over_time: { date: string; scans: number }[];
  top_scam_types: { type: string; count: number }[];
}

const COLORS = {
  safe: 'hsl(142, 71%, 45%)',
  suspicious: 'hsl(38, 92%, 50%)',
  scam: 'hsl(0, 84%, 60%)',
  primary: 'hsl(262, 83%, 58%)',
};

const DEMO_DATA: AnalyticsData = {
  total_scans: 12847,
  scams_detected: 8432,
  detection_rate: 65.6,
  avg_risk_score: 62,
  classification_breakdown: [
    { name: 'Safe', value: 3200 },
    { name: 'Suspicious', value: 1215 },
    { name: 'Scam', value: 8432 },
  ],
  scans_over_time: [
    { date: 'Mon', scans: 1200 },
    { date: 'Tue', scans: 1800 },
    { date: 'Wed', scans: 2100 },
    { date: 'Thu', scans: 1600 },
    { date: 'Fri', scans: 2400 },
    { date: 'Sat', scans: 1900 },
    { date: 'Sun', scans: 1847 },
  ],
  top_scam_types: [
    { type: 'Phishing', count: 3200 },
    { type: 'UPI Fraud', count: 2100 },
    { type: 'Lottery', count: 1500 },
    { type: 'KYC Scam', count: 900 },
    { type: 'Job Fraud', count: 732 },
  ],
};

const PIE_COLORS = [COLORS.safe, COLORS.suspicious, COLORS.scam];

const formatNumber = (num: number | undefined | null) => (num ?? 0).toLocaleString();

const StatCard = ({ icon: Icon, label, value, accent }: { icon: typeof Shield; label: string; value: string; accent: string }) => (
  <div className="relative overflow-hidden rounded-2xl bg-surface border border-border p-5 group hover:border-primary/50 transition-all">
    <div className={`absolute top-0 right-0 -mr-4 -mt-4 h-24 w-24 rounded-full blur-3xl opacity-20`} style={{ background: accent }} />
    <Icon className="w-5 h-5 mb-3" style={{ color: accent }} />
    <div className="text-2xl font-black tracking-tight text-foreground tabular-nums font-display">{value}</div>
    <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mt-1">{label}</div>
  </div>
);

const ChartCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <div className="rounded-2xl bg-surface border border-border p-5">
    <h4 className="text-sm font-semibold text-foreground mb-4 font-display">{title}</h4>
    {children}
  </div>
);

const AnalyticsDashboard = () => {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/analytics');
        if (!response.ok) throw new Error('Failed to fetch');
        const json = await response.json();
        console.log('Analytics data:', json);

        // Transform nested API response to flat format
        const transformed: AnalyticsData = {
          total_scans: Number(json.overview?.total_scans ?? 0),
          scams_detected: Number(json.overview?.scams_detected ?? 0),
          detection_rate: Number(json.overview?.detection_rate ?? 0),
          avg_risk_score: Number(json.overview?.avg_risk_score ?? 0),
          classification_breakdown: (json.classification_breakdown?.labels ?? []).map(
            (label: string, i: number) => ({
              name: label,
              value: json.classification_breakdown.data[i] ?? 0,
            })
          ),
          scans_over_time: (json.scans_timeline?.labels ?? []).map(
            (label: string, i: number) => ({
              date: label,
              scans: json.scans_timeline.data[i] ?? 0,
            })
          ),
          top_scam_types: json.top_scam_types ?? [],
        };
        setData(transformed);
      } catch {
        setData(DEMO_DATA);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <section className="space-y-6 pt-12 border-t border-border">
        <h3 className="text-xl font-bold font-display text-foreground">📊 Analytics Dashboard</h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 rounded-2xl" />)}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => <Skeleton key={i} className="h-64 rounded-2xl" />)}
        </div>
      </section>
    );
  }

  if (!data) {
    return (
      <section className="pt-12 border-t border-border text-center py-16">
        <p className="text-muted-foreground">No scans yet. Try analyzing some messages!</p>
      </section>
    );
  }

  const rate = data.detection_rate ?? 0;
  const rateColor = rate > 60 ? COLORS.scam : rate > 30 ? COLORS.suspicious : COLORS.safe;

  return (
    <motion.section
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="space-y-6 pt-12 border-t border-border"
    >
      <h3 className="text-xl font-bold font-display text-foreground">📊 Analytics Dashboard</h3>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={BarChart3} label="Total Scans" value={formatNumber(data.total_scans)} accent={COLORS.primary} />
        <StatCard icon={Shield} label="Scams Detected" value={formatNumber(data.scams_detected)} accent={COLORS.scam} />
        <StatCard icon={TrendingUp} label="Detection Rate" value={`${rate}%`} accent={rateColor} />
        <StatCard icon={Activity} label="Avg Risk Score" value={`${data.avg_risk_score ?? 0}/100`} accent={COLORS.suspicious} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ChartCard title="Classification Breakdown">
          {(data.classification_breakdown?.length ?? 0) > 0 ? (
            <>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={data.classification_breakdown} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={70} strokeWidth={0}>
                    {data.classification_breakdown.map((_, i) => (
                      <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ background: 'hsl(222, 47%, 14%)', border: '1px solid hsl(217, 33%, 20%)', borderRadius: '0.75rem', color: 'hsl(210, 40%, 98%)' }}
                    itemStyle={{ color: 'hsl(210, 40%, 98%)' }}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="flex justify-center gap-4 mt-2">
                {data.classification_breakdown.map((entry, i) => (
                  <div key={entry.name} className="flex items-center gap-1.5 text-xs text-muted-foreground">
                    <span className="w-2.5 h-2.5 rounded-full" style={{ background: PIE_COLORS[i] }} />
                    {entry.name}
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="text-muted-foreground text-sm text-center py-16">No data available yet</p>
          )}
        </ChartCard>

        <ChartCard title="Scans Over Last 7 Days">
          {(data.scans_over_time?.length ?? 0) > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={data.scans_over_time}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(217, 33%, 20%)" />
                <XAxis dataKey="date" tick={{ fill: 'hsl(215, 20%, 65%)', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: 'hsl(215, 20%, 65%)', fontSize: 12 }} axisLine={false} tickLine={false} />
                <Tooltip
                  contentStyle={{ background: 'hsl(222, 47%, 14%)', border: '1px solid hsl(217, 33%, 20%)', borderRadius: '0.75rem', color: 'hsl(210, 40%, 98%)' }}
                  itemStyle={{ color: 'hsl(210, 40%, 98%)' }}
                />
                <Line type="monotone" dataKey="scans" stroke={COLORS.primary} strokeWidth={2.5} dot={{ fill: COLORS.primary, r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-muted-foreground text-sm text-center py-16">No data available yet</p>
          )}
        </ChartCard>

        <ChartCard title="Top Scam Types">
          {(data.top_scam_types?.length ?? 0) > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.top_scam_types} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(217, 33%, 20%)" />
                <XAxis type="number" tick={{ fill: 'hsl(215, 20%, 65%)', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis dataKey="type" type="category" tick={{ fill: 'hsl(215, 20%, 65%)', fontSize: 11 }} axisLine={false} tickLine={false} width={70} />
                <Tooltip
                  contentStyle={{ background: 'hsl(222, 47%, 14%)', border: '1px solid hsl(217, 33%, 20%)', borderRadius: '0.75rem', color: 'hsl(210, 40%, 98%)' }}
                  itemStyle={{ color: 'hsl(210, 40%, 98%)' }}
                />
                <Bar dataKey="count" fill={COLORS.primary} radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-muted-foreground text-sm text-center py-16">No data available yet</p>
          )}
        </ChartCard>
      </div>
    </motion.section>
  );
};

export default AnalyticsDashboard;
