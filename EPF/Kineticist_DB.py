Kineticist_DB = {
    "elemental blast (air)": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Air) - Electricity",
            "lvl": 1,
            "traits": ["air", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d6 electricity"},
            "heighten": {"interval": 4, "effect": "1d6 electricity"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Air) - Slashing",
            "lvl": 1,
            "traits": ["air", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d6 slashing"},
            "heighten": {"interval": 4, "effect": "1d6 slashing"},
        },
    ],
    "elemental blast (earth)": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Earth) Piercing",
            "lvl": 1,
            "traits": ["earth", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 piercing"},
            "heighten": {"interval": 4, "effect": "1d8 piercing"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Earth) Bludgeoning",
            "lvl": 1,
            "traits": ["earth", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 bludgeoning"},
            "heighten": {"interval": 4, "effect": "1d8 bludgeoning"},
        },
    ],
    "elemental blast (fire)": {
        "complex": True,
        "category": "kineticist",
        "title": "Elemental Blast (Fire)",
        "lvl": 1,
        "traits": ["fire", "impulse", "kineticist", "primal", "attack"],
        "type": {"value": "attack"},
        "effect": {"success": "1d6 fire"},
        "heighten": {"interval": 4, "effect": "1d6 fire"},
    },
    "elemental blast (metal)": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Metal) Piercing",
            "lvl": 1,
            "traits": ["metal", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 piercing"},
            "heighten": {"interval": 4, "effect": "1d8 piercing"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Metal) Slashing",
            "lvl": 1,
            "traits": ["metal", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 slashing"},
            "heighten": {"interval": 4, "effect": "1d8 slashing"},
        },
    ],
    "elemental blast (water)": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Water) Bludgeoning",
            "lvl": 1,
            "traits": ["water", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 bludgeoning"},
            "heighten": {"interval": 4, "effect": "1d8 bludgeoning"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Water) Cold",
            "lvl": 1,
            "traits": ["water", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 cold"},
            "heighten": {"interval": 4, "effect": "1d8 cold"},
        },
    ],
    "elemental blast (wood)": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Wood) Bludgeoning",
            "lvl": 1,
            "traits": ["wood", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 bludgeoning"},
            "heighten": {"interval": 4, "effect": "1d8 bludgeoning"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Elemental Blast (Wood) Vitality",
            "lvl": 1,
            "traits": ["wood", "impulse", "kineticist", "primal", "attack"],
            "type": {"value": "attack"},
            "effect": {"success": "1d8 vitality"},
            "heighten": {"interval": 4, "effect": "1d8 vitality"},
        },
    ],
    "aerial boomerang": {
        "complex": True,
        "category": "kineticist",
        "title": "Aerial Boomerang",
        "lvl": 1,
        "traits": ["air", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "2d4 slashing"},
        "heighten": {"interval": 2, "effect": "1d4 slashing"},
    },
    "flying flame": {
        "complex": True,
        "category": "kineticist",
        "title": "Flying Flame",
        "lvl": 1,
        "traits": ["fire", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "1d6 fire"},
        "heighten": {"interval": 2, "effect": "1d6 fire"},
    },
    "hail of splinters": {
        "complex": True,
        "category": "kineticist",
        "title": "Hail of Splinters",
        "lvl": 1,
        "traits": ["overflow", "impulse", "kineticist", "primal", "wood"],
        "type": {"value": "save", "save": "reflex", "type": "complex"},
        "effect": {
            "critical success": "",
            "success": "1d4 piercing, pd 1d4 bleed / dc15 flat",
            "failure": "1d4 piercing, pd 1d4 bleed / dc15 flat",
            "critical failure": "1d4 piercing, pd 1d4 bleed / dc15 flat ",
        },
        "heighten": {"interval": 2, "effect": "1d4 piercing, hpd 1d4 bleed"},
    },
    "magnetic pinions": {
        "complex": True,
        "category": "kineticist",
        "title": "Magnetic Pinions",
        "lvl": 1,
        "traits": ["overflow", "impulse", "kineticist", "primal", "metal"],
        "type": {
            "value": "attack",
        },
        "effect": {"success": "1d4 piercing, 1d4 bludgeoning"},
        "heighten": {"interval": 2, "effect": "1d4 piercing, 1d4 bludgeoning"},
    },
    "scorching column": {
        "complex": True,
        "category": "kineticist",
        "title": "Scorching Column",
        "lvl": 1,
        "traits": ["fire", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "1d6 fire"},
        "heighten": {"interval": 3, "effect": "1d6 fire"},
    },
    "shard strike": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Shard Strike (Shards)",
            "lvl": 1,
            "traits": ["impulse", "kineticist", "primal", "metal"],
            "type": {"value": "save", "save": "reflex", "type": "basic"},
            "effect": {
                "failure": "1d6 slashing",
                "critical failure": "1d6 piercing, pd 1d6 bleed / dc15 flat ",
            },
            "heighten": {"interval": 2, "effect": "1d6 piercing"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Shard Strike (Spines)",
            "lvl": 1,
            "traits": ["impulse", "kineticist", "primal", "metal"],
            "type": {"value": "save", "save": "reflex", "type": "basic"},
            "effect": {
                "failure": "1d6 slashing",
                "critical failure": "1d6 slashing, clumsy 1 auto duration: 1 flex myturn",
            },
            "heighten": {"interval": 2, "effect": "1d6 slashing"},
        },
    ],
    "tidal hands": {
        "complex": True,
        "category": "kineticist",
        "title": "Tidal Hands",
        "lvl": 1,
        "traits": ["water", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "1d8 bludgeoning"},
        "heighten": {"interval": 2, "effect": "1d8 bludgeoning"},
    },
    "tremor": {
        "complex": True,
        "category": "kineticist",
        "title": "Tremor",
        "lvl": 1,
        "traits": ["earth", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {"failure": "1d8 bludgeoning", "critical failure": "1d8 bludgeoning, prone"},
        "heighten": {"interval": 2, "effect": "1d10 bludgeoning"},
    },
    "winter's clutch": {
        "complex": True,
        "category": "kineticist",
        "title": "Winter's Clutch",
        "lvl": 1,
        "traits": ["cold", "impulse", "kineticist", "primal", "water"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "2d4 cold"},
        "heighten": {"interval": 2, "effect": "1d4 cold"},
    },
    # Level 4
    "blazing wave": {
        "complex": True,
        "category": "kineticist",
        "title": "Blazing Wave",
        "lvl": 4,
        "traits": ["fire", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {"failure": "4d6 fire", "critical failure": "4d6 fire, prone"},
        "heighten": {"interval": 2, "effect": "1d6 fire"},
    },
    "lava leap": {
        "complex": True,
        "category": "kineticist",
        "title": "Lava Leap",
        "lvl": 4,
        "traits": ["fire", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "1d6 bludgeoning, 2d6 fire, Shielded 2 duration: 1 unit: round auto flex self data 'ac +2 c'",
        },
        "heighten": {"interval": 3, "effect": "1d6 bludgeoning, 1d6 fire"},
    },
    "lightning dash": {
        "complex": True,
        "category": "kineticist",
        "title": "Lightning Dash",
        "lvl": 4,
        "traits": ["air", "electricity", "impulse", "kineticist", "primal", "overflow", "move", "polymorph"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "2d12 electricity",
        },
        "heighten": {"interval": 3, "effect": "1d12 electricity"},
    },
    "rain of rust": {
        "complex": True,
        "category": "kineticist",
        "title": "Rain of Rust",
        "lvl": 4,
        "traits": ["metal", "water", "impulse", "kineticist", "primal", "composite"],
        "type": {"value": "save", "save": "fort", "type": "complex"},
        "effect": {
            "failure": "3d6 untyped, pd 1d6 untyped / dc15 flat, clumsy 1",
        },
        "heighten": {"interval": 2, "effect": "1d6 untyped"},
    },
    # Prototype Utility Skill
    "thermal nimbus": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Thermal Nimbus (Fire)",
            "lvl": 4,
            "traits": ["fire", "stance", "impulse", "kineticist", "primal"],
            "type": {"value": "utility"},
            "effect": {
                "success": "aura 0 data: 'fire r _lvl_'",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Thermal Nimbus (Cold)",
            "lvl": 4,
            "traits": ["fire", "stance", "impulse", "kineticist", "primal"],
            "type": {"value": "utility"},
            "effect": {
                "success": "aura 0 data: 'cold r _lvl_'",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
    ],
    "whirling grindstone": {
        "complex": True,
        "category": "kineticist",
        "title": "Whirling Grindstone",
        "lvl": 4,
        "traits": ["attack", "composite", "earth", "metal", "impulse", "kineticist", "primal"],
        "type": {"value": "attack"},
        "effect": {
            "success": "2d6 slashing, 1d6 fire",
        },
        "heighten": {"interval": 5, "effect": "1d6 slashing, 1d6 fire"},
    },
    # Level 6
    "ash strider": {
        "complex": True,
        "category": "kineticist",
        "title": "Ash Strider",
        "lvl": 6,
        "traits": ["air", "fire", "composite", "impulse", "kineticist", "primal", "overflow", "polymorph"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "3d6 fire, concealed 1 duration: 1 unit: round auto flex self",
        },
        "heighten": {"interval": 2, "effect": "1d6 fire"},
    },
    "driving rain": {
        "complex": True,
        "category": "kineticist",
        "title": "Driving Rain",
        "lvl": 6,
        "traits": ["water", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "3d8 bludgeoning",
        },
        "heighten": {"interval": 2, "effect": "1d8 bludgeoning"},
    },
    "elemental artillery": {
        "complex": True,
        "category": "kineticist",
        "title": "Elemental Artillery",
        "lvl": 6,
        "traits": ["composite", "wood", "metal", "impulse", "kineticist", "primal"],
        "type": {"value": "attack"},
        "effect": {
            "success": "3d12 piercing",
        },
        "heighten": {"interval": 3, "effect": "1d12 piercing"},
    },
    "lightning rod": {
        "complex": True,
        "category": "kineticist",
        "title": "Lightning Rod (Lightning)",
        "lvl": 6,
        "traits": ["air", "metal", "composite", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "1d12 electricity",
        },
        "heighten": {"interval": 6, "effect": "1d12 electricity"},
    },
    "molten wire": {
        "complex": True,
        "category": "kineticist",
        "title": "Molten Wire",
        "lvl": 6,
        "traits": ["composite", "fire", "metal", "impulse", "kineticist", "primal"],
        "type": {"value": "attack"},
        "effect": {
            "success": "2d6 slashing, clumsy 1 duration: 1 unit: minute auto, pd 2d4 fire / dcdc reflex ",
        },
        "heighten": {"interval": 4, "effect": "1d6 slashing, hpd 1d4 fire"},
    },
    "rising hurricane": {
        "complex": True,
        "category": "kineticist",
        "title": "Rising Hurricane",
        "lvl": 6,
        "traits": ["air", "water", "composite", "impulse", "kineticist", "primal", "overflow"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "2d6 bludgeoning",
        },
        "heighten": {"interval": 3, "effect": "1d6 bludgeoning"},
    },
    "roiling mudslide": {
        "complex": True,
        "category": "kineticist",
        "title": "Roiling Mudslide",
        "lvl": 6,
        "traits": ["earth", "water", "composite", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "2d8 bludgeoning",
        },
        "heighten": {"interval": 4, "effect": "1d8 bludgeoning"},
    },
    "steam knight": {
        "complex": True,
        "category": "kineticist",
        "title": "Steam Knight (Steam Aura)",
        "lvl": 6,
        "traits": ["fire", "water", "composite", "stance", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "2d6 fire",
        },
        "heighten": {"interval": 5, "effect": "1d6 fire"},
    },
    "volcanic escape": {
        "complex": True,
        "category": "kineticist",
        "title": "Volcanic Escape",
        "lvl": 6,
        "traits": ["fire", "kineticist", "primal", "impulse", "overflow"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "1d6 fire",
        },
        "heighten": {"interval": 4, "effect": "1d6 fire"},
    },
    "weight of stone": {
        "complex": True,
        "category": "kineticist",
        "title": "weight of stone",
        "lvl": 6,
        "traits": ["earth", "overflow", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "4d8 bludgeoning",
        },
        "heighten": {"interval": 2, "effect": "1d8 bludgeoning"},
    },
    # Level 8
    "call the hurricane": {
        "complex": True,
        "category": "kineticist",
        "title": "Call the Hurricane",
        "lvl": 8,
        "traits": ["water", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "6d8 bludgeoning",
        },
        "heighten": {"interval": 2, "effect": "1d8 bludgeoning"},
    },
    "conductive sphere": {
        "complex": True,
        "category": "kineticist",
        "title": "Conductive Sphere (Sphere)",
        "lvl": 8,
        "traits": ["metal", "electricity", "impulse", "manipulate", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "1d12 electricity",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "drifting pollen": {
        "complex": True,
        "category": "kineticist",
        "title": "Drifting Pollen (Aura)",
        "lvl": 8,
        "traits": ["plant", "wood", "impulse", "stance", "kineticist", "primal"],
        "type": {"value": "save", "save": "fort", "type": "complex"},
        "effect": {
            "failure": "sickened 1, dazzled 0",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "retch rust": {
        "complex": True,
        "category": "kineticist",
        "title": "Retch Rust",
        "lvl": 8,
        "traits": ["metal", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "4d10 slashing",
        },
        "heighten": {"interval": 2, "effect": "1d10 slashing"},
    },
    "sanguivolent roots": {
        "complex": True,
        "category": "kineticist",
        "title": "Sanguivolent Roots",
        "lvl": 8,
        "traits": ["wood", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "3d6 piercing",
        },
        "heighten": {"interval": 2, "effect": "1d6 piercing"},
    },
    "solar detonation": {
        "complex": True,
        "category": "kineticist",
        "title": "Solar Detonation",
        "lvl": 8,
        "traits": ["fire", "impulse", "incapacitation", "overflow", "kineticist", "primal", "vitality"],
        "type": {"value": "save", "save": "reflex", "type": "complex"},
        "effect": {
            "success": "6d6 fire, dazzled 1 auto flex myturn",
            "failure": "6d6 fire, blinded 0  duration: 1 unit: Round, auto flex myturn",
            "critical failure": "6d6 fire, blinded 0 duration: 1 unit: Minute",
        },
        "heighten": {"interval": 2, "effect": "1d6 fire"},
    },
    "storm spiral": {
        "complex": True,
        "category": "kineticist",
        "title": "Storm Spiral",
        "lvl": 8,
        "traits": ["air", "electricity", "impulse", "overflow", "kineticist", "primal", "sonic"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "3d12 electricity, 1d10 sonic, deafened 1 unit: round auto",
            "critical failure": "3d12 electricity, 1d10 sonic, deafened 1 duration: 1 unit: minute auto",
        },
        "heighten": {"interval": 3, "effect": "1d12 electricity"},
    },
    # Level 12
    "rain of razors": {
        "complex": True,
        "category": "kineticist",
        "title": "Rain of Razors",
        "lvl": 12,
        "traits": ["metal", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "9d6 slashing",
        },
        "heighten": {"interval": 2, "effect": "1d6 slashing"},
    },
    "rattle the earth": {
        "complex": True,
        "category": "kineticist",
        "title": "Rattle the Earth",
        "lvl": 12,
        "traits": ["earth", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "11d6 bludgeoning, prone 0",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "wiles on the wind": {
        "complex": True,
        "category": "kineticist",
        "title": "Wiles on the Wind",
        "lvl": 12,
        "traits": ["air", "auditory", "illusion", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "will", "type": "complex"},
        "effect": {"failure": "fascinated 1 unit: round auto", "critical failure": "fascinated 1 unit: minute auto"},
        "heighten": {"interval": 20, "effect": ""},
    },
    "witchwood seed": {
        "complex": True,
        "category": "kineticist",
        "title": "Witchwood Seed",
        "lvl": 12,
        "traits": ["wood", "impulse", "overflow", "kineticist", "primal", "plant", "polymorph"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "5d10 piercing, clumsy 2 duration: 1 unit: round auto",
            "critical failure": "5d10 piercing, clumsy 2, immobilized 0",
        },
        "heighten": {"interval": 4, "effect": "1d10 piercing"},
    },
    # Level 14
    "walk through the conflagration": {
        "complex": True,
        "category": "kineticist",
        "title": "Walk Through the Conflagration",
        "lvl": 14,
        "traits": ["fire", "impulse", "overflow", "kineticist", "primal", "teleportation"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "4d6 fire",
        },
        "heighten": {"interval": 3, "effect": "1d6 fire"},
    },
    # Level 18
    "all shall end in flames": {
        "complex": True,
        "category": "kineticist",
        "title": "All Shall End in Flames",
        "lvl": 18,
        "traits": ["fire", "death", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "13d6 fire",
        },
        "heighten": {"interval": 2, "effect": "2d6 fire"},
    },
    "hell of 1,000,000 needles": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Hell of 1,000,000 Needles (Attack)",
            "lvl": 18,
            "traits": ["metal", "impulse", "overflow", "kineticist", "primal"],
            "type": {"value": "save", "save": "reflex", "type": "complex"},
            "effect": {
                "failure": "13d6 piercing, immobilized 0",
                "critical failure": "13d6 piercing, immobilized 0, off-guard 0",
            },
            "heighten": {"interval": 2, "effect": "4d6 piercing"},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Hell of 1,000,000 Needles (Sustain)",
            "lvl": 18,
            "traits": ["metal", "impulse", "overflow", "kineticist", "primal"],
            "type": {"value": "save", "save": "reflex", "type": "basic"},
            "effect": {
                "failure": "3d12 electricity",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
    ],
    "ignite the sun": {
        "complex": True,
        "category": "kineticist",
        "title": "Ignite the Sun",
        "lvl": 18,
        "traits": ["fire", "light", "impulse", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "7d6 fire",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "infinite expanse of bluest heaven": {
        "complex": True,
        "category": "kineticist",
        "title": "Infinite Expanse of Bluest Heaven",
        "lvl": 18,
        "traits": ["air", "illusion", "impulse", "mental", "overflow", "kineticist", "primal", "visual"],
        "type": {"value": "save", "save": "reflex", "type": "complex"},
        "effect": {
            "success": "off-guard 0",
            "failure": "off-guard 0, fleeing 0",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "ride the tsunami": {
        "complex": True,
        "category": "kineticist",
        "title": "Ride the Tsunami",
        "lvl": 18,
        "traits": ["water", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "reflex", "type": "basic"},
        "effect": {
            "failure": "10d10 bludgeoning",
        },
        "heighten": {"interval": 20, "effect": ""},
    },
    "the shattered mountain weeps": {
        "complex": True,
        "category": "kineticist",
        "title": "The Shattered Mountain Weeps",
        "lvl": 18,
        "traits": ["earth", "impulse", "overflow", "kineticist", "primal"],
        "type": {"value": "save", "save": "fort", "type": "basic"},
        "effect": {
            "failure": "9d10 bludgeoning, prone 0",
        },
        "heighten": {"interval": 2, "effect": "1d10 bludgeoning"},
    },
    "turn the wheel of seasons": [
        {
            "complex": True,
            "category": "kineticist",
            "title": "Turn the Wheel of Seasons (Summer)",
            "lvl": 18,
            "traits": ["wood", "light", "impulse", "overflow", "kineticist", "primal"],
            "type": {"value": "save", "save": "reflex", "type": "complex"},
            "effect": {
                "success": "dazed 1 unit: round auto flex myturn",
                "failure": "blinded 1 unit: round auto flex myturn",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Turn the Wheel of Seasons (Autum)",
            "lvl": 18,
            "traits": ["wood", "impulse", "overflow", "kineticist", "primal"],
            "type": {"value": "save", "save": "fort", "type": "complex"},
            "effect": {
                "failure": "slowed 1 unit: round auto flex myturn stable",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
        {
            "complex": True,
            "category": "kineticist",
            "title": "Turn the Wheel of Seasons (Winte)",
            "lvl": 18,
            "traits": ["wood", "impulse", "overflow", "kineticist", "primal"],
            "type": {"value": "save", "save": "reflex", "type": "complex"},
            "effect": {
                "success": "5d6 cold",
                "failure": "5d6 cold, pd 2d6 cold / dc15 flat",
            },
            "heighten": {"interval": 20, "effect": ""},
        },
    ],
}
