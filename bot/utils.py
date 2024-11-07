import re
import json

from aiogram.utils.i18n import gettext as _

from database.models import Site, user_sites, Channel, Organization

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
import logging

from database.base import db
from database.models import Category, user_categories
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def save_categories_to_db():
    categories = [
        {"name": "Sport", "emoji": "⚽️"},
        {"name": "Technique", "emoji": "💻"},
        {"name": "Business", "emoji": "💼"},
        {"name": "Art", "emoji": "🎨"},
        {"name": "Health", "emoji": "🩺"},
        {"name": "Culture", "emoji": "🏛"},
        {"name": "Finance", "emoji": "💵"},
        {"name": "Science", "emoji": "🔬"},
        {"name": "Travel", "emoji": "✈️"},
        {"name": "Auto", "emoji": "🚗"},
        {"name": "Food", "emoji": "🍽"},
        {"name": "Fashion", "emoji": "👗"},
        {"name": "Games", "emoji": "🎮"},
        {"name": "Education", "emoji": "📚"},
        {"name": "Music", "emoji": "🎶"},
        {"name": "Nature", "emoji": "🌿"},
        {"name": "Movies", "emoji": "🎬"},
        {"name": "Sports_techniques", "emoji": "🤾‍"},
        {"name": "Family", "emoji": "👨‍👩‍👧‍👦"},
        {"name": "Art_history", "emoji": "🖼"},
        {"name": "Genetics", "emoji": "🧬"},
        {"name": "Energy", "emoji": "⚡️"},
        {"name": "Programming", "emoji": "💻"},
        {"name": "Scientific_techniques", "emoji": "🔧"},
        {"name": "Photography", "emoji": "📸"},
        {"name": "Animation", "emoji": "🎥"},
        {"name": "Architecture", "emoji": "🏗"},
        {"name": "Environment", "emoji": "🌎"},
        {"name": "Astronomy", "emoji": "🌌"},
        {"name": "Literature", "emoji": "📖"},
        {"name": "Fitness", "emoji": "💪"},
        {"name": "Psychology", "emoji": "🧠"},
        {"name": "Philosophy", "emoji": "📜"},
        {"name": "History", "emoji": "🏺"},
        {"name": "News", "emoji": "📰"},
        {"name": "Pets", "emoji": "🐾"},
        {"name": "Spirituality", "emoji": "🕉️"},
        {"name": "Politics", "emoji": "🏛️"},
        {"name": "Economics", "emoji": "📊"},
        {"name": "Agriculture", "emoji": "🌾"},
        {"name": "Cosmetology", "emoji": "💄"},
        {"name": "Martial_Arts", "emoji": "🥋"},
        {"name": "Adventure", "emoji": "🏕"},
        {"name": "Social_Media", "emoji": "📱"},
        {"name": "Cybersecurity", "emoji": "🔐"},
        {"name": "Esports", "emoji": "🎮"},
        {"name": "Real_Estate", "emoji": "🏘"},
        {"name": "Crafts", "emoji": "🧵"},
        {"name": "Gardening", "emoji": "🌱"},
        {"name": "Volunteering", "emoji": "🤝"},
        {"name": "Language_Learning", "emoji": "🗣️"}
    ]

    existing_categories_query = select(Category.name)
    existing_categories_result = await db.execute(existing_categories_query)

    existing_categories = {row for row in existing_categories_result.scalars().all()}

    new_categories = [category for category in categories if category['name'] not in existing_categories]

    if new_categories:
        try:
            stmt = insert(Category).values(new_categories)
            await db.execute(stmt)
            await db.commit()
            print(f"Added {len(new_categories)} new categories to the database.")
        except IntegrityError as e:
            print(f"Error occurred while inserting categories: {e}")
    else:
        print("No new categories to add. All categories already exist.")


