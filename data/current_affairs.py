"""
Current Affairs Training Data — Pre-built topic-wise study material
with key facts, one-liners, and MCQs for banking & regulatory exams.
"""

# =============================================================================
# CURRENT AFFAIRS CATEGORIES & TRAINING DATA
# =============================================================================

CURRENT_AFFAIRS_CATEGORIES = {
    "RBI & Monetary Policy": {
        "icon": "🏦",
        "description": "RBI policies, rate changes, regulations, circulars",
        "importance": "Very High",
        "expected_questions": "5-8",
        "color": "#1565C0",
    },
    "Union Budget": {
        "icon": "💰",
        "description": "Annual budget highlights, allocations, tax changes",
        "importance": "Very High",
        "expected_questions": "3-5",
        "color": "#2E7D32",
    },
    "Economic Survey": {
        "icon": "📊",
        "description": "GDP, inflation, fiscal data, key recommendations",
        "importance": "High",
        "expected_questions": "2-4",
        "color": "#F57F17",
    },
    "Banking & Finance": {
        "icon": "🏧",
        "description": "Banking reforms, mergers, NPA, digital banking, regulations",
        "importance": "Very High",
        "expected_questions": "5-8",
        "color": "#6A1B9A",
    },
    "Government Schemes": {
        "icon": "📋",
        "description": "New & modified central/state schemes",
        "importance": "High",
        "expected_questions": "3-5",
        "color": "#00838F",
    },
    "International Organizations": {
        "icon": "🌍",
        "description": "IMF, World Bank, ADB, BRICS, G20, UN bodies",
        "importance": "Medium",
        "expected_questions": "2-3",
        "color": "#BF360C",
    },
    "Appointments & Awards": {
        "icon": "🏆",
        "description": "Key appointments, Padma awards, Nobel, national awards",
        "importance": "Medium",
        "expected_questions": "2-4",
        "color": "#FF6F00",
    },
    "Financial Markets": {
        "icon": "📈",
        "description": "SEBI regulations, stock market, mutual funds, bonds",
        "importance": "High (SEBI/RBI)",
        "expected_questions": "2-5",
        "color": "#1B5E20",
    },
    "Insurance & Pension": {
        "icon": "🛡️",
        "description": "IRDAI, insurance schemes, pension reforms",
        "importance": "Medium",
        "expected_questions": "1-2",
        "color": "#4527A0",
    },
    "Agriculture & Rural": {
        "icon": "🌾",
        "description": "MSP, crop insurance, NABARD, rural development",
        "importance": "High (NABARD)",
        "expected_questions": "3-5",
        "color": "#33691E",
    },
    "External Sector": {
        "icon": "🌐",
        "description": "Trade, FDI, forex reserves, CAD, BOP",
        "importance": "High",
        "expected_questions": "2-3",
        "color": "#0D47A1",
    },
    "Summits & Agreements": {
        "icon": "🤝",
        "description": "G20, BRICS, bilateral summits, trade agreements",
        "importance": "Medium",
        "expected_questions": "1-3",
        "color": "#880E4F",
    },
}


# =============================================================================
# TOPIC-WISE KEY FACTS (One-liners for quick revision)
# =============================================================================

