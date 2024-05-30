CREATE TABLE nmea_data (
    id SERIAL PRIMARY KEY,
    gps_time TIMESTAMP,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    altitude DOUBLE PRECISION
);