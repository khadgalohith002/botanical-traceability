"""
PhytoTrace Botanical Crop Catalog
=================================
Single source of truth for the 20 supported botanical crops:
- Turmeric (Curcuma longa)
- Neem (Azadirachta indica)
- Tulsi / Holy Basil (Ocimum tenuiflorum)
- Ashwagandha (Withania somnifera)
- Aloe Vera (Aloe vera)
- Ginger (Zingiber officinale)
- Amla / Indian Gooseberry (Phyllanthus emblica)
- Moringa (Moringa oleifera)
- Brahmi (Bacopa monnieri)
- Shatavari (Asparagus racemosus)
- Giloy (Tinospora cordifolia)
- Lemongrass (Cymbopogon citratus)
- Peppermint (Mentha × piperita)
- Senna (Senna alexandrina)
- Black Pepper (Piper nigrum)
- Cardamom (Elettaria cardamomum)
- Cinnamon (Cinnamomum verum)
- Clove (Syzygium aromaticum)
- Coriander (Coriandrum sativum)
- Fenugreek (Trigonella foenum-graecum)

Each crop entry contains:
- id: stable 3-letter identifier
- name: English common name
- scientific_name: botanical taxonomy (preserved across all languages)
- category: one of 'Roots & Rhizomes', 'Medicinal Plants', 'Herbs', 'Spices'
- icon: visual emoji icon for illiterate/multilingual farmers
- variety_sample: typical commercial/GI-tagged variety in India
- translations: full 12-language dictionary (en, kn, te, hi, ta, ml, mr, bn, pa, or, gu, ur)
"""

CATEGORIES = [
    {"id": "all", "icon": "🌿", "en": "All Categories", "name": "All Categories"},
    {"id": "roots", "icon": "🫚", "en": "Roots & Rhizomes", "name": "Roots & Rhizomes"},
    {"id": "medicinal", "icon": "🪴", "en": "Medicinal Plants", "name": "Medicinal Plants"},
    {"id": "herbs", "icon": "🌱", "en": "Herbs", "name": "Herbs"},
    {"id": "spices", "icon": "🌰", "en": "Spices", "name": "Spices"},
]

CATEGORY_TRANSLATIONS = {
    "all": {
        "en": "All Categories",
        "kn": "ಎಲ್ಲಾ ವಿಭಾಗಗಳು",
        "te": "అన్ని విభాగాలు",
        "hi": "सभी श्रेणियां",
        "ta": "அனைத்து பிரிவுகள்",
        "ml": "എല്ലാ വിഭാഗങ്ങളും",
        "mr": "सर्व श्रेणी",
        "bn": "সব বিভাগ",
        "pa": "ਸਾਰੀਆਂ ਸ਼੍ਰੇਣੀਆਂ",
        "or": "ସମସ୍ତ ବର୍ଗ",
        "gu": "બધી શ્રેણીઓ",
        "ur": "تمام زمرے",
    },
    "roots": {
        "en": "Roots & Rhizomes",
        "kn": "ಬೇರುಗಳು ಮತ್ತು ಗೆಡ್ಡೆಗಳು",
        "te": "వేర్లు మరియు దుంపలు",
        "hi": "जड़ें और प्रकंद",
        "ta": "வேர்கள் மற்றும் கிழங்குகள்",
        "ml": "വേരുകളും കിഴങ്ങുകളും",
        "mr": "मुळे आणि कंद",
        "bn": "মূল ও কন্দ",
        "pa": "ਜੜ੍ਹਾਂ ਅਤੇ ਕੰਦ",
        "or": "ଚେର ଏବଂ କନ୍ଦ",
        "gu": "મૂળ અને ગાંઠો",
        "ur": "جڑیں اور زیر زمین تنے",
    },
    "medicinal": {
        "en": "Medicinal Plants",
        "kn": "ಔಷಧೀಯ ಸಸ್ಯಗಳು",
        "te": "ఔషధ మొక్కలు",
        "hi": "औषधीय पौधे",
        "ta": "மூலிகைத் தாவரங்கள்",
        "ml": "ഔഷധ സസ്യങ്ങൾ",
        "mr": "औषधी वनस्पती",
        "bn": "ভেষজ উদ্ভিদ",
        "pa": "ਔਸ਼ਧੀ ਪੌਦੇ",
        "or": "ଔଷଧୀୟ ଉଦ୍ଭିଦ",
        "gu": "ઔષધીય વનસ્પતિઓ",
        "ur": "طبی پودے",
    },
    "herbs": {
        "en": "Herbs",
        "kn": "ಗಿಡಮೂಲಿಕೆಗಳು",
        "te": "మూలికలు",
        "hi": "जड़ी-बूटियां",
        "ta": "பச்சை மூலிகைகள்",
        "ml": "ഔഷധച്ചെടികൾ",
        "mr": "जडीबुटी",
        "bn": "ভেষজ পাতা",
        "pa": "ਜੜੀ-ਬੂਟੀਆਂ",
        "or": "ଜଡିବୁଟି",
        "gu": "જડીબુટ્ટીઓ",
        "ur": "جڑی بوٹیاں",
    },
    "spices": {
        "en": "Spices",
        "kn": "ಸಾಂಬಾರ ಪದಾರ್ಥಗಳು",
        "te": "సుగంధ ద్రవ్యాలు",
        "hi": "मसाले",
        "ta": "மசாலாப் பொருட்கள்",
        "ml": "സുഗന്ധവ്യഞ്ജനങ്ങൾ",
        "mr": "मसाले",
        "bn": "মসলা",
        "pa": "ਮਸਾਲੇ",
        "or": "ମସଲା",
        "gu": "મસાલા",
        "ur": "مصالحہ جات",
    },
}

