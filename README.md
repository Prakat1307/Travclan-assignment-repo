# Hotel Booking Analysis — Travclan Assignment

A complete end-to-end data analysis of **30,000 hotel bookings** across 10 US cities (April 2024 – June 2025), covering key observations, root cause analysis, and actionable business recommendations.

---

## Repository Structure

```
├── hotel_booking_analysis.py          # Main analysis & visualization script
├── create_report.py                   # PowerPoint report generator
├── output/
│   ├── 01_cancel_rate_by_channel.png
│   ├── 02_avg_value_by_channel.png
│   ├── 03_channel_distribution.png
│   ├── 04_cancel_rate_by_room_type.png
│   ├── 05_cancel_rate_by_star_rating.png
│   ├── 06_room_type_distribution.png
│   ├── 07_monthly_bookings_and_cancel_rate.png
│   ├── 08_avg_value_by_month.png
│   ├── 09_stay_length_distribution.png
│   ├── 10_cancel_rate_by_payment_method.png
│   ├── 11_markup_heatmap_channel_vs_room.png
│   └── Hotel_Booking_Analysis_Report.pptx
└── .gitignore
```

---

## Dataset Overview

| Attribute | Value |
|---|---|
| Total Records | 30,000 bookings |
| Date Range | April 2024 – June 2025 |
| Booking Channels | Web, Mobile App, Travel Agent |
| Room Types | Standard, Deluxe, Suite |
| Star Ratings | 2★, 3★, 4★, 5★ |
| Overall Cancellation Rate | **20.23%** |

---

## Deliverable 1 — Code File

**File:** `hotel_booking_analysis.py`

### What it does
- Loads and cleans the dataset (parses dates, derives `stay_length`, `lead_time`, `is_cancelled`, `gross_margin`)
- Prints Section 1 (Key Observations), Section 2 (Root Cause Analysis), Section 3 (Business Recommendations) to console
- Generates **11 individual chart PNG files** in `output/`

### How to run
```bash
pip install pandas numpy matplotlib seaborn
python hotel_booking_analysis.py
```

**File:** `create_report.py`

### What it does
- Generates an **11-slide PowerPoint report** (`output/Hotel_Booking_Analysis_Report.pptx`) using `python-pptx`
- Requires `visualizations` charts to already exist in `output/` (run `hotel_booking_analysis.py` first)

### How to run
```bash
pip install python-pptx
python create_report.py
```

---

## Deliverable 2 — Visualizations

All charts are saved as individual PNG files in `output/`:

| File | Chart |
|---|---|
| `01_cancel_rate_by_channel.png` | Cancellation rate comparison across Web, Mobile App, Travel Agent |
| `02_avg_value_by_channel.png` | Average booking value by channel |
| `03_channel_distribution.png` | Booking volume share by channel (donut chart) |
| `04_cancel_rate_by_room_type.png` | Cancellation rate for Standard, Deluxe, Suite |
| `05_cancel_rate_by_star_rating.png` | Cancellation rate across 2★–5★ properties |
| `06_room_type_distribution.png` | Room type booking share (donut chart) |
| `07_monthly_bookings_and_cancel_rate.png` | Monthly volumes + cancellation rate (dual-axis) |
| `08_avg_value_by_month.png` | Avg booking value trend across 12 months |
| `09_stay_length_distribution.png` | Distribution of stay lengths (1–7 nights) |
| `10_cancel_rate_by_payment_method.png` | Cancellation rate by payment method |
| `11_markup_heatmap_channel_vs_room.png` | Avg markup heatmap: Channel × Room Type |

---

## Deliverable 3 — Summary Report

**File:** `output/Hotel_Booking_Analysis_Report.pptx`

An 11-slide PowerPoint deck containing:
- Title slide
- Executive Summary with KPI cards
- Key Observations (Trends 1 & 2)
- Key Observations (Trends 3 & 4 + Cancellation table)
- Full Visualizations Dashboard
- Root Cause Analysis (3-column layout)
- Business Recommendations: Reduce Cancellations
- Business Recommendations: Profitability & Repeat Bookings
- Business Recommendations: Pricing & Channel Strategy
- Implementation Roadmap & Expected Impact
- Conclusion & Next Steps

---

## 1. Key Observations