TOPIC_KEY_FACTS = {
    "RBI & Monetary Policy": [
        {"fact": "RBI was established on April 1, 1935 under the RBI Act, 1934", "type": "static"},
        {"fact": "RBI was nationalized in 1949", "type": "static"},
        {"fact": "RBI headquarters: Mumbai (Shahid Bhagat Singh Road)", "type": "static"},
        {"fact": "Current RBI Governor: Sanjay Malhotra (took charge December 11, 2024)", "type": "current"},
        {"fact": "Monetary Policy Committee (MPC) has 6 members — 3 from RBI + 3 external", "type": "static"},
        {"fact": "MPC targets 4% CPI inflation (with +/-2% band i.e., 2%-6%)", "type": "static"},
        {"fact": "Repo Rate is the rate at which RBI lends to commercial banks", "type": "static"},
        {"fact": "Reverse Repo Rate is the rate at which RBI borrows from commercial banks", "type": "static"},
        {"fact": "CRR (Cash Reserve Ratio) — % of deposits banks must keep with RBI as cash", "type": "static"},
        {"fact": "SLR (Statutory Liquidity Ratio) — % of deposits banks must invest in government securities", "type": "static"},
        {"fact": "LAF (Liquidity Adjustment Facility) includes Repo and Reverse Repo", "type": "static"},
        {"fact": "MSF (Marginal Standing Facility) rate is typically Repo Rate + 0.25%", "type": "static"},
        {"fact": "Bank Rate = MSF Rate (for penalty lending)", "type": "static"},
        {"fact": "RBI conducts monetary policy review 6 times a year (bi-monthly)", "type": "static"},
        {"fact": "RBI regulates banks, NBFCs, payment systems, and foreign exchange under FEMA", "type": "static"},
        {"fact": "DICGC (Deposit Insurance) covers deposits up to ₹5 lakh per depositor per bank", "type": "static"},
        {"fact": "Prompt Corrective Action (PCA) framework monitors capital, asset quality & profitability of banks", "type": "static"},
        {"fact": "Digital Rupee (e₹) — CBDC pilot launched by RBI in Dec 2022 (wholesale) and retail", "type": "current"},
        {"fact": "UPI (Unified Payments Interface) — developed by NPCI, regulated by RBI", "type": "static"},
    ],
    "Union Budget": [
        {"fact": "Union Budget is presented on February 1 every year", "type": "static"},
        {"fact": "Article 112 of Constitution — Annual Financial Statement (Union Budget)", "type": "static"},
        {"fact": "Budget has two parts: Revenue Budget and Capital Budget", "type": "static"},
        {"fact": "Fiscal Deficit = Total Expenditure - Total Receipts (excluding borrowing)", "type": "static"},
        {"fact": "Revenue Deficit = Revenue Expenditure - Revenue Receipts", "type": "static"},
        {"fact": "Primary Deficit = Fiscal Deficit - Interest Payments", "type": "static"},
        {"fact": "FRBM Act 2003 — mandates fiscal discipline, targets fiscal deficit at 3% of GDP", "type": "static"},
        {"fact": "Finance Bill is introduced along with the Budget", "type": "static"},
        {"fact": "Budget was merged with Railway Budget from 2017 onwards", "type": "static"},
        {"fact": "Customs duty changes take effect from midnight of Budget day", "type": "static"},
    ],
    "Economic Survey": [
        {"fact": "Economic Survey is presented one day before the Union Budget", "type": "static"},
        {"fact": "Economic Survey is prepared by the Chief Economic Adviser (CEA)", "type": "static"},
        {"fact": "Economic Survey is tabled in both houses of Parliament", "type": "static"},
        {"fact": "India's GDP is measured at both constant prices (real) and current prices (nominal)", "type": "static"},
        {"fact": "GDP at constant prices uses base year 2011-12", "type": "static"},
        {"fact": "NSO (National Statistical Office) releases GDP estimates", "type": "static"},
        {"fact": "CPI (Consumer Price Index) is used for inflation targeting by RBI", "type": "static"},
        {"fact": "WPI (Wholesale Price Index) base year: 2011-12", "type": "static"},
        {"fact": "India's major sectors: Agriculture (~15% GDP), Industry (~25%), Services (~60%)", "type": "static"},
    ],
    "Banking & Finance": [
        {"fact": "SBI is the largest bank in India by assets", "type": "static"},
        {"fact": "PMJDY (PM Jan Dhan Yojana) — launched Aug 28, 2014 for financial inclusion", "type": "static"},
        {"fact": "Basel III norms require banks to maintain minimum CRAR of 9% (India: 11.5% including buffers)", "type": "static"},
        {"fact": "NPA (Non-Performing Asset) — loan overdue for more than 90 days", "type": "static"},
        {"fact": "IBC (Insolvency & Bankruptcy Code) 2016 — resolution framework with NCLT", "type": "static"},
        {"fact": "SARFAESI Act 2002 — allows banks to recover NPAs without court intervention", "type": "static"},
        {"fact": "Small Finance Banks — min paid-up capital ₹200 crore, 75% lending to PSL", "type": "static"},
        {"fact": "Payment Banks — max deposit ₹2 lakh, cannot lend", "type": "static"},
        {"fact": "NBFC regulation transferred fully to RBI from 2019", "type": "static"},
        {"fact": "Priority Sector Lending: 40% of ANBC for domestic banks, 75% for SFBs", "type": "static"},
        {"fact": "NEFT — available 24×7, 365 days (from Dec 2019)", "type": "static"},
        {"fact": "RTGS — real-time, available 24×7 (from Dec 2020), min ₹2 lakh", "type": "static"},
        {"fact": "IMPS — immediate mobile payment, 24×7, up to ₹5 lakh", "type": "static"},
    ],
    "Government Schemes": [
        {"fact": "PM-KISAN — ₹6,000/year to farmer families in 3 installments", "type": "static"},
        {"fact": "MGNREGA — guarantees 100 days of wage employment per rural household", "type": "static"},
        {"fact": "Ayushman Bharat (PM-JAY) — ₹5 lakh health cover per family per year", "type": "static"},
        {"fact": "PM Mudra Yojana — loans up to ₹10 lakh: Shishu (≤50K), Kishore (50K-5L), Tarun (5L-10L)", "type": "static"},
        {"fact": "Atal Pension Yojana — pension of ₹1,000-5,000/month for unorganized sector (18-40 age)", "type": "static"},
        {"fact": "PM Jeevan Jyoti Bima Yojana (PMJJBY) — ₹2 lakh life cover at ₹436/year premium", "type": "static"},
        {"fact": "PM Suraksha Bima Yojana (PMSBY) — ₹2 lakh accidental cover at ₹20/year premium", "type": "static"},
        {"fact": "Stand-Up India — loans ₹10 lakh to ₹1 crore for SC/ST/women entrepreneurs", "type": "static"},
        {"fact": "Start-Up India — launched Jan 2016 for promoting entrepreneurship", "type": "static"},
        {"fact": "PLI (Production Linked Incentive) scheme — 14 key sectors for manufacturing boost", "type": "static"},
        {"fact": "Swachh Bharat Mission launched Oct 2, 2014", "type": "static"},
        {"fact": "Digital India — launched July 1, 2015 for digital infrastructure & governance", "type": "static"},
    ],
    "International Organizations": [
        {"fact": "IMF headquarters: Washington DC | MD: Kristalina Georgieva", "type": "current"},
        {"fact": "World Bank headquarters: Washington DC | President: Ajay Banga", "type": "current"},
        {"fact": "ADB (Asian Development Bank) headquarters: Manila, Philippines", "type": "static"},
        {"fact": "NDB (New Development Bank / BRICS Bank) headquarters: Shanghai", "type": "static"},
        {"fact": "AIIB (Asian Infrastructure Investment Bank) headquarters: Beijing", "type": "static"},
        {"fact": "WTO headquarters: Geneva | DG: Ngozi Okonjo-Iweala", "type": "current"},
        {"fact": "UN headquarters: New York | Secretary-General: Antonio Guterres", "type": "current"},
        {"fact": "BRICS members: Brazil, Russia, India, China, South Africa + Egypt, Ethiopia, Iran, UAE, Saudi Arabia", "type": "current"},
        {"fact": "G20 has 19 countries + EU + African Union", "type": "static"},
        {"fact": "India hosted G20 presidency in 2023 (New Delhi declaration)", "type": "current"},
        {"fact": "SDR (Special Drawing Rights) — IMF's unit of account based on 5 currencies (USD, EUR, CNY, JPY, GBP)", "type": "static"},
        {"fact": "FATF (Financial Action Task Force) — anti-money laundering body, HQ: Paris", "type": "static"},
    ],
    "Financial Markets": [
        {"fact": "SEBI was established April 12, 1988 and given statutory status in 1992", "type": "static"},
        {"fact": "SEBI headquarters: Mumbai", "type": "static"},
        {"fact": "BSE (Bombay Stock Exchange) — oldest in Asia, established 1875, index: SENSEX (30 stocks)", "type": "static"},
        {"fact": "NSE (National Stock Exchange) — established 1992, index: NIFTY 50", "type": "static"},
        {"fact": "FPI (Foreign Portfolio Investors) regulated by SEBI", "type": "static"},
        {"fact": "Mutual Funds regulated by SEBI under MF Regulations, 1996", "type": "static"},
        {"fact": "T+1 settlement cycle implemented in India from Jan 2023", "type": "current"},
        {"fact": "SCORES — SEBI's online complaint redressal system", "type": "static"},
        {"fact": "REITs (Real Estate Investment Trusts) and InvITs regulated by SEBI", "type": "static"},
        {"fact": "Green bonds — SEBI issued framework for green debt securities", "type": "current"},
    ],
    "Agriculture & Rural": [
        {"fact": "MSP (Minimum Support Price) recommended by CACP (Commission for Agricultural Costs & Prices)", "type": "static"},
        {"fact": "MSP is declared for 23 crops each year", "type": "static"},
        {"fact": "PM Fasal Bima Yojana — crop insurance at 2% premium for Kharif, 1.5% for Rabi", "type": "static"},
        {"fact": "NABARD — apex body for rural & agricultural credit, established 1982", "type": "static"},
        {"fact": "NABARD refinances RRBs, cooperative banks, and commercial banks for agri-lending", "type": "static"},
        {"fact": "Kisan Credit Card (KCC) — provides credit for crop production + allied activities", "type": "static"},
        {"fact": "SHG-Bank Linkage Programme — pioneered by NABARD for microfinance", "type": "static"},
        {"fact": "eNAM — electronic National Agriculture Market for online trading of agri-commodities", "type": "static"},
        {"fact": "Soil Health Card Scheme — launched 2015 for soil testing and nutrient recommendations", "type": "static"},
    ],
    "External Sector": [
        {"fact": "CAD (Current Account Deficit) = Trade deficit + Net invisibles", "type": "static"},
        {"fact": "BOP (Balance of Payments) = Current Account + Capital Account + Financial Account", "type": "static"},
        {"fact": "FEMA (Foreign Exchange Management Act) 1999 replaced FERA 1973", "type": "static"},
        {"fact": "FDI routes: Automatic route (no approval) and Government route (approval needed)", "type": "static"},
        {"fact": "ECB (External Commercial Borrowings) governed by RBI guidelines", "type": "static"},
        {"fact": "India's largest trading partner: USA (for goods trade)", "type": "current"},
        {"fact": "India's major exports: Petroleum products, IT services, gems & jewellery, pharma", "type": "static"},
        {"fact": "Forex reserves include: foreign currency assets, gold, SDR, reserve with IMF", "type": "static"},
    ],
    "Appointments & Awards": [
        {"fact": "Bharat Ratna — highest civilian award of India", "type": "static"},
        {"fact": "Padma Awards: Padma Vibhushan > Padma Bhushan > Padma Shri", "type": "static"},
        {"fact": "Nobel Prize categories: Physics, Chemistry, Medicine, Literature, Peace, Economics", "type": "static"},
        {"fact": "Booker Prize — awarded for best novel in English", "type": "static"},
        {"fact": "Arjuna Award — for outstanding sports performance", "type": "static"},
        {"fact": "Rajiv Gandhi Khel Ratna (now Major Dhyan Chand Khel Ratna) — highest sports honour", "type": "static"},
        {"fact": "Dronacharya Award — for outstanding sports coaches", "type": "static"},
    ],
    "Insurance & Pension": [
        {"fact": "IRDAI (Insurance Regulatory & Development Authority of India) — HQ: Hyderabad", "type": "static"},
        {"fact": "LIC — largest life insurer in India, established 1956", "type": "static"},
        {"fact": "FDI limit in insurance sector raised to 74% (from 49%) in Budget 2021", "type": "static"},
        {"fact": "NPS (National Pension System) managed by PFRDA (Pension Fund Regulatory & Development Authority)", "type": "static"},
        {"fact": "EPF (Employees' Provident Fund) managed by EPFO", "type": "static"},
    ],
    "Summits & Agreements": [
        {"fact": "SAARC — South Asian Association for Regional Cooperation (8 members)", "type": "static"},
        {"fact": "ASEAN — 10 Southeast Asian nations, India is dialogue partner", "type": "static"},
        {"fact": "SCO (Shanghai Cooperation Organisation) — India became full member in 2017", "type": "static"},
        {"fact": "Quad — India, USA, Japan, Australia — strategic security dialogue", "type": "static"},
        {"fact": "RCEP — India opted out of this mega trade deal in 2019", "type": "static"},
        {"fact": "Paris Agreement — climate change deal, India pledged net-zero by 2070", "type": "current"},
    ],
}