NOT_LISTED_ID = "NOT_LISTED"

NOT_LISTED_TRANSLATIONS = {
    "label": {
        "en": "❓ Not listed? Contact an administrator",
        "kn": "❓ ಬೆಳೆ ಪಟ್ಟಿಯಲ್ಲಿಲ್ಲವೇ? ಆಡಳಿತಾಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ",
        "te": "❓ పంట జాబితాలో లేదా? నిర్వాహకుడిని సంప్రదించండి",
        "hi": "❓ फसल सूची में नहीं है? व्यवस्थापक से संपर्क करें",
        "ta": "❓ பயிர் பட்டியலில் இல்லையா? நிர்வாகியைத் தொடர்பு கொள்ளவும்",
        "ml": "❓ വിള പട്ടികയിൽ ഇല്ലേ? അഡ്മിനിസ്ട്രേറ്ററെ ബന്ധപ്പെടുക",
        "mr": "❓ पीक यादीत नाही? प्रशासकाशी संपर्क साधा",
        "bn": "❓ ফসল তালিকায় নেই? প্রশাসকের সাথে যোগাযোগ করুন",
        "pa": "❓ ਫਸਲ ਸੂਚੀ ਵਿੱਚ ਨਹੀਂ ਹੈ? ਪ੍ਰਬੰਧਕ ਨਾਲ ਸੰਪਰਕ ਕਰੋ",
        "or": "❓ ଫସଲ ତାଲିକାରେ ନାହିଁ? ପ୍ରଶାସକଙ୍କ ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ",
        "gu": "❓ પાક યાદીમાં નથી? વહીવટકર્તાનો સંપર્ક કરો",
        "ur": "❓ فصل فہرست میں نہیں ہے؟ منتظم سے رابطہ کریں",
    },
    "notice": {
        "en": "To maintain cryptographic property graph traceability standards, unverified botanical crops cannot be registered directly. Please contact your regional cooperative coordinator or call the Farmer Support Desk (1800-425-TREE / admin@phytotrace.org) to request botanical provenance onboarding.",
        "kn": "ಪ್ರಾಪರ್ಟಿ ಗ್ರಾಫ್ ಪತ್ತೆಹಚ್ಚುವಿಕೆಯ ಮಾನದಂಡಗಳನ್ನು ಕಾಪಾಡಲು, ಪರಿಶೀಲಿಸದ ಗಿಡಮೂಲಿಕೆ ಬೆಳೆಗಳನ್ನು ನೇರವಾಗಿ ನೋಂದಾಯಿಸಲಾಗುವುದಿಲ್ಲ. ಹೊಸ ಬೆಳೆಯನ್ನು ಸೇರಿಸಲು ದಯವಿಟ್ಟು ರೈತ ಸಹಾಯವಾಣಿಯನ್ನು (1800-425-TREE / admin@phytotrace.org) ಸಂಪರ್ಕಿಸಿ.",
        "te": "ట్రేసిబిలిటీ ప్రమాణాల దృష్ట్యా, ధృవీకరించని పంటలను నేరుగా నమోదు చేయలేరు. దయచేసి రైతు సహాయ డెస్క్‌ను సంప్రదించండి (1800-425-TREE / admin@phytotrace.org).",
        "hi": "ट्रेसेबिलिटी मानकों को बनाए रखने के लिए, असत्यापित फसलों को सीधे पंजीकृत नहीं किया जा सकता। कृपया अपनी सहकारी समिति या किसान सहायता केंद्र (1800-425-TREE / admin@phytotrace.org) से संपर्क करें।",
        "ta": "சரிபார்க்கப்படாத பயிர்களை நேரடியாகப் பதிவு செய்ய முடியாது. தயவுசெய்து விவசாயி உதவி மையத்தைத் தொடர்பு கொள்ளவும் (1800-425-TREE / admin@phytotrace.org).",
        "ml": "പരിശോധിക്കാത്ത വിളകൾ നേരിട്ട് രജിസ്റ്റർ ചെയ്യാനാകില്ല. സഹായത്തിന് 1800-425-TREE / admin@phytotrace.org എന്ന നമ്പറിൽ ബന്ധപ്പെടുക.",
        "mr": "अनधिकृत पिके थेट नोंदवता येत नाहीत. कृपया शेतकरी मदत कक्षाशी संपर्क साधा (1800-425-TREE / admin@phytotrace.org).",
        "bn": "অযাচাইকৃত ফসল সরাসরি নথিভুক্ত করা যাবে না। কৃষক সহায়তা কেন্দ্রে যোগাযোগ করুন (1800-425-TREE / admin@phytotrace.org)।",
        "pa": "ਗੈਰ-ਪ੍ਰਮਾਣਿਤ ਫਸਲਾਂ ਨੂੰ ਸਿੱਧੇ ਦਰਜ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ। ਕਿਰਪਾ ਕਰਕੇ ਕਿਸਾਨ ਸਹਾਇਤਾ ਕੇਂਦਰ (1800-425-TREE / admin@phytotrace.org) ਨਾਲ ਸੰਪਰਕ ਕਰੋ।",
        "or": "ଯାଞ୍ଚ ହୋଇନଥିବା ଫସଲ ସିଧାସଳଖ ପଞ୍ଜିକୃତ ହୋଇପାରିବ ନାହିଁ। କୃଷକ ସହାୟତା ଡେସ୍କ (1800-425-TREE / admin@phytotrace.org) କୁ ଯୋଗାଯୋଗ କରନ୍ତୁ।",
        "gu": "ચકાસાયેલ ન હોય તેવા પાકો સીધા નોંધણી કરી શકાતા નથી. કૃપા કરીને ખેડૂત હેલ્પ ડેસ્ક (1800-425-TREE / admin@phytotrace.org) નો સંપર્ક કરો.",
        "ur": "غیر تصدیق شدہ فصلوں کو براہ راست درج نہیں کیا جا سکتا۔ براہ کرم کسان ہیلپ ڈیسک (1800-425-TREE / admin@phytotrace.org) سے رابطہ کریں۔",
    }
}

