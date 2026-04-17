# Each document is a dict with "text" (the content to embed) and "metadata" (structured source info).
# ChromaDB metadata values must be flat scalar types: str, int, float, or bool.

exampleSourceDocuments = [

    # --- Sailing Instructions (manage2sail) ---

    {
        "text": (
            "SPECIAL RULE — NO-TACK ZONE: The 'Obsidian Reach' channel is designated a 'No-Tack Zone' "
            "for the duration of the 2026 Emerald Bay Championship. Boats found tacking within the channel "
            "markers will receive a 20% scoring penalty. This restriction applies from the northern green "
            "marker (OB-N1) to the southern red marker (OB-S1)."
        ),
        "metadata": {
            "source_type": "sailing_instructions",
            "source_title": "2026 Emerald Bay Championship — Sailing Instructions",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/si#rule-14-2",
            "section": "Rule 14.2 — No-Tack Zone",
            "published_by": "Race Committee",
            "published_date": "2026-05-01",
        },
    },
    {
        "text": (
            "COURSE UPDATE: The traditional 'Buoy Alpha' mark has been permanently replaced for this "
            "event by a floating solar-powered navigation barge named 'Sun-Ray 1'. Sun-Ray 1 is anchored "
            "at position 34°12.4'N, 119°45.7'W. All competitors must leave Sun-Ray 1 to starboard on "
            "all windward legs."
        ),
        "metadata": {
            "source_type": "sailing_instructions",
            "source_title": "2026 Emerald Bay Championship — Sailing Instructions",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/si#appendix-a-courses",
            "section": "Appendix A — Course Descriptions",
            "published_by": "Race Committee",
            "published_date": "2026-05-01",
        },
    },
    {
        "text": (
            "SCORING SYSTEM: The 2026 Regatta uses the 'Low-Point-Plus' scoring system. "
            "A first-place finish earns 0.7 points (instead of the standard 1.0) to reward dominant "
            "performance. All other finishing positions are scored as per the standard Low Point system. "
            "A boat's series score is the total of all her race scores."
        ),
        "metadata": {
            "source_type": "sailing_instructions",
            "source_title": "2026 Emerald Bay Championship — Sailing Instructions",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/si#scoring",
            "section": "Section 10 — Scoring",
            "published_by": "Race Committee",
            "published_date": "2026-05-01",
        },
    },
    {
        "text": (
            "CREW REQUIREMENTS — MASTERS DIVISION: All boats competing in the 'Masters' division must "
            "carry at least one crew member over the age of 65 and at least one crew member under the "
            "age of 18 at the time of the first race. This rule is intended to promote intergenerational "
            "mentorship within the sport. Supporting documentation (birth certificates or passports) must "
            "be presented at registration."
        ),
        "metadata": {
            "source_type": "sailing_instructions",
            "source_title": "2026 Emerald Bay Championship — Sailing Instructions",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/si#eligibility",
            "section": "Section 4 — Eligibility & Crew",
            "published_by": "Race Committee",
            "published_date": "2026-05-01",
        },
    },
    {
        "text": (
            "FLAG SIGNALS: A unique 'checkered purple flag' displayed on the Committee Boat signifies an "
            "immediate race suspension due to a shark sighting in or near the course area. Upon sighting "
            "this signal, all boats must immediately stop racing and return directly to the Rusty Anchor "
            "Tavern marina. This signal takes precedence over all other flag signals."
        ),
        "metadata": {
            "source_type": "sailing_instructions",
            "source_title": "2026 Emerald Bay Championship — Sailing Instructions",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/si#flag-signals",
            "section": "Section 7 — Signals",
            "published_by": "Race Committee",
            "published_date": "2026-05-01",
        },
    },

    # --- Notices to Competitors (manage2sail) ---

    {
        "text": (
            "SAFETY NOTICE — WHISPERING REEF DEPTH: Due to significant sand migration recorded in early "
            "2026, the Whispering Reef shoal now has a minimum depth of only 1.2 metres at mean low water. "
            "This is approximately 0.5 metres shallower than the depth shown on current official Admiralty "
            "charts. All competitors with a keel draft exceeding 1.0 metres must avoid the area marked by "
            "the yellow exclusion buoys (WR-E1 through WR-E4)."
        ),
        "metadata": {
            "source_type": "notice_to_competitors",
            "source_title": "NTC #3 — Whispering Reef Depth Warning",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/ntc/ntc-003",
            "section": "NTC #3 — Issued 2026-05-28",
            "published_by": "Race Committee",
            "published_date": "2026-05-28",
        },
    },
    {
        "text": (
            "WEATHER PROTOCOL UPDATE: If sustained wind speeds exceed 28 knots at the Coastal Guard "
            "anemometer station, racing will be relocated to 'Sector 7' (The Sheltered Lagoon). "
            "If wind speeds drop below 4 knots for more than 20 consecutive minutes during a race, "
            "the race will be abandoned and a 'Paddle-Off' tiebreaker will be held at the docks "
            "to determine finishing positions for that race."
        ),
        "metadata": {
            "source_type": "notice_to_competitors",
            "source_title": "NTC #1 — Weather & Abandonment Protocol",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/ntc/ntc-001",
            "section": "NTC #1 — Issued 2026-04-20",
            "published_by": "Race Committee",
            "published_date": "2026-04-20",
        },
    },
    {
        "text": (
            "REGISTRATION CHANGE: The deadline for late entries has been extended from 2026-06-05 to "
            "2026-06-09 due to the public holiday on the original closing date. Late entry fees apply "
            "to all entries received after 2026-06-01. Please submit late entry forms via the manage2sail "
            "portal only — paper entries will not be accepted."
        ),
        "metadata": {
            "source_type": "notice_to_competitors",
            "source_title": "NTC #2 — Late Entry Deadline Extension",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2026/ntc/ntc-002",
            "section": "NTC #2 — Issued 2026-05-10",
            "published_by": "Organising Authority",
            "published_date": "2026-05-10",
        },
    },

    # --- Event Timetable / Information (event homepage) ---

    {
        "text": (
            "EVENT DATES & VENUE: The 2026 Emerald Bay Championship runs from June 12 to June 14, 2026. "
            "Racing takes place daily with the first warning signal scheduled for 10:00 local time. "
            "The Regatta Office is temporarily relocated to the 'Rusty Anchor Tavern' on Harbour Street "
            "due to ongoing pier renovations at the Yacht Club. Opening Ceremony: June 11 at 18:00."
        ),
        "metadata": {
            "source_type": "event_timetable",
            "source_title": "Emerald Bay Championship 2026 — Event Information & Timetable",
            "source_url": "https://emerald-bay-championship.example.com/2026/timetable",
            "section": "Race Schedule & Venue",
            "published_by": "Organising Authority",
            "published_date": "2026-03-15",
        },
    },
    {
        "text": (
            "PRIZE GIVING CEREMONY: The Prize Giving Ceremony will take place on June 14, 2026 at 17:30 "
            "in the Emerald Bay Yacht Club main hall. Trophy presentation will begin promptly at 18:00. "
            "All competitors are encouraged to attend in their class uniform. Dress code: smart casual. "
            "A dinner buffet will follow the prize giving. Tickets must be pre-purchased via the event website."
        ),
        "metadata": {
            "source_type": "event_timetable",
            "source_title": "Emerald Bay Championship 2026 — Event Information & Timetable",
            "source_url": "https://emerald-bay-championship.example.com/2026/timetable#prize-giving",
            "section": "Prize Giving & Social Events",
            "published_by": "Organising Authority",
            "published_date": "2026-03-15",
        },
    },

    # --- Race Results (manage2sail) ---

    {
        "text": (
            "2025 PODIUM RESULTS: The 2025 Emerald Bay Championship concluded with the following overall "
            "results. First place: yacht 'Silver Wake', skippered by Captain Elias Thorne (total: 6.7 pts). "
            "Second place: 'Blue Mist', helmed by Sarah Chen (total: 9.0 pts). "
            "Third place: 'Wind-Dancer', helmed by Markus Vane (total: 11.5 pts)."
        ),
        "metadata": {
            "source_type": "race_results",
            "source_title": "2025 Emerald Bay Championship — Final Results",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2025/results/overall",
            "section": "Overall Series Results",
            "published_by": "Race Committee",
            "published_date": "2025-06-16",
        },
    },
    {
        "text": (
            "DISQUALIFICATION RECORD: In the 2025 Emerald Bay Championship, the yacht 'Storm-Petrel' "
            "(skipper: R. Hollis) was disqualified from the entire series following a Protest Committee "
            "hearing. The grounds for disqualification were the use of an unauthorized experimental "
            "hydrofoil keel system in the 'No-Lift' division, which violated Equipment Rule 22.4. "
            "The disqualification stands in the official record."
        ),
        "metadata": {
            "source_type": "protest_decision",
            "source_title": "2025 Emerald Bay Championship — Protest Committee Decision PC-2025-07",
            "source_url": "https://manage2sail.com/en/event/emeraldbay2025/protests/pc-2025-07",
            "section": "Decision PC-2025-07 — Equipment Violation",
            "published_by": "Protest Committee",
            "published_date": "2025-06-15",
        },
    },
]