async def save_telegram_channels_to_db():
    channels = [
        {"name": "Bosh Prokratura", "username": "uzbprokuratura"},
        {"name": "Biznes-ombudsman", "username": "biznes_ombudsman"},
        {"name": "Markaziy saylov komissiyasi", "username": "electionsuz"},
        {"name": "Markaziy bank", "username": "centralbankuzbekistan"},
        {"name": "MILLIY GVARDIYA UZ | Rasmiy kanal", "username": "milliygvardiyauz_official"},
        {"name": "O'zbekiston Respublikasi Oliy Majlisi Senati", "username": "senatuz"},
        {"name": "Oliy Majlis Qonunchilik palatasi", "username": "qonunchilikpalatasi"},
        {"name": "Inson huquqlari bo'yicha vakil (ombudsman)", "username": "ombudsmanuz"},
        {"name": "Bolalar ombudsmani rasmiy telegram-kanali", "username": "Bolalar_ombudsmani"},
        {"name": "Олий суд | Расмий канал", "username": "oliysuduz"},
        {"name": "Судьялар олий кенгаши | Расмий канал", "username": "sudyalaroliykengashi"},
        {"name": "Adliya yangiliklari/Новости юстиции", "username": "adliyangiliklari"},
        {"name": "Bandlik Vazirligi", "username": "mehnatvazirligi"},
        {"name": "IIV | Rasmiy kanal", "username": "iivuz"},
        {"name": "O‘zbekiston Respublikasi Investitsiyalar", "username": "MIIT_Uz"},
        {"name": "Iqtisodiyot va moliya vazirligi", "username": "minecofinuz"},
        {"name": "Madaniyat.uz I Rasmiy kanal", "username": "madaniyatvazirligi"},
        {"name": "Mudofaa vazirligi rasmiy kanali", "username": "mudofaavazirligi"},
        {"name": "Maktabgacha va maktab ta'limi vazirligi", "username": "uzedu"},
        {"name": "Edu UZ", "username": "eduuz"},
        {"name": "Digital.uz", "username": "mitcuz"},
        {"name": "Sport vazirligi", "username": "Minsportuz"},
        {"name": "Соғлиқни сақлаш вазирлиги | Вакцина", "username": "ssvuz"},
        {"name": "Matbuot kotibi - Suv xo‘jaligi vazirligi", "username": "TGminwater"},
        {"name": "Tashqi ishlar vazirligi", "username": "uzbekmfa"},
        {"name": "Ўзбекистон Республикаси Транспорт вазирлиги", "username": "Mintrans_uz"},
        {"name": "Kon-geologiya vazirligi | Мингеологии | Ministry of Mining and Geology", "username": "uzdavgeolcom"},
        {"name": "FAVQULODDA VAZIYATLAR VAZIRLIGI/МИНИСТЕРСТВО ПО ЧРЕЗВЫЧАЙНЫМ СИТУАЦИЯМ", "username": "MCHSUzbek"},
        {"name": "MINENERGY.UZ", "username": "minenergy_uz"},
        {"name": "QISHLOQ XO'JALIGI VAZIRLIGI", "username": "uzagroministry"},
        {"name": "QURILISH VA UY-JOY KOMMUNAL XO'JALIGI VAZIRLIGI", "username": "minstroyuz"},
        {"name": "Ekologiya vazirligi | Министерство Экологии | Ministry of Ecology", "username": "ecogovuz"},
        {"name": "Avtomobil yo'llari qo'mitasi", "username": "avtoyulqumita"},
        {"name": "O'zbekiston Respublikasi Davlat bojxona qo'mitasining rasmiy axborot kanali",
         "username": "customschannel"},
        {"name": "VETLEGNEWS", "username": "VeterinariansUzbekistan"},
        {"name": "Din ishlari bo‘yicha qo‘mita", "username": "DinQumita"},
        {"name": "Ipakchilik va jun sanoatini rivojlantirish qo'mitasi|Rasmiy kanal",
         "username": "ipakchilikvajunsanoati"},
        {"name": "Миллатлараро муносабатлар қўмитаси", "username": "millatlararoqumita"},
        {"name": "OlympicUz", "username": "OlympicUz"},
        {"name": "Oila va xotin-qizlar qo'mitasi", "username": "Oila va xotin-qizlar qo'mitasi"},
        {"name": "Raqobat qo‘mitasi", "username": "RaqobatGovUz"},
        {"name": "Soliq xizmati xabarlari - Rasmiy kanal", "username": "soliqnews"},
        {"name": "Саноат хавфсизлиги давлат қўмитаси ахборот хизмати", "username": "scisuz"},
        {"name": "Sanitariya-epidemiologiya qo'mitasi | Vaksina oling!", "username": "sanepidcommittee"},
        {"name": "Uzbektourism.uz", "username": "uzbektourismofficial"},
        {"name": "AOKA - Rasmiy kanali", "username": "aoka_uz"},
        {"name": "Агентство Uzatom Агентлиги", "username": "uzatom_info"},
        {"name": "Bilimni baholash agentligi", "username": "BaholashUz"},
        {"name": "Hydromet.uz", "username": "uzgydromet"},
        {"name": "Davlat xizmatini rivojlantirish agentligi | АРГОС", "username": "argos_uz"},
        {"name": "Давлат активларини бошқариш агентлиги", "username": "DAVAKTIVUZ"},
        {"name": "Yoshlar ishlari agentligi", "username": "yoshlaragentligi"},
        {"name": "Ijtimoiy himoya milliy agentligi", "username": "ijtimoiyhimoya_agentligi"},
        {"name": "NAPP", "username": "napp_uz"},
        {"name": "Innovatsion rivojlanish agentligi", "username": "innovatsion_rivojlanish"},
        {"name": "Ixtisoslashtirilgan ta'lim muassasalari agentligi", "username": "piimauz"},
        {"name": "KADASTR AGENTLIGI - RASMIY", "username": "uz_kadastr"},
        {"name": "Korrupsiyaga qarshi kurashish agentligi", "username": "antikor_uzb"},
        {"name": "UzKosmos", "username": "uzbekkosmos_uz"},
        {"name": "O‘zbekiston Milliy antidoping agentligi (UzNADA)", "username": "antidopinguz"},
        {"name": "Madaniy meros agentligi", "username": "madaniy_meros_uz"},
        {"name": "MAHALLABAY ISHLASH VA TADBIRKORLIKNI RIVOJLANTIRISH AGENTLIGI|Rasmiy kanal", "username": "uzadeuz"},
        {"name": "Strategik islohotlar agentligi - Rasmiy kanal", "username": "siauzbekistan"},
        {"name": "STATISTIKA | Rasmiy kanal", "username": "statistika_rasmiy"},
        {"name": "Migratsiya agentligi / The Migration Agency", "username": "migratsiyaagentligi"},
        {"name": "Ўзбекистон техник жиҳатдан тартибга солиш агентлиги | Расмий канал", "username": "UzstandardChannel"},
        {"name": "«O’zaviatsiya» Agentligi", "username": "uzcaa"},
        {"name": "Uzpharmagency", "username": "Uzpharm_agency"},
        {"name": "O‘ZARXIV AGENTLIGI", "username": "uzarxivs"},
        {"name": "O'SIMLIKLAR KARANTINI VA HIMOYASI AGENTLIGI", "username": "uzdavkarantinuz"},
        {"name": "O‘zbekiston Kinematografiya agentligi", "username": "uzbekkinopress"},
        {"name": "Energetika bozori regulyatori//Rasmiy kanal", "username": "emdra_uz"},
        {"name": "UZAGROINSPEKSIYA XABARLARI", "username": "uzagroinspeksiyanews"},
        {"name": "O‘ZENERGOINSPEKSIYA", "username": "Energoinspeksiya"},
        {"name": "Transport nazorati inspeksiyasi", "username": "Uztransnazorat"},
        {"name": "DAVLAT EKOLOGIK EKSPERTIZASI MARKAZI", "username": "ecoekspertiza"},
        {"name": "bukhari.uz", "username": "bukhariuz"},
        {"name": "Center for Economic Research and Reforms", "username": "cerruz"},
        {"name": "NHRC | НЦПЧ", "username": "NationalHumanRightsCenter"},
        {"name": "IJTIMOIY FIKR", "username": "ijtimoiyfikruz"},
        {"name": "IT taʼlim", "username": "edurtm_uz"},
        {"name": "MARKAZ XABARLARI", "username": "manaviyat_markaz"},
        {"name": "Chiqindilarni boshqarish agentligi | Агентство по управлению отходами", "username": "sanitationuz"},
        {"name": "TRM - Rasmiy kanal", "username": "trm_uz"},
        {"name": "Tourquality.uz", "username": "tourqualityuz"},
        {"name": "Ўзбекистондаги Ислом цивилизацияси маркази", "username": "islommarkazi"},
        {"name": "Uzpharmcontrol", "username": "uzpharmcontrol"},
        {"name": "SUDEX.UZ | RSEM | РЦСЭ", "username": "sudexuz"},
        {"name": "Milliy markaz (AKIS) RASMIY", "username": "AKIS_milliy_markaz"},
        {"name": "Pensiya jamg'armasi | Rasmiy kanal", "username": "PensionFundRUz"},
        {"name": "VAQF.UZ | Расмий канал", "username": "vaqfuz"},
        {"name": "DBA", "username": "bacademy"},
        {"name": "DAVLAT KADASTRLARI PALATASI", "username": "DavKadastrPalata"},
        {"name": "DTSJ-Tibbiy sug'urta | Rasmiy kanal", "username": "tibbiysugurta"},
        {"name": "Prokuratura Departamenti", "username": "Department_uz"},
        {"name": "Mahalla fondining | rasmiy kanali", "username": "obfmuz"},
        {"name": "Фонд развития культуры и искусства | Madaniyat va san’atni rivojlantirish jamg’armasi",
         "username": "acdfuz"},
        {"name": "MIB faoliyatidan", "username": "mib_faoliyatidan"},
        {"name": "Oliy ta’lim, fan va innovatsiyalar vazirligi huzuridagi Oliy attestatsiya komissiyasi",
         "username": "attestatsiya"},
        {"name": "Oila va gender ilmiy-tadqiqot instituti", "username": "mahallavaoila_instituti"},
        {"name": "Savdo-sanoat palatasi", "username": "uzchamber"},
        {"name": "O'zR FA | FAN - JAMIYAT TARAQQIYOTINI OLG'A SILJITUVCHI KUCH, VOSITA BO'LMOG'I LOZIM!",
         "username": "ANRUz"},
        {"name": "Muslim.uz", "username": "muslimuzportal"},
        {"name": "O‘zbekiston Badiiy akademiyasi", "username": "artacademyuz"},
        {"name": "O'zbekiston kasaba uyushmalari Federatsiyasi", "username": "uzkufk"},
        {"name": "O'zbekkonsert.uz / Rasmiy kanal", "username": "uzbekkonsert_dm"},
        {"name": "El-yurt umidi Foundation", "username": "elyurtumidifoundation"},
        {"name": "Dori-Darmon AK", "username": "doridarmon_ak"},
        {"name": "IES.UZ| Rasmiy kanali", "username": "ies_uz"},
        {"name": "NKMK AJ - АО НГМК", "username": "ngmkofficial"},
        {"name": "NAVOIYURAN DK", "username": "Navoiyuran_official"},
        {"name": "AGMK - OKMK | Rasmiy kanal", "username": "ao_agmk"},
        {"name": "Tadbirkorlikni rivojlantirish kompaniyasi AJ", "username": "edcomuz"},
        {"name": "Toshshahartransxizmat AJ Matbuot xizmati", "username": "tshtxuz"},
        {"name": "Hududiy elektr tarmoqlari AJ bilan muloqot", "username": "hetmuloqot"},
        {"name": "HUDUDGAZTA'MINOT AJ", "username": "AO_Hududgaztaminot"},
        {"name": "UZBEKISTAN AIRPORTS", "username": "uzbairportsuz"},
        {"name": "Uzbekistan Airways", "username": "uzbekistanairways"},
        {"name": "O`zkimyosanoat AJ | Rasmiy kanali", "username": "uzkimyosanoat"},
        {"name": "O'zdonmahsulot AK yangiliklari", "username": "uzdonyangiliklari"},
        {"name": "O‘zAgroLizing | Rasmiy kanal", "username": "uzal_uz"},
        {"name": "UzAuto_official", "username": "O‘zAgroLizing | Rasmiy kanal"},
        {"name": "Uzagrokimyohimoya AJ", "username": "UZAGROKIMYOHIMOYA"},
        {"name": "O‘zbekiston temir yo‘llari AJ", "username": "uzrailways_uz"},
        {"name": "UZEXUZ", "username": "uzexuz"},
        {"name": "UZTELECOM", "username": "uztelecomuz"},
        {"name": "O‘zsuvta'minot", "username": "uzsuv"},
        {"name": "O'zbekiston milliy elektr tarmoqlari AJ", "username": "uzmetaxborotxizmati"},
        {"name": "Oʻzbekkoʻmir aksiyadorlik jamiyati", "username": "uzbekcoaluz"},
        {"name": "Agrobank", "username": "AgrobankChannel"},
        {"name": "ASAKABANK", "username": "Asakabank_official"},
        {"name": "aloqabank", "username": "AloqaBank"},
        {"name": "Xalq Banki", "username": "xalqbankinfo"},
        {"name": "MKBANK", "username": "mkbankuz"},
        {"name": "SANOAT QURILISH BANK", "username": "sqbuz"},
        {"name": "NBU_official", "username": "nbu_official"},
        {"name": "Biznesni Rivojlantirish Banki", "username": "brb_uzb"},
        {"name": "Ipotekabank OTP Group", "username": "ipotekabankofficial"},
        {"name": "Turonbank", "username": "turonbankuz"},
        {"name": "«Oʻzagrosugʻurta» AJ", "username": "uzagrosugurta_aj"},
        {"name": "Uzbekinvest Insurance", "username": "uzbekinvest"},
        {"name": "O‘zbekiston mahallalari uyushmasi rasmiy kanali", "username": "uzmahallalari"},
        {"name": "O'zqurilishmateriallari", "username": "ozqurilishmateriallari"},
        {"name": "UzTextile-News | Rasmiy kanal", "username": "uztsuz"},
        {"name": "Ўзбекистон асаларичилари уюшмаси", "username": "beekeepersuz"},
        {"name": "“O‘zbekbaliqsanoat” uyushmasi", "username": "uzbaliqsanoat_uz"},
        {"name": "O‘zbekiston Yozuvchilar uyushmasi", "username": "yozuvchilar_uz"},
        {"name": "O'zbekiston banklari Assotsiatsiyasi", "username": "ubamatbuot"},
        {"name": "O’zbekiston Eksportchilari Uyushmasi", "username": "eksportuyushma"},
        {"name": "Karakalpakstan.uz", "username": "QResMinistrlerKenesi"},
        {"name": "Андижон вилояти ҳокимлиги матбуот хизмати", "username": "andpress"},
        {"name": "BUXORO.UZ | Rasmiy kanal", "username": "buxorouz_official"},
        {"name": "Jizzax.Uz|Rasmiy kanal", "username": "jizzaxviloyatihokimligi"},
        {"name": "NAVOI.UZ | Navoiy viloyati hokimligi", "username": "navoiy_hokimligi"},
        {"name": "Namangan viloyati hokimligi", "username": "namvilhok"},
        {"name": "Samarqand viloyati hokimligi 🇺🇿", "username": "e_turdimov"},
        {"name": "Sirdaryo.uz", "username": "SirdaryoUz"},
        {"name": "Surxondaryo viloyati hokimligi", "username": "axborot_xizmati"},
        {"name": "Toshkent viloyati hokimligi", "username": "toshvilpressa"},
        {"name": "Фарғона вилояти ҳокимлиги", "username": "fvhokimligi"},
        {"name": "Xorazm.uz", "username": "xorazm_uz_rasmiy"},
        {"name": "QASHQADARYO.UZ | RASMIY - Қашқадарё вилояти ҳокимлиги - Qashqadaryo viloyati hokimligi",
         "username": "qvh_axboroti"},
        {"name": "Toshkent shahar hokimligi Matbuot xizmati", "username": "poytaxt_uz"},

    ]

    existing_channels_query = select(Channel.username)
    existing_channels_result = await db.execute(existing_channels_query)

    existing_usernames = {row for row in existing_channels_result.scalars().all()}

    new_channels = [channel for channel in channels if channel['username'] not in existing_usernames]

    if new_channels:
        try:
            stmt = insert(Channel).values(new_channels)
            await db.execute(stmt)
            await db.commit()
            print(f"Added {len(new_channels)} new Telegram channels to the database.")
        except IntegrityError as e:
            print(f"Error occurred while inserting Telegram channels: {e}")
    else:
        print("No new channels to add. All channels already exist.")


