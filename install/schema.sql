CREATE TABLE prefixes (
    guild_id bigint NOT NULL,
    prefix text
);

ALTER TABLE ONLY prefixes
    ADD CONSTRAINT prefixes_guild_id_key UNIQUE (guild_id);

CREATE TABLE profile (
    user_id bigint NOT NULL,
    description text,
    socials text,
    friends text
);

ALTER TABLE ONLY profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (user_id);

CREATE TABLE blacklist (
    object_id BIGINT NOT NULL,
    object_type text NOT NULL
);

ALTER TABLE ONLY blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (object_id, object_type);