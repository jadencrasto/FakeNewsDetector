export type AppMode = 'scam' | 'news';

export interface Indicator {
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
}

export interface AnalysisResult {
  risk_score: number;
  classification: 'safe' | 'suspicious' | 'scam' | 'verified' | 'unverified' | 'false';
  indicators: Indicator[];
  recommendations: string[];
  urls_found: string[];
  analysis_time_ms: number;
  timestamp: string;
}
