"""Photographs, historical context and cross-links for The Wall.
All photographs are public domain or openly licensed and are hosted in The Lake Norman Brief's media library."""
import re

IMG = 'https://i0.wp.com/lkn-law.com/wp-content/uploads/2026/11/%s?w=%d&ssl=1'
LKN = 'https://lkn-law.com'

# key: (file, caption, credit)
PHOTOS = {
 'wall-reflect': ('vietnam-wall-reflection-washington-monument.jpg', 'The Washington Monument reflected in the black granite of the Vietnam Veterans Memorial.', 'Antonio Zugaldia, CC BY 2.0, via Wikimedia Commons'),
 'wall-names': ('vietnam-wall-names-low-light-nps.jpg', 'Names etched into the granite of the Memorial, in the order of the dates on which they died.', 'National Park Service, CC BY 2.0, via Wikimedia Commons'),
 'wall-dod': ('vietnam-wall-washington-monument-dod.jpg', 'The Vietnam Veterans Memorial, dedicated on 13 November 1982, with the Washington Monument beyond.', 'Department of Defense, public domain'),
 'wall-flag': ('vietnam-wall-flag-points-to-name.jpg', 'A visitor uses a small flag to point to a name on the Wall, Memorial Day 2012.', 'Linda Hosek, Department of Defense, public domain'),
 'wall-trace': ('vietnam-wall-marine-traces-name-2025.jpg', 'A Marine traces a name on the Wall on National Vietnam War Veterans Day, 29 March 2025.', '3d U.S. Infantry Regiment (The Old Guard), public domain'),
 'wall-wreath': ('vietnam-wall-wreath-50th-anniversary-2025.jpg', 'A full-honors wreath-laying at the Wall for the 50th anniversary of the end of the war, 24 April 2025.', '3d U.S. Infantry Regiment (The Old Guard), public domain'),
 'wall-wide': ('vietnam-wall-rob-young-2011.jpg', 'The two black granite walls of the Memorial meet at a vertex 10.1 feet high.', 'Rob Young, CC BY 2.0, via Wikimedia Commons'),
 'three-soldiers': ('vietnam-three-soldiers-statue.jpg', 'Frederick Hart’s bronze “The Three Soldiers” (1984) looks toward the names.', 'ILoveCustard, CC BY-SA 3.0, via Wikimedia Commons'),
 'womens-memorial': ('vietnam-womens-memorial.jpg', 'Glenna Goodacre’s Vietnam Women’s Memorial, dedicated 11 November 1993.', 'Karen Cutter, CC BY-SA 4.0, via Wikimedia Commons'),
 'nc-memorial': ('vietnam-nc-vietnam-memorial-names.jpg', 'Visitors read the names at the North Carolina Vietnam Veterans Memorial Park.', 'Washuotaku, CC BY-SA 4.0, via Wikimedia Commons'),
 'pow-vigil': ('vietnam-seymour-johnson-pow-mia-vigil.jpg', 'An airman lights a candle during POW/MIA recognition week at Seymour Johnson Air Force Base, North Carolina.', 'A1C Aaron Jenne, U.S. Air Force, public domain'),
 'homecoming': ('vietnam-homecoming-pows-cheer-c141.jpg', 'Released prisoners of war cheer as their C-141 lifts off from Hanoi, February 1973.', 'U.S. Air Force, public domain'),
 'army-assault': ('vietnam-101st-airborne-jump-from-uh1d.jpg', 'Soldiers of the 101st Airborne Division leap from a UH-1D during an air assault.', 'SP4 Johnnie Jackson, U.S. Army, public domain'),
 'army-cav': ('vietnam-1-9-cavalry-combat-assault-1966.jpg', 'Troopers of the 1st Squadron, 9th Cavalry, 1st Cavalry Division, make a combat assault, December 1966.', 'SP5 Charles V. Hoover, U.S. Army, public domain'),
 'army-lz': ('vietnam-4th-infantry-landing-zone-1967.jpg', 'A soldier of the 4th Infantry Division secures a landing zone, October 1967.', 'SP5 Robert C. Lafoon, U.S. Army, public domain'),
 'army-jc': ('vietnam-junction-city-4-31-infantry-1967.jpg', 'Soldiers of the 196th Light Infantry Brigade wait for a UH-1D during Operation Junction City, 1967.', 'U.S. Army, public domain'),
 'army-173': ('vietnam-173rd-airborne-2-503-patrol-1970.jpg', 'Troopers of the 2nd Battalion, 503rd Infantry, 173rd Airborne Brigade, watch a UH-1D land, March 1970.', 'U.S. Army, public domain'),
 'army-dustoff': ('vietnam-57th-medical-detachment-dustoff.jpg', 'A 57th Medical Detachment crew loads a wounded soldier aboard a UH-1D “Dustoff” helicopter.', 'SP4 James B. Egan, U.S. Army, public domain'),
 'army-hueys': ('vietnam-1st-cav-hueys-coastline-chu-lai.jpg', 'UH-1 helicopters of the 1st Cavalry Division skim the coastline near Chu Lai, October 1967.', 'PFC Franklin G. Nickerson, U.S. Army, public domain'),
 'sf': ('vietnam-special-forces-cidg-m79-instruction.jpg', 'A 5th Special Forces Group sergeant teaches Civilian Irregular Defense Group trainees, March 1967.', 'SP5 Robert C. Lafoon, DASPO, U.S. Army, public domain'),
 'sf-camp': ('vietnam-plei-djereng-special-forces-camp.jpg', 'The gate of the Plei Djereng Special Forces camp in the Central Highlands, April 1970.', 'U.S. Army, public domain'),
 'iadrang': ('vietnam-ia-drang-1-7-cav-disembark-lz-xray.jpg', 'Troopers of the 1st Battalion, 7th Cavalry, leave a UH-1D at LZ X-Ray, Ia Đrăng, November 1965.', 'U.S. Army, public domain'),
 'dakto': ('vietnam-dak-to-173rd-foxholes-hill-875.jpg', 'Men of the 173rd Airborne Brigade dig foxholes on Hill 875 near Đắk Tô, 22 November 1967.', 'SSG Alfred Batungbacal, U.S. Army, public domain'),
 'khesanh': ('vietnam-khe-sanh-1-26-trenchline.jpg', 'The trench line of the 1st Battalion, 26th Marines at Khe Sanh, 1968.', 'Michael Braukus Collection, USMC Archives, CC BY 2.0'),
 'khesanh-air': ('vietnam-khe-sanh-f4-close-air-support.jpg', 'Marines at Khe Sanh watch an F-4 Phantom make a close air support run, March 1968.', 'Sgt. Robert F. Witowski, U.S. Army, public domain'),
 'hue': ('vietnam-hue-marines-mopping-up.jpg', 'Marines move through the streets of Huế near the end of the 26-day battle, February 1968.', 'USMC Archives, CC BY 2.0'),
 'hue-tank': ('vietnam-hue-marines-m48-tank-cover.jpg', 'Marines use an M48 tank as cover in the street fighting in Huế, 4 February 1968.', 'SSgt Jack L. Harlan, USMC, CC BY 2.0'),
 'hue-corpsman': ('vietnam-hue-corpsman-treats-marine.jpg', 'A Navy corpsman treats a wounded Marine of H Company, 2nd Battalion, 5th Marines, in Huế, February 1968.', 'Sgt. William F. Dickman, USMC, public domain'),
 'marines-danang': ('vietnam-da-nang-marines-bazooka-1965.jpg', 'Marines of the 9th Marine Expeditionary Brigade after landing at Đà Nẵng, March 1965.', 'U.S. Marine Corps, public domain'),
 'marines-starlite': ('vietnam-starlite-e-2-4-marines-lz.jpg', 'Marines of E Company, 2nd Battalion, 4th Marines, move out on the first day of Operation Starlite, 18 August 1965.', 'Sgt. Choate, USMC, public domain'),
 'marines-dewey': ('vietnam-dewey-canyon-uh1e-firebase-cunningham.jpg', 'Marine UH-1Es at Fire Support Base Cunningham during Operation Dewey Canyon, January 1969.', 'U.S. Marine Corps, public domain'),
 'navy-swift': ('vietnam-swift-boat-long-tau-river-1966.jpg', 'A Navy Swift boat patrols the Long Tàu River to keep the channel to Saigon open, December 1966.', 'PH1 V.H. McColley, U.S. Navy, public domain'),
 'navy-pbr': ('vietnam-pbr-river-patrol-boat-1966.jpg', 'A Navy river patrol boat (PBR) in the Mekong Delta, June 1966.', 'U.S. Navy, public domain'),
 'navy-riverine': ('vietnam-mobile-riverine-boats-ba-lai-river.jpg', 'Boats of the Mobile Riverine Force on the Ba Lai River in the Mekong Delta, April 1968.', 'SSG Alfred Batungbacal, U.S. Army, public domain'),
 'navy-carrier': ('vietnam-uss-enterprise-gulf-of-tonkin-1966.jpg', 'USS Enterprise on Yankee Station in the Gulf of Tonkin, May 1966.', 'U.S. Navy, public domain'),
 'navy-a4': ('vietnam-a4e-skyhawks-phuong-dinh-bridge.jpg', 'Navy A-4E Skyhawks from USS Oriskany attack a bridge in North Vietnam, September 1967.', 'LCdr. Jerry Breast, U.S. Navy, public domain'),
 'af-f105': ('vietnam-f105-thunderchiefs-refuel-kc135.jpg', 'F-105D Thunderchiefs refuel from a KC-135 on the way to North Vietnam, about 1966.', 'U.S. Air Force, public domain'),
 'af-skyraider': ('vietnam-a1e-skyraider-sunset-ca-mau.jpg', 'An A-1E Skyraider returns over the Cà Mau peninsula at sunset, about 1966.', 'U.S. Air Force, public domain'),
 'af-spooky': ('vietnam-ac47-spooky-tracers-night.jpg', 'An AC-47D “Spooky” gunship fires on a target at night over South Vietnam.', 'U.S. Air Force, public domain'),
 'af-b52': ('vietnam-b52ds-andersen-linebacker-ii.jpg', 'B-52Ds await takeoff at Andersen Air Force Base, Guam, December 1972.', 'U.S. Air Force, public domain'),
 'af-sa2': ('vietnam-f105-hit-by-sa2.jpg', 'An F-105D trails fire after being hit by an SA-2 missile over North Vietnam.', 'U.S. Air Force, public domain'),
 'trail': ('vietnam-ho-chi-minh-trail-bomb-craters.jpg', 'Bomb craters along the Ho Chi Minh Trail in Laos, August 1970.', 'U.S. Air Force, public domain'),
 'cambodia': ('vietnam-11th-acr-enters-snuol-cambodia.jpg', 'The 2nd Squadron, 11th Armored Cavalry Regiment, enters Snuol, Cambodia, 4 May 1970.', 'U.S. Army, public domain'),
 'cobra': ('vietnam-ah1g-cobra-1st-cav-katum-1970.jpg', 'A 1st Cavalry Division AH-1G Cobra comes in to refuel at Katum, May 1970.', 'SSgt. Harry G. Giffen, U.S. Army, public domain'),
 'easter': ('vietnam-kontum-mother-child-evacuated-1972.jpg', 'A mother and child are evacuated from Kon Tum to Pleiku during the Easter Offensive, 4 May 1972.', '1LT Stacy Stewart, U.S. Army, public domain'),
 'frequent-wind': ('vietnam-frequent-wind-last-marines-uss-okinawa.jpg', 'The last Marines of the U.S. Embassy security guard land aboard USS Okinawa, 30 April 1975.', 'GySgt Russ Thurman, USMC, public domain'),
 'tonkin': ('vietnam-tonkin-p4-boats-from-maddox.jpg', 'North Vietnamese torpedo boats photographed from USS Maddox, 2 August 1964.', 'U.S. Navy, public domain'),
 'apbac': ('vietnam-ap-bac-downed-helicopters-1963.jpg', 'U.S. Army helicopters downed at Ấp Bắc in the Mekong Delta, January 1963.', 'Richard Tregaskis Collection, USMC Archives, CC BY 2.0'),
 'advisers': ('vietnam-duc-my-ranger-training-allied-1965.jpg', 'Australian, American, South Vietnamese and Korean soldiers at the Đức Mỹ Ranger Training Center, December 1965.', 'SP5 Allan K. Holm, U.S. Army, public domain'),
 'cedar': ('vietnam-junction-city-ch47-resupply.jpg', 'A CH-47 Chinook lifts off on a resupply mission during Operation Junction City, April 1967.', 'SSG Howard C. Breedlove, U.S. Army, public domain'),
 'artillery': ('vietnam-175mm-gun-2-32-artillery.jpg', 'Gunners of the 2nd Battalion, 32nd Artillery prepare to fire a 175 mm gun.', 'SP5 Kevin Malone, U.S. Army, public domain'),
 'linebacker': ('vietnam-b52d-takeoff-u-tapao-linebacker-ii.jpg', 'B-52Ds take off from U-Tapao, Thailand, during Linebacker II, December 1972.', 'U.S. Air Force, public domain'),
 'hanoi-hilton': ('vietnam-hoa-lo-prison-gate-2013.jpg', 'The surviving gatehouse of Hỏa Lò prison, the “Hanoi Hilton,” in Hanoi.', 'Clay Gilliland, CC BY-SA 2.0, via Wikimedia Commons'),
}

