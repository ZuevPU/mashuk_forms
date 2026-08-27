CREATE TABLE IF NOT EXISTS seminar_applications (
    id              BIGSERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    program         TEXT,
    fio_latin       TEXT NOT NULL,
    fio_ru          TEXT,
    birth_date      TEXT,
    gender          TEXT,
    country         TEXT,
    city            TEXT,
    arrival         TEXT,
    citizenship     TEXT,
    all_citizenships TEXT,
    phone           TEXT,
    email           TEXT,
    messenger       JSONB,
    messenger_link  TEXT,
    messenger_other TEXT,
    org_name        TEXT,
    org_spec        TEXT,
    org_location    TEXT,
    position        TEXT,
    audience        JSONB,
    audience_other  TEXT,
    stream          TEXT,
    how_learned     TEXT,
    intl_programs   TEXT,
    intl_details    TEXT,
    ru_programs     TEXT,
    ru_details      TEXT,
    why             TEXT,
    coop            TEXT,
    mentor          TEXT,
    directions      JSONB,
    directions_other TEXT,
    address         TEXT,
    passport_series TEXT,
    passport_number TEXT,
    passport_date   TEXT,
    passport_issued TEXT,
    portfolio_path  TEXT,
    consent_path    TEXT,
    payload_raw     JSONB
);

CREATE INDEX IF NOT EXISTS seminar_applications_email_idx
    ON seminar_applications (email);
CREATE INDEX IF NOT EXISTS seminar_applications_created_idx
    ON seminar_applications (created_at DESC);

CREATE TABLE IF NOT EXISTS participant_details (
    id                   BIGSERIAL PRIMARY KEY,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fio_latin            TEXT NOT NULL,
    gender               TEXT,
    citizenship          TEXT,
    other_citizenships   TEXT,
    other_citizenships_detail TEXT,
    health_limits        TEXT,
    allergies            TEXT,
    allergies_detail     TEXT,
    health_conditions    TEXT,
    health_conditions_detail TEXT,
    meal_type            TEXT,
    meal_type_other      TEXT,
    id_doc_type          TEXT,
    id_doc_type_other    TEXT,
    id_doc_series        TEXT,
    id_doc_number        TEXT,
    id_doc_issued        TEXT,
    id_doc_valid_from    TEXT,
    id_doc_valid_to      TEXT,
    id_doc_issuer        TEXT,
    entry_doc_name       TEXT,
    entry_doc_series     TEXT,
    entry_doc_number     TEXT,
    entry_doc_issued     TEXT,
    entry_doc_valid_from TEXT,
    entry_doc_valid_to   TEXT,
    entry_doc_issuer     TEXT,
    stream               TEXT,
    depart_country       TEXT,
    depart_city          TEXT,
    return_ticket        TEXT,
    baggage              TEXT,
    visa_needed          TEXT,
    visa_current         TEXT,
    visa_status          TEXT,
    transit_visa         TEXT,
    agree_tickets        TEXT,
    agree_participate    TEXT,
    agree_notice         TEXT,
    agree_truth          TEXT,
    agree_extra_docs     TEXT,
    agree_refusal        TEXT,
    agree_logistics_city TEXT,
    agree_logistics_fixed TEXT,
    agree_logistics_change TEXT,
    payload_raw          JSONB
);

CREATE INDEX IF NOT EXISTS participant_details_created_idx
    ON participant_details (created_at DESC);
CREATE INDEX IF NOT EXISTS participant_details_stream_idx
    ON participant_details (stream);

ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS gender TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS citizenship TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS other_citizenships TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS other_citizenships_detail TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS id_doc_type_other TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS visa_current TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS visa_status TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS allergies TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS allergies_detail TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS health_conditions TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS health_conditions_detail TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS meal_type_other TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS agree_participate TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS agree_logistics_city TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS agree_logistics_fixed TEXT;
ALTER TABLE participant_details ADD COLUMN IF NOT EXISTS agree_logistics_change TEXT;
