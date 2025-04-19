-- Table: users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(254) UNIQUE,
    password VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table: resumes
CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    resume_analysis_id UUID,
    resume_id VARCHAR NOT NULL UNIQUE,
    overall_score INTEGER,
    technical_score INTEGER,
    grammer_score INTEGER,
    is_analysed BOOLEAN,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table: user_resume
CREATE TABLE user_resume (
    id SERIAL PRIMARY KEY,
    resume_id VARCHAR NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table: resume_upload
CREATE TABLE resume_upload (
    id SERIAL PRIMARY KEY,
    resume_id VARCHAR NOT NULL REFERENCES resumes(resume_id) ON DELETE CASCADE,
    filename VARCHAR NOT NULL,
    file_path VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