def img(key, w=1600):
    return IMG % (PHOTOS[key][0], w)

CH = {
 1: ('Chapter 1: From Colony to War', LKN + '/2026/11/02/vietnam-french-indochina-war-dien-bien-phu/'),
 2: ('Chapter 2: Geneva and Two Vietnams, 1954–1963', LKN + '/2026/11/02/vietnam-geneva-two-vietnams-1954-1963/'),
 3: ('Chapter 3: The Gulf of Tonkin and the Decision for War', LKN + '/2026/11/02/vietnam-gulf-of-tonkin-escalation/'),
 4: ('Chapter 4: The Ground War, 1965–1967', LKN + '/2026/11/02/vietnam-ia-drang-search-and-destroy/'),
 5: ('Chapter 5: The Air War', LKN + '/2026/11/02/vietnam-air-war-rolling-thunder-linebacker/'),
 6: ('Chapter 6: 1968 — Khe Sanh, Tet and Huế', LKN + '/2026/11/02/vietnam-tet-offensive-hue-khe-sanh/'),
 7: ('Chapter 7: My Lai and the Law of War', LKN + '/2026/11/02/vietnam-my-lai-law-of-war/'),
 8: ('Chapter 8: Vietnamization, the POWs and Paris', LKN + '/2026/11/02/vietnam-vietnamization-pows-paris-accords/'),
 9: ('Chapter 9: The Fall of Saigon and After', LKN + '/2026/11/02/vietnam-fall-of-saigon-memory-north-carolina/'),
}
PEOPLE = {
 'moore': ('Hal Moore at Ia Đrăng', LKN + '/vietnam-war/hal-moore-ia-drang/'),
 'khesanh': ('Khe Sanh and the 26th Marines', LKN + '/vietnam-war/khe-sanh-26th-marines/'),
 'thompson': ('Thompson, Andreotta and Colburn at Mỹ Lai', LKN + '/vietnam-war/hugh-thompson-my-lai/'),
 'pows': ('The Hanoi Hilton and the POWs', LKN + '/vietnam-war/hanoi-hilton-pows-stockdale-denton-mccain/'),
 'joel': ('Lawrence Joel and the 173rd Airborne', LKN + '/vietnam-war/lawrence-joel-medal-of-honor/'),
 'sf': ('The Special Forces of Fort Bragg', LKN + '/vietnam-war/special-forces-fort-bragg-vietnam/'),
 'faq': ('The Vietnam War: questions answered', LKN + '/vietnam-war/vietnam-war-faq/'),
 'hub': ('The Vietnam War on The Lake Norman Brief', LKN + '/vietnam-war/'),
 'wallpage': ('The Wall on The Lake Norman Brief', LKN + '/vietnam-war/the-wall/'),
}