# Master List of 20 Botanical Crops
CROP_CATALOG = [
    {
        "id": "TUR",
        "name": "Turmeric",
        "scientific_name": "Curcuma longa",
        "category_id": "roots",
        "category": "Roots & Rhizomes",
        "icon": "🫚",
        "color": "#2C694E",
        "variety_sample": "Alleppey Finger / Lakadong",
        "translations": {
            "en": "Turmeric",
            "kn": "ಅರಿಶಿನ",
            "te": "పసుపు",
            "hi": "हल्दी",
            "ta": "மஞ்சள்",
            "ml": "മഞ്ഞൾ",
            "mr": "हळद",
            "bn": "হলুদ",
            "pa": "ਹਲਦੀ",
            "or": "ହଳଦୀ",
            "gu": "હળદર",
            "ur": "ہلدی",
        }
    },
    {
        "id": "NEE",
        "name": "Neem",
        "scientific_name": "Azadirachta indica",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "🌳",
        "color": "#1B4332",
        "variety_sample": "Wildcraft Kernel",
        "translations": {
            "en": "Neem",
            "kn": "ಬೇವು",
            "te": "వేప",
            "hi": "नीम",
            "ta": "வேம்பு",
            "ml": "വേപ്പ്",
            "mr": "कडुनिंब",
            "bn": "নিম",
            "pa": "ਨਿੰਮ",
            "or": "ନିମ",
            "gu": "લીમડો",
            "ur": "نیم",
        }
    },
    {
        "id": "TUL",
        "name": "Tulsi / Holy Basil",
        "scientific_name": "Ocimum tenuiflorum",
        "category_id": "herbs",
        "category": "Herbs",
        "icon": "🌿",
        "color": "#40916C",
        "variety_sample": "Krishna / Rama Tulsi",
        "translations": {
            "en": "Tulsi / Holy Basil",
            "kn": "ತುಳಸಿ",
            "te": "తులసి",
            "hi": "तुलसी",
            "ta": "துளசி",
            "ml": "തുളസി",
            "mr": "तुळस",
            "bn": "তুলসী",
            "pa": "ਤੁਲਸੀ",
            "or": "ତୁଳସୀ",
            "gu": "તુલસી",
            "ur": "تلسی",
        }
    },
    {
        "id": "ASH",
        "name": "Ashwagandha",
        "scientific_name": "Withania somnifera",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "🌾",
        "color": "#74A892",
        "variety_sample": "Nagori / Jawahar-20",
        "translations": {
            "en": "Ashwagandha",
            "kn": "ಅಶ್ವಗಂಧ",
            "te": "అశ్వగంధ",
            "hi": "अश्वगंधा",
            "ta": "அஸ்வகந்தா / அமுக்கிரா",
            "ml": "അമുക്കുരം",
            "mr": "अश्वगंधा",
            "bn": "অশ্বগন্ধা",
            "pa": "ਅਸ਼ਵਗੰਧਾ",
            "or": "ଅଶ୍ୱଗନ୍ଧା",
            "gu": "અશ્વગંધા",
            "ur": "اشوگندھا",
        }
    },
    {
        "id": "ALO",
        "name": "Aloe Vera",
        "scientific_name": "Aloe vera",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "🪴",
        "color": "#52B788",
        "variety_sample": "Barbadensis Miller",
        "translations": {
            "en": "Aloe Vera",
            "kn": "ಲೋಳೆಸರ",
            "te": "కలబంద",
            "hi": "घृतकुमारी (एलोवेरा)",
            "ta": "கற்றாழை",
            "ml": "കറ്റാർവാഴ",
            "mr": "कोरफड",
            "bn": "ঘৃতকুমারী",
            "pa": "ਕਵਾਰ ਗੰਦਲ",
            "or": "ଘିକୁଆଁରୀ",
            "gu": "કુંવારપાઠું",
            "ur": "ایلو ویرا (گھیگوار)",
        }
    },
    {
        "id": "GIN",
        "name": "Ginger",
        "scientific_name": "Zingiber officinale",
        "category_id": "roots",
        "category": "Roots & Rhizomes",
        "icon": "🫚",
        "color": "#D8973C",
        "variety_sample": "Maran / Rio de Janeiro",
        "translations": {
            "en": "Ginger",
            "kn": "ಶುಂಠಿ",
            "te": "అల్లం",
            "hi": "अदरक",
            "ta": "இஞ்சி",
            "ml": "ഇഞ്ചി",
            "mr": "आले",
            "bn": "আদা",
            "pa": "ਅਦਰਕ",
            "or": "ଅଦା",
            "gu": "આદુ",
            "ur": "ادرک",
        }
    },
    {
        "id": "AML",
        "name": "Amla / Indian Gooseberry",
        "scientific_name": "Phyllanthus emblica",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "🍈",
        "color": "#8EB897",
        "variety_sample": "Banarasi / Chakaiya",
        "translations": {
            "en": "Amla / Indian Gooseberry",
            "kn": "ಬೆಟ್ಟದ ನೆಲ್ಲಿಕಾಯಿ",
            "te": "ఉసిరికాయ",
            "hi": "आंवला",
            "ta": "நெல்லிக்காய்",
            "ml": "നെല്ലിക്ക",
            "mr": "आवळा",
            "bn": "আমলকী",
            "pa": "ਔਂਵਲਾ",
            "or": "ଅଁଳା",
            "gu": "આમળાં",
            "ur": "آملہ",
        }
    },
    {
        "id": "MOR",
        "name": "Moringa",
        "scientific_name": "Moringa oleifera",
        "category_id": "herbs",
        "category": "Herbs",
        "icon": "🌿",
        "color": "#2D6A4F",
        "variety_sample": "PKM-1 / ODC-3",
        "translations": {
            "en": "Moringa",
            "kn": "ನುಗ್ಗೆ",
            "te": "మునగ",
            "hi": "सहजन (मोरिंगा)",
            "ta": "முருங்கை",
            "ml": "മുരിങ്ങ",
            "mr": "शेवगा",
            "bn": "সজনে",
            "pa": "ਸੁਹਾਂਜਣਾ",
            "or": "ସଜନା",
            "gu": "સરગવો",
            "ur": "سہانجنا",
        }
    },
    {
        "id": "BRA",
        "name": "Brahmi",
        "scientific_name": "Bacopa monnieri",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "☘️",
        "color": "#3A5A40",
        "variety_sample": "Subodhak / Pragyashakti",
        "translations": {
            "en": "Brahmi",
            "kn": "ಬ್ರಾಹ್ಮೀ",
            "te": "బ్రాహ్మి (సరస్వతీ ఆకు)",
            "hi": "ब्राह्मी",
            "ta": "பிரம்மி",
            "ml": "ബ്രഹ്മി",
            "mr": "ब्राह्मी",
            "bn": "ব্রাহ্মী",
            "pa": "ਬ੍ਰਾਹਮੀ",
            "or": "ବ୍ରାହ୍ମୀ",
            "gu": "બ્રાહ્મી",
            "ur": "براہمی",
        }
    },
    {
        "id": "SHA",
        "name": "Shatavari",
        "scientific_name": "Asparagus racemosus",
        "category_id": "roots",
        "category": "Roots & Rhizomes",
        "icon": "🌿",
        "color": "#95D5B2",
        "variety_sample": "Yellow Shatavari",
        "translations": {
            "en": "Shatavari",
            "kn": "ಶತಾವರಿ",
            "te": "శతావరి",
            "hi": "शतावरी",
            "ta": "சதாவரி",
            "ml": "ശതാവരി",
            "mr": "शतावरी",
            "bn": "শতমূলী",
            "pa": "ਸ਼ਤਾਵਰੀ",
            "or": "ଶତାବରୀ",
            "gu": "શતાવરી",
            "ur": "شتاوری",
        }
    },
    {
        "id": "GIL",
        "name": "Giloy",
        "scientific_name": "Tinospora cordifolia",
        "category_id": "medicinal",
        "category": "Medicinal Plants",
        "icon": "🍃",
        "color": "#588157",
        "variety_sample": "Amrithavalli",
        "translations": {
            "en": "Giloy",
            "kn": "ಅಮೃತಬಳ್ಳಿ",
            "te": "తిప్పతీగ",
            "hi": "गिलोय (गुडुची)",
            "ta": "சீந்தில் கொடி",
            "ml": "ചിറ്റമൃത്",
            "mr": "गुळवेल",
            "bn": "গুলঞ্চ",
            "pa": "ਗਿਲੋਏ",
            "or": "ଗୁଳୁଚି",
            "gu": "ગળો",
            "ur": "گلوئے",
        }
    },
    {
        "id": "LEM",
        "name": "Lemongrass",
        "scientific_name": "Cymbopogon citratus",
        "category_id": "herbs",
        "category": "Herbs",
        "icon": "🌾",
        "color": "#A3B18A",
        "variety_sample": "Krishna / Sugandhi",
        "translations": {
            "en": "Lemongrass",
            "kn": "ನಿಂಬೆ ಹುಲ್ಲು",
            "te": "నిమ్మగడ్డి",
            "hi": "लेमनग्रास (नींबू घास)",
            "ta": "எலுமிச்சை புல்",
            "ml": "വാസനപ്പുല്ല്",
            "mr": "गवती चहा",
            "bn": "লেমনগ্রাস",
            "pa": "ਲੈਮਨਗ੍ਰਾਸ",
            "or": "ଲେମନଗ୍ରାସ",
            "gu": "લીલી ચા",
            "ur": "لیمن گراس",
        }
    },
    {
        "id": "PEP",
        "name": "Peppermint",
        "scientific_name": "Mentha × piperita",
        "category_id": "herbs",
        "category": "Herbs",
        "icon": "🍃",
        "color": "#6096BA",
        "variety_sample": "Menthol Shivalik",
        "translations": {
            "en": "Peppermint",
            "kn": "ಪುದೀನಾ",
            "te": "పుదీనా",
            "hi": "पिपरमिंट (पुदीना)",
            "ta": "புதினா",
            "ml": "പുതിന",
            "mr": "पुदिना",
            "bn": "পিপারমিন্ট (পুদিনা)",
            "pa": "ਪੁਦੀਨਾ",
            "or": "ପୋଦିନା",
            "gu": "ફુદીનો",
            "ur": "پودینہ (پیپرمینٹ)",
        }
    },
    {
        "id": "SEN",
        "name": "Senna",
        "scientific_name": "Senna alexandrina",
        "category_id": "herbs",
        "category": "Herbs",
        "icon": "🌱",
        "color": "#B5838D",
        "variety_sample": "Tinnevelly Senna",
        "translations": {
            "en": "Senna",
            "kn": "ಸೋನಾಮುಖಿ",
            "te": "నేలతంగೇಡು",
            "hi": "सनाय (सेना)",
            "ta": "நிலவாகை",
            "ml": "നിലവാക",
            "mr": "सोनामुखी",
            "bn": "সোনাপাতা",
            "pa": "ਸਨਾਇ",
            "or": "ସୁନାମୁଖୀ",
            "gu": "સોનામુખી",
            "ur": "ثناء مکی",
        }
    },
    {
        "id": "BLP",
        "name": "Black Pepper",
        "scientific_name": "Piper nigrum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "⚫",
        "color": "#3D3A45",
        "variety_sample": "Panniyur-1 / Karimunda",
        "translations": {
            "en": "Black Pepper",
            "kn": "ಕಾಳು ಮೆಣಸು",
            "te": "మిరియాలు",
            "hi": "काली मिर्च",
            "ta": "மிளகு",
            "ml": "കുരുമുളക്",
            "mr": "काळी मिरी",
            "bn": "গোলমরিচ",
            "pa": "ਕਾਲੀ ਮਿਰਚ",
            "or": "ଗୋଲମରିଚ",
            "gu": "કાળા મરી",
            "ur": "کالی مرچ",
        }
    },
    {
        "id": "CAR",
        "name": "Cardamom",
        "scientific_name": "Elettaria cardamomum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "🟢",
        "color": "#4A7C59",
        "variety_sample": "Malabar / Mysore Extra Bold",
        "translations": {
            "en": "Cardamom",
            "kn": "ಏಲಕ್ಕಿ",
            "te": "యాలకులు",
            "hi": "इलायची",
            "ta": "ஏலக்காய்",
            "ml": "ഏലം",
            "mr": "वेलची",
            "bn": "এলাচ",
            "pa": "ਇਲਾਇਚੀ",
            "or": "ଗୁଜୁରାତି / ଅଳେଇଚ",
            "gu": "એલચી",
            "ur": "الائچی",
        }
    },
    {
        "id": "CIN",
        "name": "Cinnamon",
        "scientific_name": "Cinnamomum verum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "🪵",
        "color": "#9C6644",
        "variety_sample": "Navashree Ceylon True",
        "translations": {
            "en": "Cinnamon",
            "kn": "ದಾಲ್ಚಿನ್ನಿ",
            "te": "దాల్చిన చెక్క",
            "hi": "दालचीनी",
            "ta": "இலவங்கப்பட்டை",
            "ml": "കറുവപ്പട്ട",
            "mr": "दालचिनी",
            "bn": "দারুচিনি",
            "pa": "ਦਾਲਚੀਨੀ",
            "or": "ଡାଲଚିନି",
            "gu": "તજ",
            "ur": "دار چینی",
        }
    },
    {
        "id": "CLO",
        "name": "Clove",
        "scientific_name": "Syzygium aromaticum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "🌰",
        "color": "#6F4E37",
        "variety_sample": "Zanzibar Hand-Selected",
        "translations": {
            "en": "Clove",
            "kn": "ಲವಂಗ",
            "te": "లవంగం",
            "hi": "लौंग",
            "ta": "கிராம்பு",
            "ml": "ഗ്രാമ്പൂ",
            "mr": "लवंग",
            "bn": "লবঙ্গ",
            "pa": "ਲੌਂਗ",
            "or": "ଲବଙ୍ଗ",
            "gu": "લવિંગ",
            "ur": "لونگ",
        }
    },
    {
        "id": "COR",
        "name": "Coriander",
        "scientific_name": "Coriandrum sativum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "🌿",
        "color": "#7EA172",
        "variety_sample": "Pant Haritima Seed",
        "translations": {
            "en": "Coriander",
            "kn": "ಕೊತ್ತಂಬರಿ",
            "te": "ధనియాలు",
            "hi": "धनिया",
            "ta": "கொத்தமல்லி",
            "ml": "മല്ലി",
            "mr": "धने",
            "bn": "ধনে",
            "pa": "ਧਨੀਆ",
            "or": "ଧନିଆ",
            "gu": "ધાણા",
            "ur": "دھنیا",
        }
    },
    {
        "id": "FEN",
        "name": "Fenugreek",
        "scientific_name": "Trigonella foenum-graecum",
        "category_id": "spices",
        "category": "Spices",
        "icon": "🟡",
        "color": "#E9C46A",
        "variety_sample": "Pusa Early Bunching",
        "translations": {
            "en": "Fenugreek",
            "kn": "ಮೆಂತ್ಯ",
            "te": "మెంతులు",
            "hi": "मेथी",
            "ta": "வெந்தயம்",
            "ml": "ഉലുവ",
            "mr": "मेथी",
            "bn": "মেথি",
            "pa": "ਮੇਥੀ",
            "or": "ମେଥି",
            "gu": "મેથી",
            "ur": "میتھی",
        }
    },
]

