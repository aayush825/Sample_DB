-- PRISM Web Database Setup
-- PostgreSQL Database and Table Creation

-- Create database (run this as postgres superuser)
-- If database already exists, skip this step
-- CREATE DATABASE prism_db;

-- Connect to the database
\c prism_db;

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS aws_recommendation_consolidate;

-- Create the recommendations table
CREATE TABLE aws_recommendation_consolidate (
    id BIGSERIAL PRIMARY KEY,
    type TEXT,
    account TEXT,
    region TEXT,
    resource_name TEXT,
    resource_id TEXT,
    service TEXT,
    sub_service TEXT,
    recommendation TEXT,
    description TEXT,
    potential NUMERIC(18, 4),
    actual_cost NUMERIC(18, 4),
    target_cost NUMERIC(18, 4),
    current_configuration TEXT,
    expected_configuration TEXT,
    justifications TEXT,
    tags_json JSONB,
    actionable BOOLEAN,
    risk_level TEXT,
    impact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on potential for faster sorting
CREATE INDEX idx_potential ON aws_recommendation_consolidate(potential DESC);
CREATE INDEX idx_type ON aws_recommendation_consolidate(type);

-- Insert sample data for testing
INSERT INTO aws_recommendation_consolidate 
(type, description, potential, actual_cost, target_cost, recommendation, resource_name, region, service, actionable) 
VALUES 
('AWS', 'Recommended to right-size EC2 instance from m5.large to m5.medium in us-east-1', 781.12, 1200.00, 418.88, 'Right-size EC2 instance', 'i-0abc123def456', 'us-east-1', 'EC2', true),
('AWS', 'Delete unused EBS volume in us-east-1 region - no attachments found', 750.50, 750.50, 0.00, 'Delete unused volume', 'vol-0xyz789', 'us-east-1', 'EBS', true),
('Databricks', 'Optimize cluster auto-scaling configuration to reduce idle time', 680.00, 1100.00, 420.00, 'Optimize cluster auto-scaling', 'cluster-abc123', 'us-west-2', 'Databricks Cluster', true),
('Snowflakes', 'Reduce warehouse size from X-Large to Large based on usage patterns', 620.30, 1020.30, 400.00, 'Reduce warehouse size', 'COMPUTE_WH', 'aws-us-east-1', 'Warehouse', true),
('AWS', 'Migrate to newer generation RDS instance (db.m5 to db.m6g) for better performance', 580.00, 900.00, 320.00, 'Migrate RDS instance', 'mydb-instance', 'us-west-2', 'RDS', true),
('Google Cloud', 'Delete unattached persistent disks in us-central1 region', 550.00, 550.00, 0.00, 'Delete unattached disks', 'disk-persistent-1', 'us-central1', 'Compute Engine', true),
('AWS', 'Convert On-Demand instances to Reserved Instances for long-running workloads', 480.00, 1080.00, 600.00, 'Purchase Reserved Instances', 'i-0def456abc789', 'eu-west-1', 'EC2', true),
('Databricks', 'Schedule cluster auto-termination during non-business hours', 450.00, 850.00, 400.00, 'Configure auto-termination', 'cluster-xyz789', 'us-east-1', 'Databricks Cluster', true);

-- Verify data insertion
SELECT 
    id,
    type as platform,
    description,
    potential as savings,
    actual_cost,
    target_cost
FROM aws_recommendation_consolidate
ORDER BY potential DESC
LIMIT 10;

-- Show table summary
SELECT 
    type as platform,
    COUNT(*) as recommendation_count,
    SUM(potential) as total_potential_savings,
    AVG(potential) as avg_savings
FROM aws_recommendation_consolidate
GROUP BY type
ORDER BY total_potential_savings DESC;
