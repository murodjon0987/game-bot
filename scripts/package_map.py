"""
O'yin nomi -> Haqiqiy Android package name xaritasi
APKPure CDN: https://d.apkpure.net/b/APK/{packageName}?version=latest
"""

PACKAGE_NAME_MAP = {
    # VIP/MOD O'yinlar (asl o'yin packageName lari)
    "car parking": "com.olzhsoft.market",
    "null's brawl": "com.supercell.brawlstars",
    "null's clash": "com.supercell.clashofclans",
    "gta san andreas": "com.rockstar.gtasa",
    "shadow fight 2": "com.nekki.shadowfight2",
    "subway surfers": "com.kiloo.subwaysurf",
    "traffic rider": "com.skgames.trafficrider",
    "hill climb racing": "com.fingersoft.hillclimb2",
    "score! hero": "com.firsttouchgames.sfa",
    "8 ball pool": "com.miniclip.eightballpool",
    "dead target": "com.vng.deadtarget2",
    "sniper 3d": "com.fungames.sniper3dassault",
    "mini militia": "com.appsomniacs.da2",
    "earn to die": "com.notdoppler.earntodie2",
    "zombie catchers": "com.deca.zombiecatchers",
    "swamp attack": "com.candywriter.swampattack",
    "hungry shark world": "com.future.games.sharkworld.android",
    "bowmasters": "com.playgendary.bowmasters",
    "fruit ninja": "com.halfbrick.fruitninja",
    "plants vs zombies": "com.ea.game.pvzfree_row",
    "dude theft wars": "com.hzmark.sandbox",
    "stickman warriors": "com.xichengqichegame.stickmanwarriors",
    "payback 2": "au.com.halfbrick.jetpackjoyride",
    "kick the buddy": "com.playtend.kickthebuddyforever",
    "dr. driving": "com.sss.dr",

    # Action
    "pubg mobile": "com.tencent.iglite",
    "free fire": "com.dts.freefiremax",
    "standoff 2": "com.axlebolt.standoff2",
    "special forces group": "com.ForceContact.Force2",
    "call of duty": "com.activision.callofduty.shooter",
    "modern strike": "com.gamedevltd.modernstrike",
    "cover fire": "com.generagames.coverfire",
    "hitman sniper": "com.squareenixmontreal.hitmansniperas",
    "six-guns": "com.gameloft.android.ANMP.GloftSIHM",
    "into the dead": "com.pikpok.intothe dead2",
    "mortal kombat": "com.wb.goog.mkx",
    "injustice 2": "com.wb.goog.injustice2",
    "gangstar vegas": "com.gameloft.android.ANMP.GloftGCHM",
    "soul knight": "com.ChillyRoom.MowSky",
    "magic rampage": "com.batterystaple.games.MagicRampage",

    # Racing
    "asphalt 9": "com.gameloft.android.ANMP.GloftA9HM",
    "carx drift": "com.carxtech.carxdriftracingracing2",
    "carx street": "com.carxtech.sr",
    "need for speed": "com.ea.game.nfs14_row",
    "real racing": "com.ea.games.r3_row",
    "rush rally": "com.RogerGoode.RushRally3",
    "rebel racing": "com.hutch.rebel",
    "pixel car racer": "com.tuganstudio.pixelcarracer",
    "madout2": "com.alexplay.madout2",
    "trial xtreme": "com.deemedya.trialxtreme4",
    "truck simulator ultimate": "com.zuuks.truck.simulator.ultimate",
    "bus simulator ultimate": "com.zuuks.bus.simulator.ultimate",
    "farming simulator": "com.giants.software.farm.simulator.23",
    "flight pilot": "com.fungames.flightpilot",

    # Simulator
    "simcity": "com.ea.game.simcitymobile_row",
    "car saler simulator": "com.xtornament.car.saler.simulator",

    # Sport
    "dream league soccer": "com.firsttouchgames.dls5",
    "ea sports fc": "com.ea.gp.fifamobile",
    "efootball": "com.konami.pesam",
    "head ball": "com.masomo.headball2",
    "real steel": "com.disney.realsteelwrb_goo",
    "wwe mayhem": "com.reliance.jio.wwe",
    "nba live": "com.ea.game.nbas2014_row",

    # Puzzle
    "monument valley": "com.ustwo.monumentvalley2",
    "the room": "com.FireproofStudios.TheRoom4",
    "limbo": "com.playdead.limbo",
    "cut the rope": "com.zeptolab.ctr.free",
    "bad piggies": "com.rovio.BadPiggiesHD",
    "brain out": "com.mind.quiz.tricky.puzzle.masteriq",
    "2048": "com.androbaby.game2048",

    # Adventure
    "minecraft": "com.mojang.minecraftpe",
    "terraria": "com.and.games505.TerrariaPaid",
    "roblox": "com.roblox.client",
    "temple run": "com.imangi.templerun2",
    "vector": "com.nekki.vector",
    "swordigo": "com.chillingo.swordigo.android.google",
    "alto's odyssey": "com.noodlecake.altosodyssey",

    # Retro
    "super mario": "com.nintendo.zara",
    "sonic dash": "com.sega.sonicdash",
    "contra": "com.ktplay.contrareturnsglobal",
    "doodle jump": "com.lima.doodlejump",
    "pac-man": "com.bandainamcoent.pacmanparty",
    "1945 air force": "net.onesoft.ww2.airforce.shooting.games.army.plane",

    # Apps - Video/Photo
    "capcut": "com.lemon.lvoverseas",
    "inshot": "com.camerasideas.instashot",
    "kinemaster": "com.nexstreaming.app.kinemasterfree",
    "alight motion": "com.alightcreative.motion",
    "filmora": "com.wondershare.filmorago",
    "vn video editor": "com.vlognow.editor",
    "lightroom": "com.adobe.lrmobile",
    "snapseed": "com.niksoftware.snapseed",

    # Apps - Media
    "spotify": "com.spotify.music",
    "youtube vanced": "app.revanced.android.youtube",
    "soundcloud": "com.soundcloud.android",
    "boom music": "com.globaldelight.music.android",
    "poweramp": "com.maxmpz.audioplayer",

    # Apps - VPN
    "vpn super": "com.secure.vpnsuper",
    "hide.me vpn": "hideme.vpn.android",
    "nordvpn": "com.nordvpn.android",
    "express vpn": "com.expressvpn.vpn",
    "proton vpn": "ch.protonvpn.android",

    # Apps - Tools
    "wps office": "cn.wps.moffice_eng",
    "microsoft word": "com.microsoft.office.word",
    "google docs": "com.google.android.apps.docs.editors.docs",
    "duolingo": "com.duolingo",
    "busuu": "com.busuu.android.enc",
    "chatgpt": "com.openai.chatgpt",
    "character ai": "ai.character.app",
}

def get_package_name(game_title: str) -> str:
    """O'yin nomiga mos keladigan Android package name ni qaytaradi"""
    title_lower = game_title.lower()
    for key, pkg in PACKAGE_NAME_MAP.items():
        if key.lower() in title_lower:
            return pkg
    # Default: Subway Surfers
    return "com.kiloo.subwaysurf"


def get_apkpure_cdn_url(package_name: str) -> str:
    """APKPure CDN direct download URL ni qaytaradi"""
    return f"https://d.apkpure.net/b/APK/{package_name}?version=latest"