# =============================================================================
# PRACTICE MCQs — Topic-wise
# =============================================================================

PRACTICE_MCQS = {
    "RBI & Monetary Policy": [
        {
            "question": "The Monetary Policy Committee (MPC) of RBI consists of how many members?",
            "options": ["4", "5", "6", "8"],
            "answer": 2,
            "explanation": "MPC has 6 members — 3 from RBI (Governor as chairperson, Deputy Governor, one RBI officer) and 3 external members nominated by the Government.",
        },
        {
            "question": "Which of the following is NOT a quantitative tool of monetary policy used by RBI?",
            "options": ["CRR", "SLR", "Moral Suasion", "Repo Rate"],
            "answer": 2,
            "explanation": "Moral Suasion is a qualitative/selective tool. CRR, SLR, Repo Rate, Reverse Repo, MSF, Bank Rate are quantitative tools.",
        },
        {
            "question": "DICGC insures deposits up to what amount per depositor per bank?",
            "options": ["₹1 lakh", "₹2 lakh", "₹5 lakh", "₹10 lakh"],
            "answer": 2,
            "explanation": "DICGC covers deposits up to ₹5 lakh per depositor per bank (increased from ₹1 lakh in Feb 2020).",
        },
        {
            "question": "The inflation target for RBI's Monetary Policy Framework is:",
            "options": ["2% +/-1%", "4% +/-2%", "4% +/-1%", "6% +/-2%"],
            "answer": 1,
            "explanation": "RBI targets CPI inflation at 4% with a tolerance band of +/-2% (i.e., 2% to 6%).",
        },
        {
            "question": "Which of the following is the full form of LAF?",
            "options": [
                "Liquidity Adjustment Facility",
                "Loan Assistance Fund",
                "Lending and Finance",
                "Liquid Asset Framework",
            ],
            "answer": 0,
            "explanation": "LAF (Liquidity Adjustment Facility) is a monetary policy tool that allows banks to borrow from RBI (via Repo) or park surplus funds (via Reverse Repo).",
        },
        {
            "question": "Digital Rupee (e₹) is an example of:",
            "options": ["Cryptocurrency", "CBDC", "Stablecoin", "Token Money"],
            "answer": 1,
            "explanation": "Digital Rupee is India's Central Bank Digital Currency (CBDC), issued by RBI. It is legal tender, unlike cryptocurrencies.",
        },
        {
            "question": "Which committee recommended the Monetary Policy Framework with inflation targeting?",
            "options": ["Nachiket Mor Committee", "Urjit Patel Committee", "Raghuram Rajan Committee", "Y.V. Reddy Committee"],
            "answer": 1,
            "explanation": "The Urjit Patel Committee (2014) recommended flexible inflation targeting. This was adopted via amendment to RBI Act in 2016.",
        },
        {
            "question": "The minimum CRR that RBI can prescribe is:",
            "options": ["0%", "3%", "5%", "There is no minimum"],
            "answer": 0,
            "explanation": "After the 2006 amendment to the RBI Act, there is no prescribed minimum or maximum for CRR. RBI can set it between 0% and any level.",
        },
    ],
    "Union Budget": [
        {
            "question": "Under which Article of the Indian Constitution is the Union Budget presented?",
            "options": ["Article 110", "Article 112", "Article 114", "Article 280"],
            "answer": 1,
            "explanation": "Article 112 mandates the Annual Financial Statement (Union Budget) to be laid before the Parliament.",
        },
        {
            "question": "Fiscal Deficit is defined as:",
            "options": [
                "Total Expenditure - Total Revenue",
                "Total Expenditure - Total Receipts (excluding borrowings)",
                "Revenue Expenditure - Revenue Receipts",
                "Total Expenditure - Capital Receipts",
            ],
            "answer": 1,
            "explanation": "Fiscal Deficit = Total Expenditure - Total Receipts excluding borrowings. It represents the total borrowing requirement of the government.",
        },
        {
            "question": "The FRBM Act was enacted in which year?",
            "options": ["2000", "2003", "2005", "2010"],
            "answer": 1,
            "explanation": "The Fiscal Responsibility and Budget Management (FRBM) Act was enacted in 2003 to ensure fiscal discipline.",
        },
        {
            "question": "Railway Budget was merged with the Union Budget from which year?",
            "options": ["2015-16", "2016-17", "2017-18", "2018-19"],
            "answer": 2,
            "explanation": "Based on the recommendation of the Bibek Debroy Committee, Railway Budget was merged with Union Budget from 2017-18.",
        },
        {
            "question": "Primary Deficit equals:",
            "options": [
                "Fiscal Deficit - Interest Payments",
                "Revenue Deficit - Capital Deficit",
                "Total Expenditure - Total Revenue",
                "Fiscal Deficit - Revenue Deficit",
            ],
            "answer": 0,
            "explanation": "Primary Deficit = Fiscal Deficit - Interest Payments. It shows the borrowing requirement excluding interest obligations.",
        },
    ],
    "Banking & Finance": [
        {
            "question": "An asset is classified as NPA if it remains overdue for more than:",
            "options": ["30 days", "60 days", "90 days", "120 days"],
            "answer": 2,
            "explanation": "A Non-Performing Asset (NPA) is a loan where interest or principal is overdue for more than 90 days.",
        },
        {
            "question": "The maximum deposit limit in a Payment Bank is:",
            "options": ["₹1 lakh", "₹2 lakh", "₹5 lakh", "₹10 lakh"],
            "answer": 1,
            "explanation": "Payment Banks can accept deposits up to ₹2 lakh per customer. They cannot issue loans or credit cards.",
        },
        {
            "question": "NEFT is available on:",
            "options": ["Weekdays only", "Weekdays + Saturdays", "24×7, 365 days", "Banking hours only"],
            "answer": 2,
            "explanation": "NEFT operates round the clock (24×7, 365 days) since December 16, 2019.",
        },
        {
            "question": "Priority Sector Lending target for domestic commercial banks is:",
            "options": ["25% of ANBC", "30% of ANBC", "40% of ANBC", "50% of ANBC"],
            "answer": 2,
            "explanation": "Domestic commercial banks must lend 40% of Adjusted Net Bank Credit (ANBC) to priority sectors.",
        },
        {
            "question": "SARFAESI Act was enacted in which year?",
            "options": ["1999", "2002", "2005", "2008"],
            "answer": 1,
            "explanation": "SARFAESI (Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest) Act was enacted in 2002.",
        },
        {
            "question": "Basel III norms require Indian banks to maintain minimum CRAR (including buffers) of:",
            "options": ["8%", "9%", "10.5%", "11.5%"],
            "answer": 3,
            "explanation": "Indian banks need minimum CRAR of 9% + Capital Conservation Buffer of 2.5% = 11.5% (RBI requirement is stricter than Basel III's 10.5%).",
        },
    ],
    "Government Schemes": [
        {
            "question": "Under PM-KISAN, eligible farmers receive how much annual income support?",
            "options": ["₹4,000", "₹5,000", "₹6,000", "₹8,000"],
            "answer": 2,
            "explanation": "PM-KISAN provides ₹6,000 per year in 3 equal installments of ₹2,000 each to eligible farmer families.",
        },
        {
            "question": "Ayushman Bharat (PM-JAY) provides health coverage of:",
            "options": ["₹1 lakh per family", "₹3 lakh per family", "₹5 lakh per family", "₹10 lakh per family"],
            "answer": 2,
            "explanation": "PM-JAY provides ₹5 lakh health coverage per family per year for secondary and tertiary hospitalization.",
        },
        {
            "question": "Under PM Mudra Yojana, 'Kishore' category covers loans of:",
            "options": ["Up to ₹50,000", "₹50,001 to ₹5 lakh", "₹5 lakh to ₹10 lakh", "₹10 lakh to ₹25 lakh"],
            "answer": 1,
            "explanation": "Mudra loan categories: Shishu (up to ₹50,000), Kishore (₹50,001 to ₹5 lakh), Tarun (₹5 lakh to ₹10 lakh).",
        },
        {
            "question": "MGNREGA guarantees how many days of employment per household?",
            "options": ["50 days", "75 days", "100 days", "150 days"],
            "answer": 2,
            "explanation": "MGNREGA guarantees 100 days of wage employment per rural household per financial year.",
        },
    ],
    "International Organizations": [
        {
            "question": "The headquarters of Asian Development Bank (ADB) is located in:",
            "options": ["Tokyo", "Beijing", "Manila", "Jakarta"],
            "answer": 2,
            "explanation": "ADB is headquartered in Manila, Philippines. It was established in 1966.",
        },
        {
            "question": "SDR (Special Drawing Rights) of IMF is based on how many currencies?",
            "options": ["3", "4", "5", "6"],
            "answer": 2,
            "explanation": "SDR basket includes 5 currencies: US Dollar, Euro, Chinese Yuan, Japanese Yen, and British Pound.",
        },
        {
            "question": "FATF is primarily concerned with:",
            "options": ["Trade facilitation", "Climate change", "Anti-money laundering", "Food security"],
            "answer": 2,
            "explanation": "FATF (Financial Action Task Force) sets global standards for combating money laundering and terrorist financing.",
        },
        {
            "question": "New Development Bank (NDB) is also known as:",
            "options": ["Asian Bank", "BRICS Bank", "Global Bank", "Development Bank of Asia"],
            "answer": 1,
            "explanation": "NDB was established by BRICS nations in 2014, headquartered in Shanghai, China.",
        },
    ],
    "Financial Markets": [
        {
            "question": "SEBI was given statutory status in which year?",
            "options": ["1988", "1990", "1992", "1995"],
            "answer": 2,
            "explanation": "SEBI was established in 1988 as an advisory body and given statutory powers through the SEBI Act, 1992.",
        },
        {
            "question": "The current settlement cycle for equity trades in India is:",
            "options": ["T+0", "T+1", "T+2", "T+3"],
            "answer": 1,
            "explanation": "India moved to T+1 settlement cycle from January 2023, meaning trades are settled the next business day.",
        },
        {
            "question": "SENSEX is the benchmark index of which stock exchange?",
            "options": ["NSE", "BSE", "MCX", "CDSL"],
            "answer": 1,
            "explanation": "SENSEX is the benchmark index of BSE (Bombay Stock Exchange) comprising 30 stocks. NIFTY 50 is NSE's benchmark.",
        },
    ],
    "External Sector": [
        {
            "question": "FEMA (Foreign Exchange Management Act) replaced which act?",
            "options": ["FEFA", "FERA", "FERA 1947", "Exchange Control Act"],
            "answer": 1,
            "explanation": "FEMA (1999) replaced FERA (Foreign Exchange Regulation Act, 1973). FEMA is a civil law while FERA was a criminal law.",
        },
        {
            "question": "Which of the following is NOT a component of India's forex reserves?",
            "options": ["Foreign Currency Assets", "Gold", "SDRs", "Government Securities"],
            "answer": 3,
            "explanation": "Forex reserves comprise: Foreign Currency Assets (FCA), Gold, SDRs (Special Drawing Rights), and Reserve Tranche Position with IMF.",
        },
    ],
    "Economic Survey": [
        {
            "question": "Economic Survey is prepared by:",
            "options": ["Finance Minister", "RBI Governor", "Chief Economic Adviser", "NITI Aayog Chairman"],
            "answer": 2,
            "explanation": "The Economic Survey is prepared under the guidance of the Chief Economic Adviser (CEA) in the Ministry of Finance.",
        },
        {
            "question": "The base year currently used for calculating India's GDP is:",
            "options": ["2004-05", "2011-12", "2015-16", "2017-18"],
            "answer": 1,
            "explanation": "India uses 2011-12 as the base year for calculating GDP at constant prices (real GDP).",
        },
        {
            "question": "Which index does RBI use for inflation targeting?",
            "options": ["WPI", "CPI", "GDP Deflator", "SPI"],
            "answer": 1,
            "explanation": "RBI uses CPI (Consumer Price Index) for inflation targeting under the flexible inflation targeting framework.",
        },
    ],
    "Agriculture & Rural": [
        {
            "question": "MSP (Minimum Support Price) is recommended by:",
            "options": ["NABARD", "CACP", "RBI", "NITI Aayog"],
            "answer": 1,
            "explanation": "CACP (Commission for Agricultural Costs and Prices) recommends MSP, which is approved by the Cabinet Committee on Economic Affairs.",
        },
        {
            "question": "NABARD was established in which year?",
            "options": ["1975", "1980", "1982", "1985"],
            "answer": 2,
            "explanation": "NABARD was established on July 12, 1982 based on the recommendation of the B. Sivaraman Committee.",
        },
        {
            "question": "Under PM Fasal Bima Yojana, the premium rate for Kharif crops is:",
            "options": ["1%", "1.5%", "2%", "5%"],
            "answer": 2,
            "explanation": "Premium rates under PMFBY: 2% for Kharif, 1.5% for Rabi crops, and 5% for commercial/horticultural crops.",
        },
    ],
    "Insurance & Pension": [
        {
            "question": "IRDAI is headquartered in:",
            "options": ["Mumbai", "New Delhi", "Hyderabad", "Chennai"],
            "answer": 2,
            "explanation": "IRDAI (Insurance Regulatory and Development Authority of India) is headquartered in Hyderabad.",
        },
        {
            "question": "The current FDI limit in the insurance sector is:",
            "options": ["26%", "49%", "74%", "100%"],
            "answer": 2,
            "explanation": "FDI limit in insurance was raised to 74% from 49% in the Union Budget 2021-22.",
        },
    ],
}