# Indexed lookup maps for performance
CROP_BY_ID = {crop["id"]: crop for crop in CROP_CATALOG}
CROP_BY_NAME = {crop["name"]: crop for crop in CROP_CATALOG}
# Also allow lookup by scientific name or lowercase
CROP_BY_LOWER = {crop["name"].lower(): crop for crop in CROP_CATALOG}
for crop in CROP_CATALOG:
    CROP_BY_LOWER[crop["scientific_name"].lower()] = crop

def get_crop_by_id(crop_id):
    """Retrieve crop metadata by 3-letter ID."""
    return CROP_BY_ID.get(crop_id)

def get_crop_by_name(name):
    """Retrieve crop metadata by common or scientific name."""
    if not name:
        return None
    if name in CROP_BY_NAME:
        return CROP_BY_NAME[name]
    if name.lower() in CROP_BY_LOWER:
        return CROP_BY_LOWER[name.lower()]
    # Check translations
    for crop in CROP_CATALOG:
        if name in crop["translations"].values():
            return crop
    return None

def get_crops_by_category(category_id=None):
    """Filter crops by category id ('roots', 'medicinal', 'herbs', 'spices') or return all."""
    if not category_id or category_id == "all":
        return CROP_CATALOG
    return [c for c in CROP_CATALOG if c["category_id"] == category_id]

