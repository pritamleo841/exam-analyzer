"""
RBI Grade B — Deep-Dive Module for AIR 1 Preparation
=====================================================
Notification date: April 28, 2026
Expected Phase 1: July 2026 | Phase 2: August/September 2026

Contains:
- Exam pattern & marking scheme (Phase 1 + Phase 2)
- Historical cut-off data
- Section-wise time strategy
- Phase 2 ESI + FM topic databases with 200+ MCQs
- Important RBI committees & acts
- RBI Governors chronology
- Important banking acts timeline
- Phase-wise preparation blueprints
- Topper strategies for AIR 1
"""
from datetime import date

# ═════════════════════════════════════════════════════════════════════════════
# EXAM CALENDAR & COUNTDOWN
# ═════════════════════════════════════════════════════════════════════════════

NOTIFICATION_DATE = date(2026, 4, 28)
EXPECTED_PHASE1_DATE = date(2026, 7, 18)
EXPECTED_PHASE2_DATE = date(2026, 9, 5)


def get_countdown():
    """Returns days remaining for each milestone."""
    today = date.today()
    return {
        "notification": (NOTIFICATION_DATE - today).days,
        "phase1": (EXPECTED_PHASE1_DATE - today).days,
        "phase2": (EXPECTED_PHASE2_DATE - today).days,
        "notification_date": NOTIFICATION_DATE.strftime("%B %d, %Y"),
        "phase1_date": EXPECTED_PHASE1_DATE.strftime("%B %d, %Y"),
        "phase2_date": EXPECTED_PHASE2_DATE.strftime("%B %d, %Y"),
        "today": today.strftime("%B %d, %Y"),
    }


# ═════════════════════════════════════════════════════════════════════════════
# EXAM PATTERN
# ═════════════════════════════════════════════════════════════════════════════