# =============================================================================
# STUDY PLAN TEMPLATES
# =============================================================================

STUDY_PLANS = {
    "RBI Grade B": {
        "Phase 1": {
            "total_weeks": 12,
            "plan": [
                {"week": "1-2", "focus": "Quantitative Aptitude Basics", "topics": "Number System, Percentage, Ratio, Average, SI/CI", "hours_per_day": 3},
                {"week": "3-4", "focus": "Advanced Quant + Reasoning Basics", "topics": "DI, Number Series, Seating Arrangement basics", "hours_per_day": 4},
                {"week": "5-6", "focus": "Reasoning Advanced + English", "topics": "Complex Puzzles, Syllogism, RC, Cloze Test", "hours_per_day": 4},
                {"week": "7-8", "focus": "General Awareness (Static)", "topics": "Banking Awareness, Financial Terms, RBI functions", "hours_per_day": 3},
                {"week": "9-10", "focus": "Current Affairs + Mock Tests", "topics": "Last 6 months CA, Full-length mocks", "hours_per_day": 5},
                {"week": "11-12", "focus": "Revision + Mock Tests", "topics": "Weak areas, 1 mock/day, CA revision", "hours_per_day": 6},
            ],
        },
    },
    "SEBI Grade A": {
        "Paper 1": {
            "total_weeks": 10,
            "plan": [
                {"week": "1-2", "focus": "Quant + Reasoning Foundations", "topics": "DI, Series, Seating, Puzzles", "hours_per_day": 4},
                {"week": "3-4", "focus": "English + GA Basics", "topics": "RC, Cloze, Banking + Capital Markets awareness", "hours_per_day": 4},
                {"week": "5-6", "focus": "SEBI-specific GA", "topics": "Securities market, SEBI regulations, Corporate Governance", "hours_per_day": 4},
                {"week": "7-8", "focus": "Current Affairs", "topics": "Last 6 months CA, focus on financial markets", "hours_per_day": 4},
                {"week": "9-10", "focus": "Mocks + Revision", "topics": "Full-length mocks, weak area focus", "hours_per_day": 5},
            ],
        },
    },
}


def get_ca_categories() -> dict:
    return CURRENT_AFFAIRS_CATEGORIES


def get_key_facts(category: str) -> list[dict]:
    return TOPIC_KEY_FACTS.get(category, [])


def get_practice_mcqs(category: str) -> list[dict]:
    return PRACTICE_MCQS.get(category, [])


def get_all_mcq_count() -> int:
    return sum(len(qs) for qs in PRACTICE_MCQS.values())


def get_study_plan(exam_type: str, phase: str) -> dict | None:
    return STUDY_PLANS.get(exam_type, {}).get(phase)