def format_crop_display(crop, lang="en", include_category=False):
    """
    Returns prominent farmer-friendly label:
    Icon + Localized Name (English Name if different) — Scientific Name [— Category]
    """
    native_name = crop["translations"].get(lang, crop["name"])
    if lang != "en" and native_name != crop["name"]:
        label = f"{crop['icon']} {native_name} ({crop['name']}) — {crop['scientific_name']}"
    else:
        label = f"{crop['icon']} {crop['name']} — {crop['scientific_name']}"
    if include_category:
        cat_lbl = get_category_label(crop.get("category_id", "all"), lang)
        label += f" [{cat_lbl}]"
    return label

def get_category_label(cat_id, lang="en"):
    """Get localized category label."""
    cat_dict = CATEGORY_TRANSLATIONS.get(cat_id, CATEGORY_TRANSLATIONS["all"])
    return cat_dict.get(lang, cat_dict.get("en", cat_id.title()))

def get_not_listed_label(lang="en"):
    """Get localized 'Not listed? Contact administrator' label."""
    return NOT_LISTED_TRANSLATIONS["label"].get(lang, NOT_LISTED_TRANSLATIONS["label"]["en"])

def get_not_listed_notice(lang="en"):
    """Get localized 'Not listed' onboarding advice notice."""
    return NOT_LISTED_TRANSLATIONS["notice"].get(lang, NOT_LISTED_TRANSLATIONS["notice"]["en"])

def get_crop_color_map():
    """Returns discrete color mapping for Plotly graphs."""
    color_map = {crop["name"]: crop["color"] for crop in CROP_CATALOG}
    # Also add translations
    for crop in CROP_CATALOG:
        for t_name in crop["translations"].values():
            color_map[t_name] = crop["color"]
    return color_map
