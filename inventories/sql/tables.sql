/*
CREATE TABLE mtgcards
                    (name TEXT, --Orginal Type <class 'str'>
                    layout TEXT, --Orginal Type <class 'str'>
                    mana_cost TEXT, --Orginal Type <class 'str'>
                    cmc INTEGER, --Orginal Type <class 'int'>
                    colors TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    -- color_identity TEXT, --Orginal Type <class 'list'> Un-needed as it's just a short version of colors
                    names ERROR, --Orginal Type <class 'NoneType'> This will have to be a JSON of {'names': [NAMES]}
                    type TEXT, --Orginal Type <class 'str'>
                    supertypes TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    subtypes TEXT, --Orginal Type <class 'list'>  This should be a comma seperated list of all the values
                    types TEXT, --Orginal Type <class 'list'> This should be a comma seperated list of all the values
                    rarity TEXT, --Orginal Type <class 'str'>
                    "text" TEXT, --Orginal Type <class 'str'> This had to be changed
                    flavor TEXT, --Orginal Type <class 'NoneType'>
                    artist TEXT, --Orginal Type <class 'str'>
                    "number" TEXT, --Orginal Type <class 'str'>
                    "power" TEXT, --Orginal Type <class 'str'>
                    toughness TEXT, --Orginal Type <class 'str'>
                    loyalty INTEGER, --Orginal Type <class 'NoneType'>
                    multiverse_id TEXT, --Orginal Type <class 'NoneType'>
                    variations TEXT, --Orginal Type <class 'NoneType'> I think this will be a comma seperated list of values
                    watermark TEXT, --Orginal Type <class 'NoneType'> I have no idea what this is
                    border TEXT, --Orginal Type <class 'NoneType'>
                    timeshifted TEXT, --Orginal Type <class 'NoneType'>
                    hand TEXT, --Orginal Type <class 'NoneType'>
                    life TEXT, --Orginal Type <class 'NoneType'>
                    release_date TEXT, --Orginal Type <class 'str'>
                    starter TEXT, --Orginal Type <class 'NoneType'>
                    printings TEXT, --Orginal Type <class 'list'>
                    original_text TEXT, --Orginal Type <class 'NoneType'>
                    original_type TEXT, --Orginal Type <class 'NoneType'>
                    "source" TEXT, --Orginal Type <class 'str'>
                    image_url TEXT, --Orginal Type <class 'NoneType'>
                    "set" TEXT, --Orginal Type <class 'str'>
                    set_name TEXT, --Orginal Type <class 'str'>
                    id TEXT PRIMARY KEY, --Orginal Type <class 'str'>
                    legalities TEXT, --Orginal Type <class 'list'>
                    rulings TEXT, --Orginal Type <class 'list'> This will have to be a JSON type of {'rulings' : []}
                    foreign_names TEXT, --Orginal Type <class 'list'> This will have to be a JSON type of {'foreign_name' : []}
                    )

CREATE TABLE collection
                    (FOREIGN KEY id REFERENCES mtgcards(id),
                    PRIMARY KEY(id),
                    quanity INTEGER,
                    )
*/

CREATE TABLE mtgcards
                (
                "id" TEXT PRIMARY KEY, --A hash being sha1(card_name, set_name, multiverse_id, collectors_number)
                "multiverse_id" INTEGER,
                "collectors_number" TEXT,
                "name" TEXT,
                FOREIGN KEY set_code REFERENCES mtgsets("code"),
                "color" TEXT,
                "mana_cost" TEXT,
                "cmc" REAL,
                "rarity" TEXT,
                "power" TEXT,
                "toughness" TEXT,
                "loyalty" TEXT,
                "flavor_text" TEXT,
                "type_line" TEXT,
                "oracle_text" TEXT,
                "artist" TEXT,
                "layout" TEXT,
                "types" TEXT,
                "subtypes" TEXT,
                "supertypes" TEXT,
                "foreign_names" TEXT,
                "rulings" TEXT,
                "legalities" TEXT,
                "image_url" TEXT,
                "language" TEXT,
                "game_format" TEXT
                )

CREATE TABLE mtgsets
                (
                "code" TEXT PRIMARY KEY,
                "name" TEXT,
                "block" TEXT,
                "gatherer_code" TEXT,
                "release_date" TEXT,
                "expansion" TEXT,
                "booster" TEXT
                )

CREATE TABLE collection
                (
                "id" TEXT PRIMARY KEY,
                FOREIGN KEY("id") REFERENCES mtgcards("id"),
                "count" INTEGER
                )

CREATE TABLE deck
                (
                "id" TEXT PRIMARY KEY,
                FOREIGN KEY("id") REFERENCES mtgcards("id"),
                "count" INTEGER,
                "board" BOOLEAN
                )