def chapter_for(date):
    if not date: return CH[9]
    if date < '1964-01-01': return CH[2]
    if date < '1965-08-01': return CH[3]
    if date < '1968-01-01': return CH[4]
    if date < '1969-01-01': return CH[6]
    if date < '1973-04-01': return CH[8]
    return CH[9]

# Battles and campaigns. provinces / countries are as spelled in the DoD casualty file.
# A name is linked to an event only when the death date and the recorded place both fall inside it.
EVENTS = [
 dict(slug='ap-bac', name='The Battle of Ấp Bắc', start='1963-01-02', end='1963-01-03', prov={'DINH TUONG'}, photo='apbac', ch=2,
      text='At Ấp Bắc in the Mekong Delta on 2 January 1963, a Viet Cong battalion held off a much larger South Vietnamese force; five U.S. helicopters were lost and three American advisers were killed.'),
 dict(slug='starlite', name='Operation Starlite', start='1965-08-18', end='1965-08-24', prov={'QUANG NGAI', 'QUANG TIN'}, svc={'MARINE CORPS'}, photo='marines-starlite', ch=4,
      text='Operation Starlite (18–24 August 1965), on the Van Tuong peninsula south of Chu Lai, was the first regimental-size U.S. ground battle of the war. Marines attacked the 1st Viet Cong Regiment by helicopter, amphibious landing and on foot.'),
 dict(slug='ia-drang', name='The Battle of the Ia Đrăng Valley', start='1965-11-14', end='1965-11-19', prov={'PLEIKU'}, units={'1 CAV DIV AIRMOBILE'}, photo='iadrang', ch=4, people=['moore'],
      text='In the Ia Đrăng Valley (14–18 November 1965), battalions of the 1st Cavalry Division (Airmobile) fought North Vietnamese regulars at Landing Zones X-Ray and Albany — the first major battle between the two armies and the first great test of the helicopter war.'),
 dict(slug='cedar-falls', name='Operation Cedar Falls', start='1967-01-08', end='1967-01-26', prov={'BINH DUONG'}, photo='cedar', ch=4,
      text='Operation Cedar Falls (8–26 January 1967) sent some 30,000 U.S. and South Vietnamese troops into the “Iron Triangle” northwest of Saigon to destroy Viet Cong base areas and tunnels.'),
 dict(slug='junction-city', name='Operation Junction City', start='1967-02-22', end='1967-05-14', prov={'TAY NINH'}, photo='army-jc', ch=4,
      text='Operation Junction City (22 February–14 May 1967), in War Zone C along the Cambodian border, was the largest U.S. operation of the war to that time and included the only major American combat parachute assault of the war.'),
 dict(slug='con-thien', name='The siege of Con Thien', start='1967-09-01', end='1967-10-31', prov={'QUANG TRI'}, photo='artillery', ch=4,
      text='Through September and October 1967, North Vietnamese artillery across the Demilitarized Zone pounded the Marine outpost at Con Thien and the bases along the DMZ in Quảng Trị Province.'),
 dict(slug='dak-to', name='The Battle of Đắk Tô', start='1967-11-03', end='1967-11-23', prov={'KONTUM'}, units={'173 AIRBORNE BDE', '4 INF DIV'}, photo='dakto', ch=4,
      text='Around Đắk Tô in the Central Highlands (3–23 November 1967), the 4th Infantry Division and the 173rd Airborne Brigade fought North Vietnamese regiments for the hills along the border, ending with the assault on Hill 875 on Thanksgiving Day.'),
 dict(slug='khe-sanh', name='The siege of Khe Sanh', start='1968-01-21', end='1968-04-08', prov={'QUANG TRI'}, photo='khesanh', ch=6, people=['khesanh'],
      text='From 21 January 1968, North Vietnamese divisions besieged the Marine combat base at Khe Sanh and its hill outposts near the Laotian border for 77 days, while U.S. aircraft dropped some 100,000 tons of bombs around it. Operation Pegasus reached the base on 8 April.'),
 dict(slug='hue', name='The Battle of Huế', start='1968-01-31', end='1968-03-02', prov={'THUA THIEN'}, photo='hue', ch=6,
      text='At Huế (31 January–2 March 1968), Marines, soldiers of the 1st Cavalry and 101st Airborne divisions and South Vietnamese troops fought house to house for 26 days to retake the old imperial capital, the longest urban battle of the war.'),
 dict(slug='tet', name='The Tet Offensive', start='1968-01-30', end='1968-03-31', prov=None, country={'SOUTH VIETNAM'}, photo='hue-tank', ch=6,
      text='Beginning on the night of 30–31 January 1968, Viet Cong and North Vietnamese forces attacked more than 100 cities and towns across South Vietnam, including the U.S. Embassy in Saigon. February 1968 was the deadliest month of the war for Americans.'),
 dict(slug='dewey-canyon', name='Operation Dewey Canyon', start='1969-01-22', end='1969-03-18', prov={'QUANG TRI'}, photo='marines-dewey', ch=8,
      text='In Operation Dewey Canyon (22 January–18 March 1969) the 9th Marines struck North Vietnamese base areas in the Đa Krông and A Shau valleys, the last major Marine offensive of the war.'),
 dict(slug='hamburger-hill', name='The Battle of Hamburger Hill', start='1969-05-10', end='1969-05-20', prov={'THUA THIEN'}, photo='army-assault', ch=8,
      text='On Đồng Ấp Bia (Hill 937) in the A Shau Valley (10–20 May 1969), the 101st Airborne Division attacked entrenched North Vietnamese troops for ten days; the soldiers called it “Hamburger Hill.” The heavy losses fed the debate at home over the war’s tactics.'),
 dict(slug='cambodia', name='The Cambodian incursion', start='1970-04-29', end='1970-07-22', prov=None, country={'CAMBODIA'}, photo='cambodia', ch=8,
      text='From 29 April to 30 June 1970, U.S. and South Vietnamese forces crossed into Cambodia to attack North Vietnamese base areas and supply caches; the announcement set off campus protests, including at Kent State.'),
 dict(slug='lam-son-719', name='Operation Lam Son 719', start='1971-02-08', end='1971-03-25', prov=None, country={'LAOS'}, photo='trail', ch=8,
      text='In Lam Son 719 (February–March 1971), South Vietnamese troops drove into Laos to cut the Ho Chi Minh Trail, carried and supported by U.S. helicopters and aircraft; more than 100 U.S. helicopters were lost.'),
 dict(slug='easter-offensive', name='The Easter Offensive', start='1972-03-30', end='1972-10-22', prov=None, country={'SOUTH VIETNAM', 'NORTH VIETNAM'}, photo='easter', ch=8,
      text='On 30 March 1972, North Vietnam launched its largest offensive since 1968, attacking across the DMZ, toward An Lộc and into the Central Highlands. By then few U.S. ground troops remained; American advisers and air power fought alongside the South Vietnamese.'),
 dict(slug='linebacker-ii', name='Linebacker II', start='1972-12-18', end='1972-12-29', prov=None, country={'NORTH VIETNAM'}, photo='linebacker', ch=5,
      text='In Linebacker II (18–29 December 1972), B-52s and fighter-bombers struck Hanoi and Haiphong for eleven days; fifteen B-52s were lost to SA-2 missiles before North Vietnam returned to the Paris talks.'),
 dict(slug='rolling-thunder', name='Operation Rolling Thunder', start='1965-03-02', end='1968-11-01', prov=None, country={'NORTH VIETNAM'}, photo='af-f105', ch=5,
      text='Operation Rolling Thunder (March 1965–November 1968) was the sustained U.S. bombing campaign against North Vietnam, flown by Air Force fighter-bombers from Thailand and Navy aircraft from carriers in the Gulf of Tonkin against some of the densest air defenses in the world.'),
 dict(slug='laos-air', name='The air war over Laos', start='1964-05-01', end='1973-04-30', prov=None, country={'LAOS'}, photo='trail', ch=5,
      text='From 1964 to 1973, U.S. aircraft bombed the Ho Chi Minh Trail and supported the war in northern Laos; many of the Americans lost over Laos were never recovered.'),
 dict(slug='mayaguez', name='The Mayaguez incident', start='1975-05-12', end='1975-05-16', prov=None, country=None, op='USS MAYAGUEZ CAPTURE', photo='frequent-wind', ch=9,
      text='After Khmer Rouge forces seized the U.S. merchant ship Mayaguez in May 1975, Marines assaulted Koh Tang island; their names are the last on the Wall.'),
]
ROLL_EVENTS = ['ia-drang', 'starlite', 'dak-to', 'khe-sanh', 'hue', 'hamburger-hill', 'dewey-canyon', 'linebacker-ii', 'mayaguez']