### Trend 1 — Channel Performance Divergence
The three booking channels show dramatically different economics:

| Channel | Share | Cancel Rate | Avg Booking Value |
|---|---|---|---|
| Web | 50.0% | **17.6%** ✅ | **$28,191** ✅ |
| Mobile App | 40.0% | 21.6% | $21,351 |
| Travel Agent | 10.0% | **27.9%** ❌ | $24,454 |

- The **Web channel** dominates with the lowest cancellation rate and the highest booking value — customers research thoroughly before committing.
- **Travel Agents** have the worst profile: 37% higher cancellation than Web, despite moderate booking values.
- **Mobile App** bookings are impulse/deal-driven, resulting in mid-range commitment.

### Trend 2 — Seasonal Demand Swings
Monthly data reveals a strong inverse relationship between booking volume and cancellation rate:

| Period | Avg Monthly Bookings | Cancellation Rate |
|---|---|---|
| Apr – Jun (Peak) | ~2,484 | **0.4 – 0.6%** ✅ |
| Jan – Feb (Winter) | ~1,851 | 7 – 8% |
| Aug – Sep (Post-summer) | ~1,892 | **10 – 11%** ❌ |

- Peak months (Apr–Jun) coincide with summer planning and wedding season — guests are committed.
- Post-summer (Aug–Sep) sees plan collapses driven by school-year restart and travel budget exhaustion.
- Booking values remain stable year-round ($24K–$27K), confirming the pattern is driven by *intent*, not price.

### Trend 3 — Room Type as a Commitment Signal
Room tier strongly predicts cancellation likelihood:

| Room Type | Share | Cancel Rate | Avg Value |
|---|---|---|---|
| Standard | 55.2% | **23.3%** ❌ | $25,147 |
| Suite | 9.9% | 18.0% | $24,978 |
| Deluxe | 34.9% | **16.0%** ✅ | $25,005 |

- **Standard room guests** face the lowest switching cost — budget alternatives are plentiful.
- **Deluxe room guests** show the strongest commitment despite near-identical pricing, suggesting higher trip intentionality.

### Booking Patterns by Star Rating
Star rating shows a narrower but meaningful spread:

| Star Rating | Cancel Rate | Avg Stay |
|---|---|---|
| 2★ | 19.8% | 4.04 nights |
| 3★ | 20.2% | 4.02 nights |
| 4★ | 20.0% | 3.99 nights |
| 5★ | **21.3%** | 4.00 nights |

- Average stay length is remarkably consistent (~4 nights) across all tiers — trip purpose, not property star rating, determines duration.
- 5★ properties have the highest cancellation rate due to price sensitivity and abundance of luxury alternatives.

---

## 2. Root Cause Analysis

### Cancellation Drivers

**Travel Agent Channel (27.9%)**
- Agents practice "speculative booking" — holding multiple properties simultaneously for the same customer.
- Corporate travel policies allow flexible cancellations, and agents face no financial penalty for customer no-shows.
- No deposit requirement means zero deterrent to frivolous holds.

**Standard Room Segment (23.3%)**
- Budget-conscious guests have the highest price sensitivity and the most readily available alternatives.
- No loyalty lock-in exists at this tier; switching costs are near zero.

**5-Star Properties (21.3%)**
- High absolute prices amplify the impact of any change in travel plans.
- Major US cities have abundant high-end alternatives, making it easy to switch or cancel.

**August–September Spike (10–11%)**
- School-year restart forces family travel cancellations.
- Post-peak budget exhaustion reduces leisure travel commitment.
- Weather uncertainty in late summer adds to plan instability.

### Channel Performance Gap
- **Web channel superiority** stems from deliberate purchase behavior — customers who book direct have already compared options and made a considered decision.
- **Mobile App underperformance** is structural: push-notification flash deals attract price-sensitive, impulse buyers who cancel when a better deal appears.
- **Travel Agent weakness** is incentive-driven: agents earn commission per booking, not per stay — there is no alignment between agent revenue and customer follow-through.

### Seasonal and Temporal Factors
- Stable avg markup (~$6,932–$6,985) across all channels and room types means revenue loss from cancellations is not offset by higher margins in high-cancellation segments.
- The consistent 4-night stay across all star ratings suggests properties should segment marketing by **trip purpose** (business, leisure, weddings) rather than by property tier.

