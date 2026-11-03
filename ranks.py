COMMON={'PVT':'Private','PV1':'Private','PV2':'Private','PFC':'Private First Class','CPL':'Corporal','SGT':'Sergeant',
'2LT':'Second Lieutenant','2NDLT':'Second Lieutenant','1LT':'First Lieutenant','1STLT':'First Lieutenant','MAJ':'Major','COL':'Colonel',
'LTC':'Lieutenant Colonel','LTCOL':'Lieutenant Colonel','BG':'Brigadier General','BGEN':'Brigadier General','MG':'Major General','MAJGEN':'Major General',
'WO':'Warrant Officer','WO1':'Warrant Officer 1','WO-1':'Warrant Officer 1','CW2':'Chief Warrant Officer 2','CWO2':'Chief Warrant Officer 2','CW3':'Chief Warrant Officer 3','CWO3':'Chief Warrant Officer 3',
'CW4':'Chief Warrant Officer 4','CWO4':'Chief Warrant Officer 4','CWO-4':'Chief Warrant Officer 4','CADET':'Cadet'}
ARMY={'SP4':'Specialist Four','SPC':'Specialist','SP5':'Specialist Five','SP6':'Specialist Six','SSG':'Staff Sergeant','SFC':'Sergeant First Class',
'PSG':'Platoon Sergeant','MSG':'Master Sergeant','1SG':'First Sergeant','SGM':'Sergeant Major','CSM':'Command Sergeant Major','CPT':'Captain','CAPT':'Captain'}
USMC={'LCPL':'Lance Corporal','SSGT':'Staff Sergeant','GYSGT':'Gunnery Sergeant','MSGT':'Master Sergeant','1STSGT':'First Sergeant','MGYSGT':'Master Gunnery Sergeant',
'SGTMAJ':'Sergeant Major','CAPT':'Captain','CPT':'Captain'}
USAF={'AB':'Airman Basic','AMN':'Airman','A3C':'Airman Third Class','A2C':'Airman Second Class','A1C':'Airman First Class','SSGT':'Staff Sergeant','TSGT':'Technical Sergeant',
'MSGT':'Master Sergeant','SMSGT':'Senior Master Sergeant','CMSGT':'Chief Master Sergeant','CAPT':'Captain','CPT':'Captain'}
NAVY={'SR':'Seaman Recruit','SA':'Seaman Apprentice','SN':'Seaman','AA':'Airman Apprentice','AN':'Airman','FA':'Fireman Apprentice','FN':'Fireman',
'CR':'Constructionman Recruit','CN':'Constructionman','HA':'Hospitalman Apprentice','HN':'Hospitalman','PO3':'Petty Officer Third Class','PO2':'Petty Officer Second Class',
'PO1':'Petty Officer First Class','CPO':'Chief Petty Officer','SCPO':'Senior Chief Petty Officer','MCPO':'Master Chief Petty Officer','ENS':'Ensign',
'LTJG':'Lieutenant (junior grade)','LT':'Lieutenant','LCDR':'Lieutenant Commander','CDR':'Commander','CAPT':'Captain','RADM':'Rear Admiral'}
BY={'ARMY':ARMY,'MARINE CORPS':USMC,'AIR FORCE':USAF,'NAVY':NAVY,'COAST GUARD':NAVY}
import re as _re
def rank_full(svc,r):
    v = BY.get(svc,{}).get(r) or COMMON.get(r)
    if v: return v
    if svc in ('NAVY','COAST GUARD'):
        m = _re.match(r'^[A-Z]{2,4}?(3|2|1|C|CS|CM)$', r)
        if m: return {'3':'Petty Officer Third Class','2':'Petty Officer Second Class','1':'Petty Officer First Class','C':'Chief Petty Officer','CS':'Senior Chief Petty Officer','CM':'Master Chief Petty Officer'}[m.group(1)]
    return r
SVC={'ARMY':'U.S. Army','MARINE CORPS':'U.S. Marine Corps','AIR FORCE':'U.S. Air Force','NAVY':'U.S. Navy','COAST GUARD':'U.S. Coast Guard'}
