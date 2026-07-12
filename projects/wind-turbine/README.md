

# Project 2: Exploratory Data Analysis - U.S. Wind Farm Acquisitions

## Problem Statement
Our client, a renewable energy private equity firm, is looking to acquire U.S. wind farms but requires deeper insight into the specific structural characteristics and geographic locations that drive peak energy efficiency. We are tasked with analyzing historical turbine specifications and combining them with regional wind speeds and electricity economics to identify the proven blueprints of highly successful wind farms, allowing the investment committee to strategically target assets with the highest return on investment.

## Executive Summary
Wind energy is one of the fastest-growing renewable sectors in the United States, with over 140 GW of installed capacity spread across more than 70,000 turbines. However, for a private equity firm, simply acquiring any operational wind farm is not a viable strategy. Technology and geographic suitability vary wildly across the country. To guide acquisition strategy, this project analyzed a comprehensive dataset of U.S. wind turbines, cleaning and standardizing the data before merging it with external state-level average wind speeds and commercial electricity rates. 

Our analysis revealed a highly concentrated market. The Midwest Census Region and the state of Texas dominate the U.S. landscape, holding roughly 55% of all active turbines. More importantly, we uncovered a massive technological shift: turbines installed after 2015 produce on average 5x more power (often exceeding 2.5 to 3 Megawatts) than those built in the 1990s, driven by significant increases in hub height and rotor diameter. 

By cross-referencing turbine density with environmental data, we identified a geographic "sweet spot." States with the absolute highest wind speeds (over 20 mph) remain surprisingly underbuilt, while the industry has primarily clustered in the 18–20 mph wind-speed range. Based on these insights, we recommend the firm heavily prioritize modern (post-2015) assets in the Midwest and Texas, while keeping a secondary focus on retrofitting older, obsolete farms in established markets like California.

## File Directory

```text
├── Code/
│   └── 01_EDA_Wind_Turbines.ipynb      # Main Jupyter Notebook containing all data cleaning, merging, and EDA
├── Data/
│   ├── wind-turbines.csv               # Primary dataset (U.S. Wind Turbine Database)
│   └── extra/
│       ├── windiest-states-in-the-us.-2025.csv  # External state-level wind speed data
│       ├── average_electricity_rates.csv        # External state-level commercial/residential rates
│       └── average_electricity_bills.csv        # External state-level monthly bills
├── Presentation/
│   └── Wind_Farm_Acquisitions_Presentation.pdf  # 5-minute non-technical slide deck for stakeholders
└── README.md                           # Project overview and executive summary
```

## Data & Data Dictionary
The primary data for this project is sourced from the [U.S. Wind Turbine Database](https://emp.lbl.gov/publications/us-wind-turbine-database-files) (Lawrence Berkeley National Laboratory), supplemented by external state-level wind speeds and electricity rate datasets. 

| Feature | Data Type | Source | Description |
| :--- | :--- | :--- | :--- |
| **case_id** | `int` | Original | Unique turbine identifier |
| **t_state** | `str` | Original | State where turbine is located (2-letter code) |
| **p_name** | `str` | Original | Wind farm / project name |
| **p_year** | `int` | Original | Year the project became operational |
| **t_cap** | `float` | Original | Turbine nameplate capacity (kW) |
| **t_hh** | `float` | Original | Hub height (meters) |
| **t_rd** | `float` | Original | Rotor diameter (meters) |
| **retrofit** | `int` | Original | Whether the turbine was retrofitted (0 = No, 1 = Yes) |
| **WindiestStatesAverageWindSpeedMPH** | `float` | External | State average wind speed (mph) |
| **Average (elec rate)** | `float` | External | State average electricity rate (cents/kWh) |
| **census_region** | `str` | Engineered | Geographic Census Region mapped from `t_state` |
| **decade** | `int` | Engineered | 10-year bucket derived from `p_year` using floor division |
| **wind_bucket** | `str` | Engineered | Categorical classification of wind speed (e.g., "Good", "High") |

## Conclusions & Recommendations
Based on the exploratory data analysis, the following actions are recommended for the investment committee:
* **Target the Midwest:** Prioritize acquisitions in states like Iowa, Illinois, and Minnesota where wind speeds (16-20 mph) and existing turbine density align perfectly.
* **Focus on Modern Assets:** Restrict primary acquisition targets to wind farms built post-2015. These modern assets utilize 90m+ hub heights and >120m rotors, yielding capacities upward of 3 MW, ensuring longer remaining useful life and exponentially higher efficiency.
* **Look for Retrofit Opportunities:** Older farms in Texas and California represent a secondary value-play. Purchasing these for the land and grid-connections, and subsequently replacing the rotors/turbines (retrofitting), is a proven method for multiplying output.
* **Monitor High-Wind Frontiers:** Keep a close watch on South Dakota, Montana, and Wyoming. These states feature the highest average wind speeds in the country (>20 mph) but remain heavily underbuilt, presenting a massive opportunity for new greenfield development.

## Areas for Further Research/Study
* **Site-Specific Wind Data:** This analysis utilized state-level average wind speeds. Because wind generation is highly susceptible to local topography (hills, valleys, and wake effects), future analysis requires site-specific weather and anemometer data.
* **Actual Generation vs. Capacity:** This project evaluated turbines based on their maximum rated "capacity" (kW). Future due diligence must include actual Net Generation (MWh) and capacity factors, as turbines do not run at 100% capacity year-round.
* **Maintenance & Operator Track Records:** A high-capacity turbine is unprofitable if it frequently breaks down. Securing historical maintenance logs and downtime data is a critical next step before formalizing any acquisition.

## Sources
* **U.S. Wind Turbine Database:** Lawrence Berkeley National Laboratory ([Link](https://emp.lbl.gov/publications/us-wind-turbine-database-files))
* **U.S. Energy Information Administration (EIA):** Operator and power plant electricity data.
