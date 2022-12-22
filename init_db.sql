CREATE TABLE IF NOT EXISTS units (
    id SERIAL PRIMARY KEY,
    name_ VARCHAR (64) UNIQUE NOT NULL,
    town VARCHAR (64) NOT NULL,
    base_lvl  INTEGER NOT NULL,
    upgrade_lvl INTEGER NOT NULL,
    attack INTEGER NOT NULL,
    defence INTEGER NOT NULL,
    min_damage INTEGER NOT NULL,
    max_damage INTEGER NOT NULL,
    ammo INTEGER NOT NULL,
    health INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    growth INTEGER NOT NULL,
    ai_value INTEGER NOT NULL,
    cost INTEGER NOT NULL,
    resources_cost VARCHAR (64) NOT NULL
);

CREATE TABLE IF NOT EXISTS specials (
    id SERIAL PRIMARY KEY,
    name_ VARCHAR (64) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS unit_specials (
    id SERIAL PRIMARY KEY,
    special_id INTEGER, 
    unit_id INTEGER,

    FOREIGN KEY(unit_id) REFERENCES units(id),
    FOREIGN KEY(special_id) REFERENCES specials(id)
);

CREATE TABLE IF NOT EXISTS aliases (
    id SERIAL PRIMARY KEY,
    alias VARCHAR (64) UNIQUE NOT NULL,
    unit_id INTEGER,

    FOREIGN KEY(unit_id) REFERENCES units(id)
);

CREATE TABLE IF NOT EXISTS hero_specialisation (
    id SERIAL PRIMARY KEY,
    name_ VARCHAR (64) UNIQUE NOT NULL,
    modification_value INTEGER
);
