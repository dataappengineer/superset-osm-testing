-- SQL script to create and populate test tables for geographic data
-- Run this in Superset SQL Lab after connecting to your database

-- Create cities table
CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    population INTEGER,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create regional stats table  
CREATE TABLE IF NOT EXISTS regional_stats (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    gdp_per_capita INTEGER,
    life_expectancy FLOAT,
    unemployment_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample cities data
INSERT INTO cities (city, country, latitude, longitude, population, category) VALUES
('Roma', 'Italy', 41.9028, 12.4964, 2873000, 'historic'),
('Milano', 'Italy', 45.4642, 9.1900, 1396000, 'business'),
('Napoli', 'Italy', 40.8518, 14.2681, 967000, 'coastal'),
('Torino', 'Italy', 45.0703, 7.6869, 870000, 'industrial'),
('Firenze', 'Italy', 43.7696, 11.2558, 383000, 'artistic'),
('Venezia', 'Italy', 45.4408, 12.3155, 261000, 'historic'),
('Paris', 'France', 48.8566, 2.3522, 2161000, 'capital'),
('Lyon', 'France', 45.764, 4.8357, 515000, 'gastronomy'),
('Marseille', 'France', 43.2965, 5.3698, 862000, 'coastal'),
('Nice', 'France', 43.7102, 7.2620, 343000, 'riviera'),
('Madrid', 'Spain', 40.4168, -3.7038, 3223000, 'capital'),
('Barcelona', 'Spain', 41.3851, 2.1734, 1620000, 'cultural'),
('Valencia', 'Spain', 39.4699, -0.3763, 791000, 'coastal'),
('Sevilla', 'Spain', 37.3891, -5.9845, 688000, 'historic'),
('Berlin', 'Germany', 52.5200, 13.4050, 3669000, 'capital'),
('Munich', 'Germany', 48.1351, 11.5820, 1472000, 'bavarian'),
('Hamburg', 'Germany', 53.5511, 9.9937, 1890000, 'port'),
('Cologne', 'Germany', 50.9375, 6.9603, 1086000, 'historic');

-- Insert regional statistics data
INSERT INTO regional_stats (country, region, latitude, longitude, gdp_per_capita, life_expectancy, unemployment_rate) VALUES
('Italy', 'Lombardia', 45.4642, 9.1900, 35000, 83.2, 6.8),
('Italy', 'Lazio', 41.9028, 12.4964, 33000, 82.8, 9.2),
('Italy', 'Toscana', 43.7696, 11.2558, 32000, 83.1, 6.2),
('Italy', 'Veneto', 45.4408, 12.3155, 33500, 83.4, 5.8),
('France', 'Île-de-France', 48.8566, 2.3522, 56000, 82.4, 7.8),
('France', 'Rhône-Alpes', 45.764, 4.8357, 35000, 82.9, 8.1),
('France', 'Provence-Alpes-Côte d''Azur', 43.2965, 5.3698, 28000, 82.2, 9.5),
('Spain', 'Madrid', 40.4168, -3.7038, 36000, 83.2, 13.8),
('Spain', 'Cataluña', 41.3851, 2.1734, 32000, 83.0, 11.9),
('Spain', 'País Vasco', 43.2627, -2.9253, 38000, 84.1, 9.4),
('Germany', 'Berlin', 52.5200, 13.4050, 40000, 81.2, 9.3),
('Germany', 'Bayern', 48.1351, 11.5820, 47000, 81.5, 3.1),
('Germany', 'Baden-Württemberg', 48.7758, 9.1829, 45000, 81.7, 3.4);