async def add_category(name: str, emoji: str, user_id: int):
    existing_category_query = select(Category).where(Category.name == name)
    existing_category_result = await db.execute(existing_category_query)
    existing_category = existing_category_result.scalar()

    if existing_category:
        user_category_query = select(user_categories).where(
            (user_categories.c.user_id == user_id) &
            (user_categories.c.category_id == existing_category.id)
        )
        user_category_result = await db.execute(user_category_query)

        if user_category_result.scalar():
            msg = _("❗Ushbu kategoriya allaqachon mavjud.")
            return msg

        try:
            stmt = insert(user_categories).values(user_id=user_id, category_id=existing_category.id)
            await db.execute(stmt)
            await db.commit()
            msg = _("✅ Kategoriya muvaffaqqiyatli bog'landi.")
            return msg

        except IntegrityError as e:
            await db.rollback()
            logging.error(f"IntegrityError while linking category to user: {e}")
            msg = _("Kategoriya qo'shishga urinishda xatolik yuz berdi.")
            return msg

    try:
        stmt = insert(Category).values(name=name, emoji=emoji).returning(Category.id)
        result = await db.execute(stmt)
        category_id = result.scalar()

        stmt_user_category = insert(user_categories).values(user_id=user_id, category_id=category_id)
        await db.execute(stmt_user_category)
        await db.commit()

        msg = _("✅ Ushbu kategoriya muvaffaqqiyatli saqlandi va bog'landi!")
        return msg

    except IntegrityError as e:
        await db.rollback()
        logging.error(f"IntegrityError while adding category: {e}")
        msg = _("Kategoriya qo'shishga urinishda xatolik yuz berdi.")
        return msg
    except Exception as e:
        await db.rollback()
        logging.error(f"Unexpected error while adding category: {e}")
        msg = _("Kategoriya qo'shishda xatolik yuz berdi.")
        return msg


