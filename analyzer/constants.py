"""Static configuration: domain blacklists and the heuristic trigger lexicon.

Kept in their own module so they can be reviewed, audited, and extended
without touching the runtime engine. All collections are immutable
(``frozenset`` / ``tuple``) to make accidental mutation impossible.
"""

from __future__ import annotations

SATIRE_BLACKLIST: frozenset[str] = frozenset({
    "clickhole.com",
    "der-postillon.com",
    "legorafi.fr",
    "theonion.com",
    "theunrealtimes.com",
})

RESTRICTED_BLACKLIST: frozenset[str] = frozenset({
    "21stcenturywire.com", "abcnews.com.co", "abeldanger.net", "abovetopsecret.com",
    "activistpost.com", "adobochronicles.com", "ahtribune.com", "allnewspipeline.com",
    "americannews.com", "americasfreedomfighters.com", "amren.com", "amtvmedia.com",
    "awdnews.com", "barenakedislam.com", "coasttocoastam.com", "corbettreport.com",
    "countercurrents.org", "counterpunch.org", "darkmoon.me", "davidduke.com",
    "davidstockmanscontracorner.com", "davidwolfe.com", "dcclothesline.com",
    "defenddemocracy.press", "dennismichaellynch.com", "departed.co",
    "fromthetrenchesworldreport.com", "frontpagemag.com", "galacticconnection.com",
    "globalresearch.ca", "infowars.com", "intrepidreport.com", "madworldnews.com",
    "naturalnews.com", "newstarget.com", "presstv.ir", "prisonplanet.com",
    "projectveritas.com", "returnofkings.com", "shiftfrequency.com", "thedailysheeple.com",
    "theeconomiccollapseblog.com", "thefreethoughtproject.com", "themindunleashed.com",
    "thepeoplescube.com", "therussophile.org", "thesaker.is", "thetruthseeker.co.uk",
    "topinfopost.com", "veteranstoday.com", "voltairenet.org", "washingtonsblog.com",
    "westernjournalism.com", "whatreallyhappened.com",
})

RUSSIAN_STATE_MEDIA_BLACKLIST: frozenset[str] = frozenset({
    ".ru/", "rt.com", "sputniknews.com", "tass.com", "rbth.com",
})

TRIGGER_PHRASES: tuple[str, ...] = (
    "guaranteed returns", "double your money", "risk-free investment", "crypto giveaway",
    "send to this wallet", "get rich quick", "secret wealth system", "banks hate this",
    "hidden loophole", "financial elite", "make thousands overnight", "passive income secret",
    "pump and dump", "unlimited cash", "secret algorithm", "earn from home guaranteed",
    "bitcoin doubler", "elon musk giveaway", "secret bank account", "tax free millions",
    "cash app hack", "venmo glitch", "zero risk trading", "insider trading secret",
    "miracle cure", "doctors don't want you to know", "secret remedy", "big pharma hiding",
    "instant weight loss", "melt fat overnight", "reverse aging instantly", "cure cancer naturally",
    "suppressed medical truth", "magical healing", "detox your liver in hours", "100% natural cure",
    "banned supplement", "fountain of youth", "secret ancient remedy", "parasite cleanse",
    "vaccine microchip", "dna altering", "shed pounds instantly", "the cure they are hiding",
    "disease free forever", "miracle pill", "health industry secret", "forbidden cure",
    "shocking truth", "you won't believe", "what happened next", "they don't want you to know",
    "secret exposed", "banned video", "act now", "before it's deleted", "truth revealed",
    "mind-blowing", "viral secret", "leaked document", "the media is hiding", "absolute proof",
    "destroying the internet", "this will make you cry", "everyone is wrong about", "hidden camera",
    "the ultimate secret", "don't ignore this", "warning to all", "emergency broadcast",
    "share immediately", "censored by big tech", "the real reason why", "what they aren't telling you",
    "deep state", "illuminati", "new world order", "lizard people", "fake moon landing",
    "flat earth proof", "mind control waves", "secret bunker", "chemtrail poison", "global elite",
    "shadow government", "staged event", "crisis actors", "false flag operation", "secret society",
    "5g mind control", "population control agenda", "the great reset", "sheeple", "wake up america",
    "secret alien pact", "hidden history", "the matrix is real", "simulation theory proof",
    "reptilian overlords", "secret pedo ring", "hollywood elites", "cloned politicians",
    "rigged election", "stolen votes", "dead people voted", "voting machine hacked",
    "fake ballots found", "election interference proof", "destroying democracy", "illegal voters",
    "ballot dumping", "secret vote count", "whistleblower exposes election", "election fraud caught",
    "destroying our country", "the radical agenda", "brainwashing our children", "secret marxist plot",
    "they are coming for your", "banning the bible", "mandatory microchips", "cashless society trap",
    "social credit score coming", "forced quarantine camps", "the end of freedom", "martial law imminent",
    "click here to claim", "congratulations you won", "claim your prize", "urgent account update",
    "password compromised click link", "your package is delayed click", "gift card generator",
)