def event_for(r):
    d = r.get('death')
    if not d: return None
    for e in EVENTS:
        if not (e['start'] <= d <= e['end']): continue
        if e.get('op'):
            if r.get('op') == e['op']: return e
            continue
        if e.get('prov') and r.get('prov') in e['prov']: return e
        if e.get('prov') and not r.get('prov') and ((e.get('units') and r.get('unit') in e['units']) or (e.get('svc') and r.get('svc') in e['svc'] and not r.get('unit'))):
            return e
        if e.get('prov') is None and e.get('country') and r.get('country') in e['country'] and (e['slug'] != 'tet' or r.get('hostile') == 'H'): return e
    return None

def photo_for(r, ev=None, moh=False):
    if ev: return ev['photo']
    svc, unit, d = r.get('svc'), r.get('unit') or '', r.get('death') or ''
    if r.get('sex') == 'F': return 'womens-memorial'
    if r.get('body') == 'N' or r.get('cat') in ('DECLARED DEAD', 'PRESUMED DEAD'): return 'pow-vigil'
    if d and d < '1965-01-01': return 'advisers'
    if 'SPECIAL FORCES' in unit: return 'sf'
    if '173' in unit: return 'army-173'
    if 'CAV' in unit: return 'army-cav'
    if svc == 'MARINE CORPS': return 'marines-danang' if d < '1966-01-01' else ('hue-corpsman' if 'CORPSMAN' in (r.get('mos_desc') or '').upper() else 'marines-dewey')
    if svc == 'NAVY':
        if r.get('aircraft') or r.get('country') == 'NORTH VIETNAM': return 'navy-a4'
        if 'CORPSMAN' in (r.get('mos_desc') or '').upper(): return 'hue-corpsman'
        if r.get('prov') == 'OFFSHORE': return 'navy-carrier'
        return 'navy-swift'
    if svc == 'AIR FORCE':
        if r.get('country') == 'NORTH VIETNAM': return 'af-sa2'
        if r.get('country') in ('LAOS',): return 'trail'
        if r.get('aircraft'): return 'af-skyraider'
        return 'af-spooky'
    if svc == 'COAST GUARD': return 'navy-swift'
    if 'MEDIC' in (r.get('mos_desc') or '').upper(): return 'army-dustoff'
    if 'AVN' in unit or 'AVIATION' in unit or r.get('aircraft'): return 'army-hueys'
    return ['army-lz', 'army-assault', 'army-jc'][sum(map(ord, r.get('wall', ''))) % 3]

def norm_name(s):
    import unicodedata
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'"[^"]*"|\([^)]*\)', ' ', s)
    s = re.sub(r'[^A-Za-z ]', ' ', s.replace('-', ' ')).upper().split()
    return [t for t in s if t not in ('JR', 'SR', 'II', 'III', 'IV')]