async def process_urls(user_id, urls):
    invalid_urls = []
    already_saved_urls = []
    site_ids = []

    for url in urls:
        if not re.match(r'^https?://', url):
            invalid_urls.append(url)
            continue

        site = (await db.execute(select(Site).where(Site.url == url))).scalar()

        if not site:
            try:
                result = await db.execute(insert(Site).values(url=url).returning(Site.id))
                site_id = result.scalar()
            except IntegrityError:
                invalid_urls.append(url)
                continue
        else:
            site_id = site.id

        user_site_exists = await db.execute(
            select(user_sites).where(user_sites.c.user_id == user_id, user_sites.c.site_id == site_id)
        )

        if user_site_exists.fetchone():
            already_saved_urls.append(url)
        else:
            site_ids.append(site_id)

    return site_ids, already_saved_urls, invalid_urls


async def save_organizations_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for entry in data:
            result = await db.execute(select(Organization).filter_by(phone=entry['phone']))
            existing_org = result.scalars().first()

            if existing_org is None:
                new_org = Organization(
                    name_uz=entry['organization']['uz'],
                    name_en=entry['organization']['en'],
                    name_ru=entry['organization']['ru'],
                    original_name=entry['name']['original'],
                    latin_name=entry['name']['latin'],
                    phone=entry['phone'],
                    type_uz=entry['type']['uz'],
                    type_en=entry['type']['en'],
                    type_ru=entry['type']['ru']
                )
                db.add(new_org)

        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Error saving organizations: {e}")
    finally:
        await db.close()
