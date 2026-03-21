-- AI Scam Detector Database Schema
-- PostgreSQL 16+

-- ============================================
-- TABLE 1: Scans (Main table - stores all analyses)
-- ============================================
CREATE TABLE IF NOT EXISTS scans (
    scan_id SERIAL PRIMARY KEY,
    
    -- Input data
    input_text TEXT NOT NULL,
    input_hash VARCHAR(64) NOT NULL,
    
    -- Results
    risk_score INTEGER NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
    classification VARCHAR(20) NOT NULL CHECK (classification IN ('safe', 'suspicious', 'scam')),
    
    -- Details (stored as JSON for flexibility)
    indicators JSONB,
    recommendations JSONB,
    urls_found TEXT[],
    score_breakdown JSONB,
    
    -- Metadata
    analysis_time_ms INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 2: Known Scams (Database of confirmed scams)
-- ============================================
CREATE TABLE IF NOT EXISTS known_scams (
    scam_id SERIAL PRIMARY KEY,
    
    -- Classification
    scam_type VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    description TEXT,
    
    -- Content
    content_sample TEXT,
    content_hash VARCHAR(64) UNIQUE,
    
    -- URL information
    url VARCHAR(500),
    domain VARCHAR(255),
    
    -- Severity
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    
    -- Verification
    reporter_count INTEGER DEFAULT 1,
    verified BOOLEAN DEFAULT FALSE,
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLE 3: Blacklisted Domains
-- ============================================
CREATE TABLE IF NOT EXISTS blacklisted_domains (
    domain_id SERIAL PRIMARY KEY,
    
    domain VARCHAR(255) UNIQUE NOT NULL,
    reason TEXT,
    source VARCHAR(50),
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    
    -- Tracking
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_count INTEGER DEFAULT 1,
    verified BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE
);

-- ============================================
-- TABLE 4: User Reports
-- ============================================
CREATE TABLE IF NOT EXISTS user_reports (
    report_id SERIAL PRIMARY KEY,
    
    scan_id INTEGER REFERENCES scans(scan_id) ON DELETE CASCADE,
    
    -- Report details
    report_type VARCHAR(50) NOT NULL,
    is_scam BOOLEAN,
    comments TEXT,
    evidence_url TEXT,
    
    -- Review status
    status VARCHAR(20) DEFAULT 'pending' 
        CHECK (status IN ('pending', 'reviewed', 'verified', 'rejected')),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- INDEXES for Performance
-- ============================================
CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_scans_classification ON scans(classification);
CREATE INDEX IF NOT EXISTS idx_scans_risk_score ON scans(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_scans_input_hash ON scans(input_hash);

CREATE INDEX IF NOT EXISTS idx_known_scams_type ON known_scams(scam_type);
CREATE INDEX IF NOT EXISTS idx_known_scams_hash ON known_scams(content_hash);
CREATE INDEX IF NOT EXISTS idx_known_scams_active ON known_scams(active) WHERE active = TRUE;

CREATE INDEX IF NOT EXISTS idx_blacklist_domain ON blacklisted_domains(domain);
CREATE INDEX IF NOT EXISTS idx_blacklist_active ON blacklisted_domains(active) WHERE active = TRUE;

-- ============================================
-- SEED DATA (Sample scams for testing)
-- ============================================
INSERT INTO known_scams (scam_type, title, description, content_hash, severity, verified, reporter_count) VALUES
('fake_prize_upi', 'KBC Fake Lottery', 'Fake KBC lottery scam asking for UPI PIN', 'hash_kbc_001', 'critical', true, 150),
('fake_job_advance_fee', 'Data Entry Job Scam', 'Fake work-from-home jobs requiring registration fee', 'hash_job_001', 'high', true, 80),
('phishing_bank', 'SBI Account Phishing', 'Fake SBI messages asking to verify account', 'hash_sbi_001', 'critical', true, 200)
ON CONFLICT (content_hash) DO NOTHING;

INSERT INTO blacklisted_domains (domain, reason, source, severity, verified, report_count) VALUES
('kbc-lottery.tk', 'Fake KBC lottery scam', 'manual_review', 'critical', true, 45),
('sbi-verify-india.com', 'SBI impersonation phishing', 'manual_review', 'critical', true, 67),
('paytm-prize.tk', 'Fake Paytm lottery', 'user_report', 'high', true, 28)
ON CONFLICT (domain) DO NOTHING;