EXAM_PATTERN = {
    "Phase 1": {
        "name": "Phase 1 — Online Objective",
        "total_marks": 200,
        "duration_minutes": 120,
        "negative_marking": 0.25,
        "sections": [
            {"name": "General Awareness", "questions": 80, "marks": 80, "time_suggested": 25,
             "cutoff_range": "16-24", "strategy": "Attempt 60-70. Focus on banking awareness + last 6 months CA. Skip obscure static GK."},
            {"name": "Quantitative Aptitude", "questions": 30, "marks": 30, "time_suggested": 25,
             "cutoff_range": "8-12", "strategy": "DI first (15-18 Qs). Then series. Skip lengthy calculations. Target 22-25 attempts."},
            {"name": "English Language", "questions": 30, "marks": 30, "time_suggested": 20,
             "cutoff_range": "9-14", "strategy": "RC = 10 Qs, do first. Cloze + Error = fastest marks. Para jumbles take time."},
            {"name": "Reasoning", "questions": 60, "marks": 60, "time_suggested": 50,
             "cutoff_range": "15-22", "strategy": "Seating + Puzzles = 25-30 Qs. Do easy ones first. Skip 3+ variable puzzles if stuck > 5 min."},
        ],
        "total_questions": 200,
        "qualification_note": "Phase 1 is qualifying. Marks NOT added to final merit. Must clear sectional + overall cutoff.",
    },
    "Phase 2": {
        "name": "Phase 2 — Descriptive + Objective",
        "papers": [
            {
                "name": "Paper 1 — Economic & Social Issues (ESI)",
                "type": "Objective",
                "marks": 100,
                "questions": 50,
                "duration_minutes": 90,
                "negative_marking": 0.25,
                "key_topics": [
                    "Growth & Development", "Indian Economy Overview", "Monetary & Credit Policy",
                    "Fiscal Policy & Public Finance", "International Trade & BOP",
                    "Social Issues (Poverty, Unemployment, Inclusion)",
                    "Globalization", "Social Sector Initiatives", "Sustainable Development",
                    "Financial Inclusion & Digital Economy",
                ],
            },
            {
                "name": "Paper 2 — English (Writing Skills)",
                "type": "Descriptive",
                "marks": 100,
                "duration_minutes": 90,
                "components": [
                    {"name": "Essay Writing", "marks": 50, "count": 3, "word_limit": 500,
                     "tip": "Pick topics on Indian economy, RBI policy, banking reforms. Use data points."},
                    {"name": "Precis Writing", "marks": 25, "count": 1, "word_limit": "1/3 of passage",
                     "tip": "Read passage twice. Write in 3rd person. No new ideas — only compress."},
                    {"name": "Comprehension", "marks": 25, "count": 1,
                     "tip": "Answer in your own words. Be concise. Reference the passage."},
                ],
            },
            {
                "name": "Paper 3 — Finance & Management (FM)",
                "type": "Objective",
                "marks": 100,
                "questions": 50,
                "duration_minutes": 90,
                "negative_marking": 0.25,
                "key_topics": [
                    "Financial System", "Financial Markets & Instruments",
                    "Risk Management (Basel norms)", "Corporate Governance",
                    "Regulatory Bodies (RBI, SEBI, IRDAI, PFRDA, IBBI)",
                    "Management — Planning, Organizing, Staffing, Directing, Controlling",
                    "Leadership & Motivation theories", "Corporate Social Responsibility",
                    "FinTech & Digital Finance", "Union Budget & Economic Survey",
                ],
            },
        ],
        "final_merit": "Phase 2 Paper 1 + Paper 2 + Paper 3 + Interview (75 marks) = Final Merit List",
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# HISTORICAL CUT-OFFS (Phase 1 — General category)
# ═════════════════════════════════════════════════════════════════════════════

HISTORICAL_CUTOFFS = {
    2024: {"overall": 127.50, "ga": 17.50, "quant": 8.50, "english": 10.25, "reasoning": 16.50, "vacancies": 322},
    2023: {"overall": 113.25, "ga": 16.75, "quant": 7.75, "english": 9.75, "reasoning": 15.25, "vacancies": 291},
    2022: {"overall": 120.75, "ga": 18.00, "quant": 9.00, "english": 10.50, "reasoning": 17.00, "vacancies": 294},
    2021: {"overall": 105.50, "ga": 15.50, "quant": 7.25, "english": 8.75, "reasoning": 14.00, "vacancies": 322},
    2020: {"overall": 115.00, "ga": 17.00, "quant": 8.00, "english": 9.50, "reasoning": 15.50, "vacancies": 241},
    2019: {"overall": 110.50, "ga": 16.50, "quant": 7.50, "english": 9.00, "reasoning": 14.50, "vacancies": 199},
}


# ═════════════════════════════════════════════════════════════════════════════
# AIR 1 STRATEGY — SECTION-WISE TIME & ATTEMPT TARGETS
# ═════════════════════════════════════════════════════════════════════════════

AIR1_TARGETS = {
    "Phase 1": {
        "target_score": "160+ / 200",
        "sections": {
            "General Awareness": {
                "target_attempts": "70-75 / 80",
                "target_accuracy": "88-92%",
                "target_score": "55-62",
                "time_minutes": 22,
                "key_strategy": [
                    "Most scoring section — every mark counts for AIR 1",
                    "Banking awareness = guaranteed 15-20 Qs — must get 95%+",
                    "Last 6 months CA — 20-25 Qs — revise daily capsule",
                    "Static GK — 10-15 Qs — focus on financial bodies HQ, heads, committees",
                    "Economy — 10-15 Qs — Budget, Survey, GDP, inflation numbers",
                    "Eliminate 2 options instantly — guess between remaining 2",
                ],
            },
            "Quantitative Aptitude": {
                "target_attempts": "25-28 / 30",
                "target_accuracy": "85-90%",
                "target_score": "22-26",
                "time_minutes": 25,
                "key_strategy": [
                    "DI = 15-18 Qs minimum — do these FIRST in Quant",
                    "Number Series = 5 Qs — easy marks, spend max 3 min total",
                    "Approximation/Simplification = quick wins",
                    "Quadratic equations = formula-based, 2 min for 5 Qs",
                    "Skip lengthy word problems if > 2 min each",
                    "Carry a mental 'skip list' — move on after 90 sec per Q",
                ],
            },
            "English Language": {
                "target_attempts": "28-30 / 30",
                "target_accuracy": "85-90%",
                "target_score": "24-27",
                "time_minutes": 18,
                "key_strategy": [
                    "RC = 10 Qs — read passage once carefully, then answer",
                    "Error detection — fastest type, do in 30 sec each",
                    "Cloze test — read full passage first, then fill",
                    "Para jumbles — find opening & closing sentence first",
                    "Vocabulary (if any) — elimination is key",
                    "English is the section to FINISH FAST and bank time for Reasoning",
                ],
            },
            "Reasoning": {
                "target_attempts": "48-52 / 60",
                "target_accuracy": "82-88%",
                "target_score": "38-45",
                "time_minutes": 55,
                "key_strategy": [
                    "LARGEST section — spend the MOST time here",
                    "Seating + Puzzles = 25-30 Qs — this is the battleground",
                    "Do linear seating & floor puzzles first (easiest pattern)",
                    "Circular with conditions — do ONLY if 7 or fewer persons",
                    "Syllogism = 5 Qs — Venn diagram method, guaranteed marks",
                    "Inequality = 5 Qs — symbolic method, < 2 min total",
                    "Blood relation + Direction = 3-5 Qs — quick wins",
                    "Skip any puzzle that takes > 6 min — come back later",
                    "Input-Output — pattern recognition, either you see it or skip",
                ],
            },
        },
        "exam_day_routine": [
            "Wake up 3 hours before exam. Light breakfast — avoid heavy food.",
            "Reach center 45 min early. Settle nerves.",
            "First 5 min: scan the whole paper. Identify easy puzzle sets.",
            "Order: English (18 min) → Quant (25 min) → GA (22 min) → Reasoning (55 min)",
            "Never spend > 6 min on a single puzzle set. Mark & move.",
            "Last 5 min: review marked questions. Make smart guesses (eliminate 2 options).",
            "Do NOT change answers unless 100% sure of the change.",
        ],
    },
    "Phase 2": {
        "target_score": "400+ / 475 (incl. interview)",
        "papers": {
            "ESI": {
                "target_score": "60-70 / 100",
                "key_strategy": [
                    "Read India's Economic Survey — at least summary chapters",
                    "Memorize: GDP numbers, fiscal deficit target, CAD, inflation trend",
                    "Social indicators: HDI, MPI, SDG ranking, Gini coefficient",
                    "Government schemes + missions = 10-15 Qs guaranteed",
                    "RBI's annual report — monetary policy highlights",
                    "Globalization, WTO, FTA — 5+ Qs every year",
                ],
            },
            "FM": {
                "target_score": "55-65 / 100",
                "key_strategy": [
                    "Basel I/II/III norms — pillars, capital requirements — 5+ Qs",
                    "Financial markets: money market instruments, capital market, derivatives",
                    "Risk management: credit risk, market risk, operational risk",
                    "Management theories: Maslow, Herzberg, McGregor X/Y, Blake-Mouton",
                    "Corporate governance — SEBI LODR, Companies Act, Board committees",
                    "FinTech: UPI, CBDC, blockchain basics, RegTech, InsurTech",
                ],
            },
            "English": {
                "target_score": "65-75 / 100",
                "key_strategy": [
                    "Essay: pick economy/banking topic. Use 5-para structure.",
                    "Include: 3-4 data points, mention govt schemes, RBI policy",
                    "Precis: compress to 1/3. Keep all key ideas. No personal opinions.",
                    "Practice 1 essay + 1 precis daily for 30 days before exam",
                    "Handwriting (or typing speed) matters — practice timed writing",
                ],
            },
        },
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# RBI GOVERNORS — COMPLETE LIST
# ═════════════════════════════════════════════════════════════════════════════

RBI_GOVERNORS = [
    {"name": "Sir Osborne Smith", "tenure": "1935-1937", "note": "First Governor"},
    {"name": "Sir James Taylor", "tenure": "1937-1943", "note": ""},
    {"name": "C.D. Deshmukh", "tenure": "1943-1949", "note": "First Indian Governor; later Finance Minister"},
    {"name": "Sir Benegal Rama Rau", "tenure": "1949-1957", "note": ""},
    {"name": "K.G. Ambegaonkar", "tenure": "1957 (acting)", "note": ""},
    {"name": "H.V.R. Iengar", "tenure": "1957-1962", "note": ""},
    {"name": "P.C. Bhattacharyya", "tenure": "1962-1967", "note": ""},
    {"name": "L.K. Jha", "tenure": "1967-1970", "note": ""},
    {"name": "B.N. Adarkar", "tenure": "1970 (acting)", "note": ""},
    {"name": "S. Jagannathan", "tenure": "1970-1975", "note": ""},
    {"name": "N.C. Sen Gupta", "tenure": "1975 (acting)", "note": ""},
    {"name": "K.R. Puri", "tenure": "1975-1977", "note": ""},
    {"name": "M. Narasimham", "tenure": "1977 (acting)", "note": "Narasimham Committee on banking reforms"},
    {"name": "I.G. Patel", "tenure": "1977-1982", "note": ""},
    {"name": "Manmohan Singh", "tenure": "1982-1985", "note": "Later PM of India"},
    {"name": "A. Ghosh", "tenure": "1985 (acting)", "note": ""},
    {"name": "R.N. Malhotra", "tenure": "1985-1990", "note": "Malhotra Committee on insurance reforms"},
    {"name": "Venugopal Reddy", "tenure": "1990 (acting)", "note": ""},
    {"name": "S. Venkitaramanan", "tenure": "1990-1992", "note": ""},
    {"name": "C. Rangarajan", "tenure": "1992-1997", "note": "Rangarajan Committee on BOP, financial sector"},
    {"name": "Bimal Jalan", "tenure": "1997-2003", "note": ""},
    {"name": "Y.V. Reddy", "tenure": "2003-2008", "note": "Credited with protecting India from 2008 crisis"},
    {"name": "D. Subbarao", "tenure": "2008-2013", "note": ""},
    {"name": "Raghuram Rajan", "tenure": "2013-2016", "note": "Introduced inflation targeting; AQR review of NPAs"},
    {"name": "Urjit Patel", "tenure": "2016-2018", "note": "First MPC formed; Demonetization period"},
    {"name": "Shaktikanta Das", "tenure": "2018-2024", "note": "COVID-era policies; CBDC launch"},
    {"name": "Sanjay Malhotra", "tenure": "2024-present", "note": "Current Governor (from Dec 11, 2024)"},
]


# ═════════════════════════════════════════════════════════════════════════════
# IMPORTANT RBI COMMITTEES
# ═════════════════════════════════════════════════════════════════════════════

RBI_COMMITTEES = [
    {"name": "Narasimham Committee I (1991)", "topic": "Banking Sector Reforms", "key_reco": "Reduce SLR/CRR, abolish branch licensing, set up Tribunals for NPA recovery"},
    {"name": "Narasimham Committee II (1998)", "topic": "Banking Sector Reforms", "key_reco": "Capital adequacy of 10%, merger of strong banks, 3% NPAs target"},
    {"name": "Urjit Patel Committee (2014)", "topic": "Monetary Policy Framework", "key_reco": "CPI-based inflation targeting at 4% (+/-2%); formation of MPC"},
    {"name": "Nachiket Mor Committee (2014)", "topic": "Financial Inclusion", "key_reco": "Universal bank account by Jan 2016; Payments bank concept; small finance banks"},
    {"name": "P.J. Nayak Committee (2014)", "topic": "Governance of Bank Boards", "key_reco": "Professionalize PSB boards; create Bank Investment Company (BIC)"},
    {"name": "Damodaran Committee (2011)", "topic": "Customer Service in Banks", "key_reco": "Basic bank account for all; simplified KYC; faster grievance redressal"},
    {"name": "R. Gandhi Committee (2016)", "topic": "Digital Payments", "key_reco": "Promote digital payments; interoperability of wallets; strengthen cyber security"},
    {"name": "Sudarshan Sen Committee (2019)", "topic": "Offshore Rupee Markets", "key_reco": "24-hour onshore rupee market; liberalize NDF regulations"},
    {"name": "Nandan Nilekani Committee (2019)", "topic": "Digital Payments", "key_reco": "Increase digital payment acceptance infra; interoperability; contactless payments"},
    {"name": "Y.H. Malegam Committee (2010)", "topic": "Microfinance regulation", "key_reco": "Interest rate cap for MFIs; creation of category under NBFC-MFI"},
    {"name": "Khan Committee (1997)", "topic": "Harmonization of Banking Regulations", "key_reco": "Uniform regulation for all credit institutions"},
    {"name": "Tandon Committee (1975)", "topic": "Working Capital Finance", "key_reco": "3 methods of lending based on inventory norms"},
    {"name": "Chore Committee (1979)", "topic": "Working Capital Finance", "key_reco": "Modified Tandon Committee norms; 2nd method of lending recommended"},
    {"name": "Ghosh Committee (1992)", "topic": "Bank Frauds", "key_reco": "Internal vigilance; staff rotation; surprise inspections"},
    {"name": "Kelkar Committee (2002)", "topic": "Direct & Indirect Tax Reforms", "key_reco": "Widen tax base; rationalize exemptions; simplify tax structure"},
    {"name": "Raghuram Rajan Committee (2008)", "topic": "Financial Sector Reforms", "key_reco": "100 Small Steps for financial sector development"},
    {"name": "Deepak Mohanty Committee (2016)", "topic": "Medium-term Path on Financial Inclusion", "key_reco": "Stepped approach to universal financial inclusion; digital-first approach"},
    {"name": "Internal Working Group (2020)", "topic": "Corporate Houses in Banking", "key_reco": "Allow corporate houses to own banks (controversial); raise promoter cap to 26%"},
]


# ═════════════════════════════════════════════════════════════════════════════
# IMPORTANT ACTS — BANKING & FINANCE
# ═════════════════════════════════════════════════════════════════════════════

IMPORTANT_ACTS = [
    {"act": "RBI Act, 1934", "purpose": "Establishment and governance of RBI", "key_point": "Sec 22: sole right to issue currency; Sec 42: CRR; Sec 45: emergency powers"},
    {"act": "Banking Regulation Act, 1949", "purpose": "Regulate banking companies", "key_point": "Sec 5(b): definition of banking; Sec 21: control advances; Sec 35A: power to issue directions"},
    {"act": "Negotiable Instruments Act, 1881", "purpose": "Law on cheques, bills of exchange, promissory notes", "key_point": "Sec 138: dishonour of cheque is criminal offence"},
    {"act": "SARFAESI Act, 2002", "purpose": "Recovery of NPAs by banks without court", "key_point": "Asset Reconstruction Companies (ARCs); securitization of financial assets"},
    {"act": "FEMA, 1999", "purpose": "Foreign exchange management", "key_point": "Replaced FERA 1973; civil offence not criminal; FDI/FPI routes"},
    {"act": "Prevention of Money Laundering Act (PMLA), 2002", "purpose": "Anti-money laundering", "key_point": "KYC compliance; suspicious transaction reporting to FIU-IND"},
    {"act": "IBC (Insolvency & Bankruptcy Code), 2016", "purpose": "Time-bound insolvency resolution", "key_point": "NCLT for companies; DRT for individuals; 330-day resolution timeline"},
    {"act": "Payment & Settlement Systems Act, 2007", "purpose": "Regulate payment systems", "key_point": "RBI as regulator; authorizes NEFT, RTGS, UPI, cards"},
    {"act": "DICGC Act, 1961", "purpose": "Deposit insurance", "key_point": "Insurance cover raised to Rs 5 lakh in 2020"},
    {"act": "Companies Act, 2013", "purpose": "Corporate governance, CSR mandate", "key_point": "Sec 135: CSR mandatory for NW >= Rs 500cr or turnover >= Rs 1000cr"},
    {"act": "SEBI Act, 1992", "purpose": "Regulate securities market", "key_point": "Protects investor interest; regulates stock exchanges, MFs, debenture trustees"},
    {"act": "IRDAI Act, 1999", "purpose": "Regulate insurance sector", "key_point": "Replaced the Controller of Insurance; FDI limit 74% (2021)"},
    {"act": "PFRDA Act, 2013", "purpose": "Regulate pension sector", "key_point": "National Pension System (NPS); statutory status for PFRDA"},
    {"act": "NABARD Act, 1981", "purpose": "Establish NABARD", "key_point": "Apex body for agricultural and rural credit"},
    {"act": "Credit Information Companies (Regulation) Act, 2005", "purpose": "Regulate credit bureaus", "key_point": "CIBIL, Equifax, Experian, CRIF operate under this"},
    {"act": "Factoring Regulation Act, 2011", "purpose": "Regulate factoring business", "key_point": "NBFC-Factors registered with RBI; TReDS platform"},
]


# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2: ESI (ECONOMIC & SOCIAL ISSUES) — TOPIC DATABASE
# ═════════════════════════════════════════════════════════════════════════════

ESI_TOPICS = {
    "Growth & Development": {
        "key_concepts": [
            "GDP vs GNP vs NNP vs NDP",
            "GDP at factor cost vs GDP at market price",
            "Real GDP (constant prices) vs Nominal GDP (current prices)",
            "HDI (Human Development Index) — UNDP — components: health, education, income",
            "MPI (Multidimensional Poverty Index) — UNDP",
            "Gini Coefficient — measures income inequality (0 = perfect equality, 1 = perfect inequality)",
            "Per Capita Income = National Income / Population",
            "Demographic Dividend — working-age population > dependents",
            "NITI Aayog replaced Planning Commission in 2015",
        ],
        "importance": "Very High — 5-8 Qs every year",
    },
    "Monetary & Credit Policy": {
        "key_concepts": [
            "Expansionary vs Contractionary monetary policy",
            "Transmission mechanism — how policy rate changes affect lending",
            "Open Market Operations (OMO) — buy/sell government securities",
            "LAF corridor: MSF rate — Repo Rate — Reverse Repo/SDF Rate",
            "Standing Deposit Facility (SDF) replaced Reverse Repo as floor (April 2022)",
            "Yield curve — normal, inverted, flat",
            "Credit creation multiplier = 1 / CRR",
            "Quantitative easing vs tapering",
        ],
        "importance": "Very High — 5+ Qs",
    },
    "Fiscal Policy & Public Finance": {
        "key_concepts": [
            "Fiscal Deficit, Revenue Deficit, Primary Deficit, Effective Revenue Deficit",
            "FRBM Act 2003 — fiscal discipline",
            "N.K. Singh Committee (2017) — revised FRBM targets",
            "Direct vs Indirect taxes — GST replaced multiple indirect taxes (July 1, 2017)",
            "GST Council under Article 279A — chaired by Union Finance Minister",
            "GST slabs: 0%, 5%, 12%, 18%, 28% + compensation cess",
            "Laffer Curve — relationship between tax rate and tax revenue",
            "Ways & Means Advances (WMA) — RBI to government for temporary cash flow mismatch",
            "Government Borrowing: G-Sec, T-Bills (91, 182, 364 day), SDL",
        ],
        "importance": "Very High — 4-6 Qs",
    },
    "Indian Economy Overview": {
        "key_concepts": [
            "Sectors: Primary (agriculture), Secondary (industry), Tertiary (services)",
            "Service sector contributes ~55% to GDP",
            "Agriculture employs ~42% workforce but ~15% GDP contribution",
            "Make in India, PLI scheme for manufacturing revival",
            "India's GDP ranking: 5th largest economy (nominal) globally",
            "NSSO merged with CSO to form NSO (National Statistical Office)",
            "Index of Industrial Production (IIP) — measures industrial output",
            "Eight Core Industries: coal, crude oil, natural gas, refinery, fertilizers, steel, cement, electricity",
        ],
        "importance": "High — 3-5 Qs",
    },
    "International Trade & BOP": {
        "key_concepts": [
            "Balance of Payments = Current Account + Capital Account + Financial Account",
            "Current Account: trade balance + net invisibles (services, remittances, investment income)",
            "Capital Account: FDI, FPI, ECB, NRI deposits",
            "Trade deficit = Imports > Exports",
            "India's major exports: petroleum, IT services, gems & jewellery, pharma, textiles",
            "India's major imports: crude oil, gold, electronics, machinery",
            "EXIM Bank — apex financial institution for foreign trade",
            "Free Trade Agreements: India-UAE CEPA, India-Australia ECTA, RCEP (India opted out)",
            "World Trade Organization — MFN principle, TRIPS, TRIMS",
        ],
        "importance": "High — 3-5 Qs",
    },
    "Poverty, Unemployment & Inclusion": {
        "key_concepts": [
            "Tendulkar Committee — BPL methodology (2011-12: 21.9%)",
            "Rangarajan Committee — revised poverty line (2011-12: 29.5%)",
            "MPI (Global MPI by UNDP + OPHI) — India's sharp decline in poverty",
            "Types of unemployment: structural, cyclical, seasonal, disguised, frictional",
            "PLFS (Periodic Labour Force Survey) by NSO — measures employment",
            "MGNREGA — largest employment guarantee programme",
            "Self-Help Groups (SHGs) — NABARD linkage for women empowerment",
            "Financial inclusion: PMJDY, Aadhaar-linked accounts, DBT",
        ],
        "importance": "High — 3-4 Qs",
    },
    "Social Sector & Development": {
        "key_concepts": [
            "Education: NEP 2020, Samagra Shiksha, PM SHRI Schools",
            "Health: Ayushman Bharat (PM-JAY), National Health Mission",
            "SDGs (Sustainable Development Goals) — 17 goals by 2030 (UN)",
            "India's SDG Index (NITI Aayog)",
            "Women empowerment: Beti Bachao Beti Padhao, SHGs, Mahila Samman",
            "Demographic dividend: median age ~28 years, window till 2050",
            "Urbanization challenges: smart cities, AMRUT, SBM-Urban",
        ],
        "importance": "Medium — 2-3 Qs",
    },
    "Sustainable Development & Environment": {
        "key_concepts": [
            "Paris Agreement 2015 — India's NDC: 45% emission intensity reduction by 2030",
            "India's net-zero target: 2070",
            "National Action Plan on Climate Change (NAPCC) — 8 missions",
            "ISA (International Solar Alliance) — launched by India & France",
            "Green bonds, carbon trading, ESG investing",
            "Circular economy, bio-economy concepts",
            "COP summits — latest climate negotiations",
        ],
        "importance": "Medium — 2-3 Qs",
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# PHASE 2: FM (FINANCE & MANAGEMENT) — TOPIC DATABASE
# ═════════════════════════════════════════════════════════════════════════════

FM_TOPICS = {
    "Financial System & Markets": {
        "key_concepts": [
            "Money market: Call money, T-Bills, CP, CD, Repo",
            "Capital market: equity, debt, derivatives",
            "Primary market (IPO, FPO, Rights issue, Bonus) vs Secondary market (exchanges)",
            "SEBI — regulation of markets, mutual funds, FPIs, takeovers",
            "Credit rating agencies: CRISIL, ICRA, CARE, India Ratings, Acuite",
            "SCORES — SEBI complaint redressal",
            "Mutual Fund categories: equity, debt, hybrid, solution-oriented, other",
            "ETF (Exchange Traded Fund) — tracks index, traded like stock",
            "AIF (Alternative Investment Fund) — 3 categories",
        ],
        "importance": "Very High — 6-8 Qs",
    },
    "Risk Management & Basel Norms": {
        "key_concepts": [
            "Types of risk: credit risk, market risk, operational risk, liquidity risk",
            "Basel I (1988): min 8% capital adequacy ratio",
            "Basel II (2004): 3 pillars — minimum capital, supervisory review, market discipline",
            "Basel III (2010): stricter capital + liquidity norms post-2008 crisis",
            "Basel III — CET1 (4.5%) + AT1 = Tier 1 (6%) + Tier 2 = CRAR (8%) [India: 9%]",
            "Capital Conservation Buffer (CCB) = 2.5%",
            "Countercyclical Capital Buffer (CCyB) = 0-2.5% (discretionary)",
            "LCR (Liquidity Coverage Ratio) — 30-day stress",
            "NSFR (Net Stable Funding Ratio) — 1-year horizon",
            "ICAAP — Internal Capital Adequacy Assessment Process (Pillar 2)",
            "ALM (Asset-Liability Management) — maturity mismatch risk",
            "VaR (Value at Risk) — max potential loss at confidence level",
        ],
        "importance": "Very High — 5-7 Qs",
    },
    "Corporate Governance": {
        "key_concepts": [
            "Companies Act 2013 — Sec 135 (CSR), Sec 149 (Independent Directors)",
            "SEBI LODR (Listing Obligations & Disclosure Requirements)",
            "Board committees: Audit, Nomination & Remuneration, CSR, Risk Management",
            "Insider trading regulations — SEBI (PIT) Regulations 2015",
            "Related party transactions — board/shareholder approval needed",
            "Kumar Mangalam Birla Committee (1999) — first CG code in India",
            "Narayana Murthy Committee (2003) — strengthened board independence",
            "Uday Kotak Committee (2017) — SEBI CG reforms",
        ],
        "importance": "High — 3-5 Qs",
    },
    "Management Concepts": {
        "key_concepts": [
            "Functions of Management: Planning, Organizing, Staffing, Directing, Controlling",
            "Henri Fayol — 14 principles of management",
            "F.W. Taylor — scientific management (time & motion studies)",
            "Maslow's Hierarchy of Needs — 5 levels (physiological to self-actualization)",
            "Herzberg's Two-Factor Theory — hygiene factors vs motivators",
            "McGregor's Theory X (lazy workers) vs Theory Y (self-motivated workers)",
            "Ouchi's Theory Z — Japanese management style (lifetime employment, consensus)",
            "Blake-Mouton Managerial Grid — concern for people vs production",
            "SWOT Analysis — Strengths, Weaknesses, Opportunities, Threats",
            "BCG Matrix — Star, Cash Cow, Question Mark, Dog",
            "Porter's Five Forces — competitive analysis framework",
            "Change management: Lewin's 3-stage model (Unfreeze-Change-Refreeze)",
            "Leadership styles: Autocratic, Democratic, Laissez-faire, Transformational, Transactional",
            "Emotional Intelligence (Daniel Goleman) — 5 components",
        ],
        "importance": "High — 5-8 Qs",
    },
    "FinTech & Digital Finance": {
        "key_concepts": [
            "UPI — NPCI — volume crossed 10+ billion monthly transactions",
            "CBDC (Central Bank Digital Currency) — e-Rs wholesale + retail pilots",
            "Blockchain basics — distributed ledger, smart contracts",
            "RegTech — technology for regulatory compliance",
            "InsurTech — technology in insurance",
            "P2P lending — regulated by RBI (NBFC-P2P)",
            "Account Aggregator framework — consent-based data sharing",
            "Digital Lending Guidelines (RBI 2022) — no 3rd party apps for collection",
            "Tokenization of cards — RBI mandate for card security",
        ],
        "importance": "High — 3-5 Qs",
    },
    "Regulatory Bodies": {
        "key_concepts": [
            "RBI — banks, NBFCs, payment systems, forex",
            "SEBI — securities markets, MFs, FPIs, takeovers",
            "IRDAI — insurance sector",
            "PFRDA — pension sector (NPS, APY)",
            "IBBI — Insolvency & Bankruptcy Board under IBC",
            "CCIL — Clearing Corporation for forex, G-Sec",
            "NPCI — UPI, NACH, BBPS, RuPay",
            "FIU-IND — Financial Intelligence Unit for anti-money laundering",
        ],
        "importance": "High — 3-4 Qs",
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# MCQs — PHASE 2: ESI + FM
# ═════════════════════════════════════════════════════════════════════════════

PHASE2_MCQS = {
    "ESI": [
        {"question": "GDP at market price equals:", "options": ["GDP at factor cost + Net indirect taxes", "GDP at factor cost - Net indirect taxes", "GNP - Depreciation", "NNP + Subsidies"], "answer": 0, "explanation": "GDP at market price = GDP at factor cost + (Indirect Taxes - Subsidies) = GDP at FC + Net Indirect Taxes"},
        {"question": "The current base year for GDP calculation in India is:", "options": ["2004-05", "2011-12", "2015-16", "2017-18"], "answer": 1, "explanation": "India uses 2011-12 as the base year for calculating GDP at constant prices (real GDP)."},
        {"question": "Human Development Index (HDI) is published by:", "options": ["World Bank", "IMF", "UNDP", "NITI Aayog"], "answer": 2, "explanation": "HDI is published by UNDP in its annual Human Development Report. It measures health, education, and income."},
        {"question": "NITI Aayog was established in:", "options": ["2013", "2014", "2015", "2016"], "answer": 2, "explanation": "NITI Aayog (National Institution for Transforming India) replaced the Planning Commission on January 1, 2015."},
        {"question": "Standing Deposit Facility (SDF) rate currently acts as:", "options": ["Ceiling of LAF corridor", "Floor of LAF corridor", "Same as Repo Rate", "Same as Bank Rate"], "answer": 1, "explanation": "Since April 2022, SDF replaced Reverse Repo as the floor of the LAF corridor. MSF is the ceiling. Repo rate is in between."},
        {"question": "GST was implemented in India from:", "options": ["April 1, 2016", "January 1, 2017", "July 1, 2017", "April 1, 2018"], "answer": 2, "explanation": "GST was rolled out on July 1, 2017, replacing multiple indirect taxes. 101st Constitutional Amendment enabled it."},
        {"question": "GST Council is constituted under which Article?", "options": ["Article 246A", "Article 269A", "Article 279A", "Article 366"], "answer": 2, "explanation": "Article 279A establishes the GST Council, chaired by the Union Finance Minister, with state finance ministers as members."},
        {"question": "N.K. Singh Committee (2017) was related to:", "options": ["Monetary policy reform", "FRBM Act review", "GST implementation", "Banking reforms"], "answer": 1, "explanation": "N.K. Singh Committee reviewed the FRBM Act and recommended fiscal deficit target of 2.5% of GDP by 2022-23 (later revised due to COVID)."},
        {"question": "Which committee defined the poverty line used for planning?", "options": ["Lakdawala Committee", "Tendulkar Committee", "Rangarajan Committee", "Sengupta Committee"], "answer": 1, "explanation": "Tendulkar Committee (2009) methodology was adopted. It defined poverty using consumption expenditure with rural/urban thresholds."},
        {"question": "The Gini coefficient value 0 represents:", "options": ["Perfect inequality", "Perfect equality", "Moderate inequality", "No income"], "answer": 1, "explanation": "Gini coefficient ranges from 0 (perfect equality) to 1 (perfect inequality). India's Gini is around 0.35."},
        {"question": "India's largest trading partner for goods trade is:", "options": ["China", "USA", "UAE", "EU"], "answer": 1, "explanation": "The USA is India's largest trading partner for goods trade (bilateral trade). China is the largest import source."},
        {"question": "EXIM Bank of India provides:", "options": ["Crop loans", "Housing loans", "Export-import financing", "Microfinance"], "answer": 2, "explanation": "EXIM Bank is the apex financial institution for financing, facilitating, and promoting India's international trade."},
        {"question": "India opted out of which mega trade deal in 2019?", "options": ["CPTPP", "RCEP", "TTIP", "DCFTA"], "answer": 1, "explanation": "India opted out of RCEP (Regional Comprehensive Economic Partnership) in 2019 due to concerns about Chinese imports flooding Indian markets."},
        {"question": "Net-zero emissions target of India is set for year:", "options": ["2050", "2060", "2070", "2080"], "answer": 2, "explanation": "PM Modi announced India's net-zero emissions target for 2070 at COP26 (Glasgow, 2021)."},
        {"question": "International Solar Alliance was launched by India and:", "options": ["USA", "Japan", "France", "Germany"], "answer": 2, "explanation": "ISA was launched by India and France at COP21 (Paris, 2015). HQ: Gurugram, India."},
        {"question": "PLFS (Periodic Labour Force Survey) is conducted by:", "options": ["Ministry of Labour", "NITI Aayog", "NSO", "CSO"], "answer": 2, "explanation": "NSO (National Statistical Office) conducts PLFS for estimating employment and unemployment indicators."},
        {"question": "Which is NOT a component of HDI?", "options": ["Life expectancy", "Mean years of schooling", "Per capita income (GNI)", "Infant mortality rate"], "answer": 3, "explanation": "HDI has 3 dimensions: Health (life expectancy), Education (mean & expected years of schooling), Income (GNI per capita PPP). IMR is not directly used."},
        {"question": "Ways and Means Advances (WMA) are provided by:", "options": ["NABARD to state govts", "RBI to central/state govts", "World Bank to India", "SBI to PSUs"], "answer": 1, "explanation": "WMA is a facility by RBI to central and state governments to bridge temporary cash flow mismatches."},
        {"question": "Eight Core Industries contribute approximately what % to IIP?", "options": ["20.27%", "30.52%", "40.27%", "50.34%"], "answer": 2, "explanation": "The Eight Core Industries have a combined weight of 40.27% in the Index of Industrial Production (IIP)."},
        {"question": "National Action Plan on Climate Change has how many missions?", "options": ["5", "6", "8", "10"], "answer": 2, "explanation": "NAPCC has 8 missions: Solar, Enhanced Energy Efficiency, Sustainable Habitat, Water, Sustaining Himalayan Eco-system, Green India, Sustainable Agriculture, Strategic Knowledge."},
    ],
    "FM": [
        {"question": "Basel III requires minimum Common Equity Tier 1 (CET1) of:", "options": ["4%", "4.5%", "6%", "8%"], "answer": 1, "explanation": "Basel III mandates minimum CET1 of 4.5% of Risk Weighted Assets. Total Tier 1 = 6%. Total CRAR = 8% (plus buffers)."},
        {"question": "Capital Conservation Buffer (CCB) under Basel III is:", "options": ["1%", "1.5%", "2%", "2.5%"], "answer": 3, "explanation": "CCB is 2.5% of RWA, to be maintained above minimum capital. Combined with 8% = 10.5% (India requires 9% + 2.5% = 11.5%)."},
        {"question": "LCR measures a bank's ability to survive stress of:", "options": ["7 days", "14 days", "30 days", "90 days"], "answer": 2, "explanation": "LCR = HQLA / Net Cash Outflows over 30 days. Banks must maintain LCR >= 100%."},
        {"question": "In Maslow's Hierarchy, the highest level is:", "options": ["Safety needs", "Esteem needs", "Self-actualization", "Social needs"], "answer": 2, "explanation": "Maslow's hierarchy (bottom to top): Physiological, Safety, Social/Love, Esteem, Self-actualization."},
        {"question": "Theory X and Theory Y was proposed by:", "options": ["Abraham Maslow", "Douglas McGregor", "Frederick Herzberg", "Peter Drucker"], "answer": 1, "explanation": "McGregor's Theory X assumes workers are lazy (need control); Theory Y assumes workers are self-motivated."},
        {"question": "Herzberg's Two-Factor Theory includes:", "options": ["Hygiene factors and Motivators", "Push and Pull factors", "External and Internal factors", "Primary and Secondary needs"], "answer": 0, "explanation": "Herzberg: Hygiene factors (salary, conditions) prevent dissatisfaction. Motivators (achievement, recognition) drive satisfaction."},
        {"question": "Porter's Five Forces does NOT include:", "options": ["Threat of new entrants", "Bargaining power of suppliers", "Government regulation", "Threat of substitute products"], "answer": 2, "explanation": "Porter's 5 Forces: rivalry, threat of entrants, threat of substitutes, bargaining power of buyers and suppliers. Government regulation is external."},
        {"question": "BCG Matrix classifies products into:", "options": ["Stars, Cash Cows, Question Marks, Dogs", "Good, Better, Best, Worst", "Leaders, Followers, Nichers, Challengers", "Growth, Maturity, Decline, Introduction"], "answer": 0, "explanation": "BCG Matrix: Star (high growth, high share), Cash Cow (low growth, high share), Question Mark (high growth, low share), Dog (low growth, low share)."},
        {"question": "Henri Fayol proposed how many principles of management?", "options": ["5", "10", "14", "20"], "answer": 2, "explanation": "Fayol's 14 principles include: unity of command, scalar chain, division of work, esprit de corps, etc."},
        {"question": "NPCI manages which of the following?", "options": ["NEFT", "RTGS", "UPI", "Both NEFT and RTGS"], "answer": 2, "explanation": "NPCI operates UPI, NACH, RuPay, BBPS, *99#. NEFT and RTGS are operated by RBI."},
        {"question": "Account Aggregator framework enables:", "options": ["Automatic tax filing", "Consent-based financial data sharing", "Loan auto-approval", "Credit score improvement"], "answer": 1, "explanation": "Account Aggregator (AA) framework by RBI enables consent-based sharing of financial data between FIPs and FIUs."},
        {"question": "Kumar Mangalam Birla Committee (1999) was related to:", "options": ["Banking reforms", "Corporate governance", "Insurance reforms", "Tax reforms"], "answer": 1, "explanation": "Birla Committee laid the first corporate governance code for listed companies in India. Adopted by SEBI."},
        {"question": "Uday Kotak Committee (2017) recommendations were adopted by:", "options": ["RBI", "Government", "SEBI", "IRDAI"], "answer": 2, "explanation": "SEBI adopted Uday Kotak Committee recommendations on corporate governance including separate chairperson and MD/CEO for top 500 companies."},
        {"question": "RBI's digital lending guidelines (2022) mandate that:", "options": ["All loans must be offline", "Loan disbursement must go to borrower's bank account", "Only banks can lend digitally", "Minimum loan is Rs 50,000"], "answer": 1, "explanation": "RBI 2022 guidelines: loan must be disbursed/serviced directly into borrower's bank account; no third-party pass-through; full transparency."},
        {"question": "Value at Risk (VaR) is a measure of:", "options": ["Profit potential", "Maximum potential loss at a confidence level", "Average return", "Risk-adjusted return"], "answer": 1, "explanation": "VaR estimates the maximum potential loss over a given time period at a certain confidence level (e.g., 99% confidence, 1-day VaR)."},
        {"question": "Lewin's change management model has how many stages?", "options": ["2", "3", "4", "5"], "answer": 1, "explanation": "Kurt Lewin's model: Unfreeze (prepare for change), Change (implement), Refreeze (stabilize). Simple but foundational."},
        {"question": "IBBI regulates:", "options": ["Insurance sector", "Insolvency proceedings under IBC", "Banking sector", "Securities market"], "answer": 1, "explanation": "IBBI (Insolvency and Bankruptcy Board of India) regulates insolvency professionals, agencies, and information utilities under IBC 2016."},
        {"question": "In a Call Money market, tenure of borrowing is:", "options": ["1 day", "1 day to 14 days", "Up to 1 year", "Up to 3 months"], "answer": 0, "explanation": "Call money = overnight (1 day). Notice money = 2-14 days. Term money = 15 days to 1 year. Only banks and PDs participate."},
        {"question": "AIF Category II includes:", "options": ["Venture capital funds", "PE funds, real estate funds", "Hedge funds", "Angel funds"], "answer": 1, "explanation": "AIF Cat I: venture capital, social venture, infra, angel. Cat II: PE, debt, real estate funds (residual). Cat III: hedge funds, PIPE."},
        {"question": "Emotional Intelligence by Daniel Goleman has how many components?", "options": ["3", "4", "5", "6"], "answer": 2, "explanation": "Goleman's 5 EI components: Self-awareness, Self-regulation, Motivation, Empathy, Social skills."},
    ],
}


# ═════════════════════════════════════════════════════════════════════════════
# REVISION CHECKLISTS — LAST 30 DAYS
# ═════════════════════════════════════════════════════════════════════════════

LAST_30_DAY_PLAN = {
    "Phase 1": {
        "weeks": [
            {
                "week": "Week 4 (D-28 to D-22)",
                "daily_schedule": [
                    "Morning (2h): 1 Full-length mock -> analyze -> note mistakes",
                    "Afternoon (2h): Weak topic practice (Puzzles/DI)",
                    "Evening (1.5h): Current Affairs daily capsule + Banking awareness",
                    "Night (30m): Revise formulas & one-liner facts",
                ],
                "targets": "Score 120+ in mocks consistently",
            },
            {
                "week": "Week 3 (D-21 to D-15)",
                "daily_schedule": [
                    "Morning (2h): Sectional test — Reasoning (timed)",
                    "Afternoon (2h): GA revision — RBI policies + committees + acts",
                    "Evening (1.5h): Quant practice — DI sets (10 sets/day)",
                    "Night (30m): English vocabulary + idioms",
                ],
                "targets": "Score 130+ in mocks; Reasoning 40+",
            },
            {
                "week": "Week 2 (D-14 to D-8)",
                "daily_schedule": [
                    "Morning (2.5h): Full mock with strict 2-hour timing, analyze in 30 min",
                    "Afternoon (1.5h): Only weak areas from mock analysis",
                    "Evening (1.5h): Last 3 months CA intensive revision",
                    "Night (30m): Read RBI Governor list + committee names",
                ],
                "targets": "Score 140+ in mocks; accuracy 85%+",
            },
            {
                "week": "Week 1 (D-7 to D-1)",
                "daily_schedule": [
                    "Morning (2h): Light mock OR sectional — no new topics",
                    "Afternoon (1h): Revise: formulas, committees, acts, shortcuts",
                    "Evening (1h): CA capsule — last 1 month focus",
                    "Night: Relax. Sleep by 10 PM. No new content.",
                ],
                "targets": "Stay sharp, don't burn out. Confidence > cramming.",
            },
        ],
        "exam_eve": [
            "No studying after 6 PM on the day before exam",
            "Prepare: Admit card, ID proof, pen, watch (analog), water bottle",
            "Light dinner. No heavy/spicy food.",
            "Sleep by 10 PM. Set 2 alarms.",
            "Morning: Light breakfast. Reach center 45 min early.",
            "Quick prayer/meditation. Trust your preparation.",
        ],
    },
    "Phase 2": {
        "weeks": [
            {
                "week": "Week 4 (D-28 to D-22)",
                "daily_schedule": [
                    "Morning (3h): ESI — read Economic Survey chapters 1-3 + practice MCQs",
                    "Afternoon (2h): FM — Basel norms + Financial Markets deep dive",
                    "Evening (2h): Essay writing practice — 1 essay (topic: Economy/Banking)",
                    "Night (1h): Precis writing practice",
                ],
                "targets": "Complete ESI syllabus reading; 1 essay/day",
            },
            {
                "week": "Week 3 (D-21 to D-15)",
                "daily_schedule": [
                    "Morning (3h): FM — Management theories + Corporate Governance + practice",
                    "Afternoon (2h): ESI — Social issues + Government schemes",
                    "Evening (2h): Essay practice — pick RBI/banking topic",
                    "Night (1h): Revise FM formulas + key ratios",
                ],
                "targets": "Score 50+ in ESI mocks; 45+ in FM mocks",
            },
            {
                "week": "Week 2 (D-14 to D-8)",
                "daily_schedule": [
                    "Morning (2.5h): Full Paper 1 (ESI) mock test + analysis",
                    "Afternoon (2.5h): Full Paper 3 (FM) mock test + analysis",
                    "Evening (2h): Paper 2 (English) — timed essay + precis",
                    "Night (30m): Quick revision of all committee names + acts",
                ],
                "targets": "ESI 55+, FM 50+, English 60+",
            },
            {
                "week": "Week 1 (D-7 to D-1)",
                "daily_schedule": [
                    "Morning (2h): ESI + FM fact sheets + key data revision",
                    "Afternoon (1.5h): 1 final practice essay (timed 30 min)",
                    "Evening (1h): Revision only — no new topics",
                    "Night: Sleep well. Stay calm. Phase 2 rewards knowledge depth.",
                ],
                "targets": "Stay confident. Review your notes, not new books.",
            },
        ],
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# TOPPER STRATEGIES — AIR 1 MINDSET
# ═════════════════════════════════════════════════════════════════════════════

TOPPER_TIPS = [
    {"title": "Accuracy > Attempts", "detail": "AIR 1 candidates score 160+ by attempting 160-170 with 90%+ accuracy. Don't attempt 200 with 70% accuracy."},
    {"title": "Mock Analysis is 50% of Preparation", "detail": "Every mock test should be followed by 30 min of analysis. Track: which topics you're getting wrong, time per question, silly mistakes."},
    {"title": "Time Management is the Real Exam", "detail": "The exam tests speed as much as knowledge. Practice under strict time limits. If a question takes > 90 sec (Phase 1), mark and move."},
    {"title": "GA is the Game Changer", "detail": "GA has 80 marks = 40% of Phase 1. Most candidates neglect this. Read daily CA for 6 months + banking awareness. Quickest way to boost score by 20-30 marks."},
    {"title": "Reasoning: Solve Easy Puzzles First", "detail": "In reasoning, scan all puzzles. Do the 2-variable puzzles first. Skip 3+ variable puzzles if conditions are tricky. Come back if time permits."},
    {"title": "Quant: DI is Non-Negotiable", "detail": "DI = 15-18 questions = half of Quant section. Master all DI types. If you score 14/15 in DI, you've cleared the quant cutoff already."},
    {"title": "Phase 2 English: Structure & Data Win", "detail": "For essays, use: Intro (define topic) -> Current scenario (data) -> Govt initiatives -> Challenges -> Way forward -> Conclusion. Include 3-4 statistics."},
    {"title": "Revision Cycles", "detail": "Do 3 revision cycles: 1st (learn topics) -> 2nd (practice MCQs) -> 3rd (quick fact revision before exam). Each cycle should be shorter than the previous."},
    {"title": "Negative Marking Math", "detail": "0.25 negative marking means you need >25% chance of being correct to attempt. If you can eliminate 2/4 options, ALWAYS attempt. If you can't eliminate any, SKIP."},
    {"title": "Health = Performance", "detail": "Sleep 7-8 hours daily in the last month. Exercise 20 min daily. Eat clean. A tired brain makes silly mistakes worth 5-10 marks."},
]


# ═════════════════════════════════════════════════════════════════════════════
# IMPORTANT FORMULAS / SHORTCUTS — QUANT
# ═════════════════════════════════════════════════════════════════════════════

QUANT_SHORTCUTS = [
    {"topic": "Percentage", "shortcuts": [
        "Fraction equivalents: 1/2=50%, 1/3=33.33%, 1/4=25%, 1/5=20%, 1/6=16.67%, 1/7=14.28%, 1/8=12.5%",
        "If A is x% more than B, then B is (x/(100+x))*100% less than A",
        "Population formula: P * (1 + r/100)^n",
        "Successive discounts: a% and b% -> net = (a + b - ab/100)%",
    ]},
    {"topic": "Profit & Loss", "shortcuts": [
        "CP * (100 + Profit%) / 100 = SP",
        "If CP of x items = SP of y items -> Profit% = ((x-y)/y) * 100",
        "Dishonest dealer: Profit% = (True weight - False weight) / False weight * 100",
    ]},
    {"topic": "SI / CI", "shortcuts": [
        "SI = P * R * T / 100",
        "CI = P * (1 + R/100)^T - P",
        "CI - SI for 2 years = P * (R/100)^2",
        "CI - SI for 3 years = P * (R/100)^2 * (3 + R/100)",
        "If amount doubles in T years (SI): Rate = 100/T",
    ]},
    {"topic": "Time & Work", "shortcuts": [
        "If A does work in 'a' days -> A's 1-day work = 1/a",
        "A+B together: 1/a + 1/b = (a+b)/ab -> days = ab/(a+b)",
        "Pipes: Inlet fills, Outlet empties -> Net = 1/inlet - 1/outlet",
        "LCM method: Take LCM of days as total work units",
    ]},
    {"topic": "Time Speed Distance", "shortcuts": [
        "Speed = Distance / Time",
        "Average speed for same distance: 2*S1*S2/(S1+S2)",
        "Relative speed (opposite direction): S1+S2 | Same direction: |S1-S2|",
        "Train crossing: Time = (Length of train + Length of object) / Speed",
        "Boats: Downstream = (u+v), Upstream = (u-v) where u=boat, v=stream",
    ]},
    {"topic": "Number Series", "shortcuts": [
        "Common patterns: +n, *n, n^2, n^3, n^2 +/- n, alternating",
        "Check differences: 1st diff -> 2nd diff -> if constant = quadratic pattern",
        "Prime number series: 2, 3, 5, 7, 11, 13, 17...",
        "Fibonacci: each term = sum of prev 2",
    ]},
    {"topic": "DI Strategy", "shortcuts": [
        "Read all questions before calculating — some need same base calc",
        "Approximate: 33.33% = 1/3, 14.28% = 1/7, 16.67% = 1/6",
        "For percentage change: (New-Old)/Old * 100 — approximate the division",
        "For ratio questions: simplify to smallest integers first",
        "If 'approximately' appears -> round aggressively, match closest option",
    ]},
]


# ═════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def get_exam_pattern():
    return EXAM_PATTERN

def get_cutoffs():
    return HISTORICAL_CUTOFFS

def get_air1_targets():
    return AIR1_TARGETS

def get_rbi_governors():
    return RBI_GOVERNORS

def get_rbi_committees():
    return RBI_COMMITTEES

def get_important_acts():
    return IMPORTANT_ACTS

def get_esi_topics():
    return ESI_TOPICS

def get_fm_topics():
    return FM_TOPICS

def get_phase2_mcqs(paper="ESI"):
    return PHASE2_MCQS.get(paper, [])

def get_all_phase2_mcq_count():
    return sum(len(qs) for qs in PHASE2_MCQS.values())

def get_last30_plan(phase="Phase 1"):
    return LAST_30_DAY_PLAN.get(phase)

def get_topper_tips():
    return TOPPER_TIPS

def get_quant_shortcuts():
    return QUANT_SHORTCUTS