---

## 3. Business Recommendations

### Reduce Cancellations

| Priority | Action | Expected Impact |
|---|---|---|
| **P1 – Immediate** | Require 25% non-refundable deposit for all Travel Agent bookings | 8–12% reduction in agent cancellations |
| **P1 – Immediate** | Agent performance scorecards — completion rate < 75% triggers commission tier demotion | Structural deterrent to speculative holds |
| **P2 – 4 Weeks** | "Flex-Date Credits" for Standard room guests: credit valid 6 months instead of full refund | Converts cancellations to rebookings |
| **P2 – 4 Weeks** | Trip insurance upsell at checkout (3% of booking value, "Cancel for Any Reason") | Reduces net cancellation cost |
| **P3 – Before Aug** | Stricter cancel windows for Aug–Sep check-ins: non-refundable 14 days out vs 3 days year-round | Reduces post-summer spike |

### Improve Profitability & Repeat Bookings

- **Book Direct Rewards Programme**: 10% discount + loyalty points for Web channel bookings. Points: 1 per $10 spent; 500 = 1 free night.
- **Post-stay personalised offers**: Rebooking email within 24 hours of checkout with 15% off same property.
- **Milestone rewards**: 3rd stay → room upgrade, 5th stay → free night, 10th stay → VIP status.
- **Upsell at check-in**: Target Standard room guests with Deluxe upgrade offers via Mobile App.
- **Bundle packages**: Room + Breakfast ($15 add-on), Room + Airport Transfer, Room + Spa to raise revenue per booking.

### Optimise Pricing, Promotions & Channel Strategy

**By Channel:**
- **Web**: Price parity + exclusive perks (late checkout, F&B credit). "Best Rate Guarantee" to prevent OTA leakage.
- **Mobile App**: 18-hour flash sales via push notifications (mobile-exclusive). Gamified check-in streaks and app-only loyalty points.
- **Travel Agents**: Volume-tiered commissions (8% → 12% → 15%) tied to *stay completion*, not bookings.

**By Season:**
- **Apr–Jun (Peak)**: "Early Bird Summer" — 15% off for 60+ day advance bookings; minimum 2-night stay.
- **Aug–Sep (High Cancel)**: "Trip Protection Bundle" — book with insurance; "rebook, don't cancel" credits valid 9 months.
- **Feb (Slow)**: "Valentine's & Beyond" couples packages; Stay-4-Pay-3 bundles.

**Dynamic Pricing Engine:**
- Daily rate adjustments based on 30/60/90-day occupancy forecasts.
- Auto-match or undercut competitors by ≤3% when occupancy < 70% with 30+ days to check-in.
- Mobile App exclusive last-minute discounts (up to 20%) to fill unsold inventory without devaluing the main channel.

---

## Implementation Roadmap

| Phase | Timeline | Actions |
|---|---|---|
| **Phase 1** | 0–4 Weeks | Agent deposit requirement (25%), Post-stay email campaigns, Flex-Date Credits |
| **Phase 2** | 1–3 Months | Book Direct Rewards launch, Mobile App flash sale system, Early-bird summer packages |
| **Phase 3** | 3–6 Months | Dynamic pricing engine, Bundle package creation, Mobile App AI personalisation |
| **Phase 4** | 6–12 Months | Full loyalty milestone system, Agent commission restructure, Competitor benchmarking |

### Expected KPI Impact (Post Full Implementation)

| KPI | Target |
|---|---|
| Overall Cancellation Rate | **↓ 15–20%** |
| Direct (Web) Bookings | **↑ 10–15%** |
| Avg Booking Value | **↑ 8–12%** |
| Repeat Customer Rate | **↑ 25%** |

---

## Requirements

```
pandas
numpy
matplotlib
seaborn
python-pptx
```

Install all dependencies:
```bash
pip install pandas numpy matplotlib seaborn python-pptx
```

---

## How to Reproduce Everything

```bash
# Step 1: Run analysis and generate all 11 charts
python hotel_booking_analysis.py

# Step 2: Generate the PowerPoint report
python create_report.py
```

All outputs will appear in the `output/` directory.

---

*Dataset: Hotel_bookings_final.csv — 30,000 records, 24 columns | Analysis Date: June 2026*
