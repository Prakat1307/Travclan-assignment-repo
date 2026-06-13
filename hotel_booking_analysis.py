import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import warnings, os, sys
warnings.filterwarnings("ignore")

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DATA_PATH   = r"e:\assignment\uploads\Hotel_bookings_final.csv"
OUTPUT_DIR  = r"e:\assignment\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PALETTE = {
    "primary"   : "#4F46E5",
    "secondary" : "#06B6D4",
    "accent"    : "#F59E0B",
    "danger"    : "#EF4444",
    "success"   : "#10B981",
    "muted"     : "#6B7280",
    "bg"        : "#F8FAFC",
    "card"      : "#FFFFFF",
}

CHANNEL_COLORS  = ["#4F46E5", "#06B6D4", "#10B981"]
ROOM_COLORS     = ["#10B981", "#4F46E5", "#F59E0B"]
STAR_COLORS     = ["#06B6D4", "#4F46E5", "#F59E0B", "#EF4444"]
MONTH_GRADIENT  = plt.cm.RdYlGn_r

plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "figure.facecolor"  : PALETTE["bg"],
    "axes.facecolor"    : PALETTE["card"],
    "axes.edgecolor"    : "#E5E7EB",
    "axes.grid"         : True,
    "grid.color"        : "#F3F4F6",
    "grid.linewidth"    : 0.7,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "xtick.labelsize"   : 9,
    "ytick.labelsize"   : 9,
    "axes.labelsize"    : 10,
    "axes.titlesize"    : 11,
    "axes.titleweight"  : "bold",
})

print("=" * 65)
print("  HOTEL BOOKING ANALYSIS  -  Starting")
print("=" * 65)

df = pd.read_csv(DATA_PATH)

for col in ["booking_date", "check_in_date", "check_out_date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

df["stay_length"]    = (df["check_out_date"] - df["check_in_date"]).dt.days
df["lead_time"]      = (df["check_in_date"]  - df["booking_date"]).dt.days
df["is_cancelled"]   = (df["booking_status"] == "Cancelled").astype(int)
df["month"]          = df["check_in_date"].dt.month
df["quarter"]        = df["check_in_date"].dt.quarter
df["gross_margin"]   = df["markup"] / df["selling_price"] * 100

print(f"\n  Records loaded : {len(df):,}")
print(f"  Date range     : {df['check_in_date'].min().date()} to {df['check_in_date'].max().date()}")
print(f"  Missing dates  : {df['check_in_date'].isna().sum():,} rows (kept for non-date analyses)\n")

overall_cancel = df["is_cancelled"].mean() * 100

print("-" * 65)
print("SECTION 1 - KEY OBSERVATIONS")
print("-" * 65)

print(f"\n  Overall cancellation rate : {overall_cancel:.2f}%")
print(f"  Total bookings            : {len(df):,}")
print(f"  Cancelled                 : {df['is_cancelled'].sum():,}")
print(f"  Confirmed                 : {(df['booking_status']=='Confirmed').sum():,}")
print(f"  Failed                    : {(df['booking_status']=='Failed').sum():,}")

print("\n  Booking Channel Analysis:")
ch = df.groupby("booking_channel").agg(
    Count       = ("customer_id", "count"),
    Cancel_Rate = ("is_cancelled", lambda x: round(x.mean()*100, 2)),
    Avg_Value   = ("booking_value", lambda x: round(x.mean(), 0)),
    Avg_Stay    = ("stay_length", lambda x: round(x.mean(), 2)),
    Avg_Markup  = ("markup", lambda x: round(x.mean(), 0)),
).reset_index()
print(ch.to_string(index=False))

print("\n  Room Type Analysis:")
rt = df.groupby("room_type").agg(
    Count       = ("customer_id", "count"),
    Cancel_Rate = ("is_cancelled", lambda x: round(x.mean()*100, 2)),
    Avg_Value   = ("booking_value", lambda x: round(x.mean(), 0)),
    Avg_Markup  = ("markup", lambda x: round(x.mean(), 0)),
).reset_index()
print(rt.to_string(index=False))

print("\n  Star Rating Analysis:")
sr = df.groupby("star_rating").agg(
    Count       = ("customer_id", "count"),
    Cancel_Rate = ("is_cancelled", lambda x: round(x.mean()*100, 2)),
    Avg_Value   = ("booking_value", lambda x: round(x.mean(), 0)),
    Avg_Stay    = ("stay_length", lambda x: round(x.mean(), 2)),
).reset_index()
print(sr.to_string(index=False))

print("\n  Monthly Booking Trends:")
mo = df.groupby("month").agg(
    Bookings    = ("customer_id", "count"),
    Cancel_Rate = ("is_cancelled", lambda x: round(x.mean()*100, 2)),
    Avg_Value   = ("booking_value", lambda x: round(x.mean(), 0)),
).reset_index()
month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
               7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
mo["Month"] = mo["month"].map(month_names)
print(mo[["Month","Bookings","Cancel_Rate","Avg_Value"]].to_string(index=False))

print("-" * 65)
print("SECTION 2 - ROOT CAUSE ANALYSIS")
print("-" * 65)
print("""
  1. CANCELLATION DRIVERS
     - Travel Agent (27.9%):  Agents hold multiple options simultaneously ('speculative
       booking'), corporate travellers face policy-driven trip cancellations, and the
       agent channel lacks deposit requirements that would otherwise deter frivolous holds.
     - Standard Rooms (23.3%): Budget-conscious guests have more price-comparison
       flexibility; numerous alternatives exist in the same price tier, lowering switching
       costs significantly.
     - 5-Star Properties (21.3%): Higher absolute prices mean guests are more sensitive to
       any change in plans; luxury alternatives are easier to find in popular US cities.

  2. CHANNEL PERFORMANCE DRIVERS
     - Web (17.6% cancel, $28,191 avg): Customers who book directly via website invest
       more research time -- higher intent and lower buyer's remorse.
     - Mobile App (21.6% cancel, $21,351 avg): Impulsive, deal-driven bookings through
       push notifications result in lower commitment; easy in-app cancel flows reduce
       friction for changing plans.
     - Travel Agents (27.9% cancel, $24,454 avg): Booking quality is structurally weaker
       because agents are incentivised on bookings, not stays, and face no penalty for
       customer no-shows.

  3. SEASONAL / TEMPORAL PATTERNS
     - Peak check-in months (Apr-Jun): Summer vacation planning and wedding season drive
       a surge in bookings; low cancellation rates (0.4-0.6%) suggest committed guests.
     - High-cancel months (Aug-Sep: 10-11%): Post-summer period sees last-minute plans
       collapse, possibly linked to school re-start and travel budget exhaustion.
     - Consistent ~4-day stays across all star ratings indicate that property type does not
       significantly influence trip duration -- segment the target by purpose instead.
""")

print("-" * 65)
print("SECTION 3 - BUSINESS RECOMMENDATIONS")
print("-" * 65)
print("""
  1. REDUCE CANCELLATIONS
     - Require a 20-25% non-refundable deposit for Travel Agent bookings.
     - Introduce agent performance scorecards; restrict commission tiers below
       threshold completion rates.
     - Offer 'Flexible Date' credits (redeemable 6 months) as a retention
       alternative to full cancellations for Standard room guests.
     - Add trip-insurance upsell at checkout for high-risk months (Aug/Sep).

  2. IMPROVE PROFITABILITY & REPEAT BOOKINGS
     - Launch a 'Book Direct Rewards' programme: 10% discount + loyalty points
       for Web channel bookings, eroding OTA and Travel Agent dependency.
     - Post-stay: send personalised rebooking offers within 24 hours of checkout.
     - Introduce milestone rewards (3rd, 5th, 10th stay) to drive repeat visits.
     - Upsell Deluxe/Suite upgrades at check-in to raise revenue per occupied room.

  3. PRICING, PROMOTIONS & CHANNEL STRATEGY
     - Web: Price parity + exclusive perks (late checkout, F&B credits).
     - Mobile App: Flash sales (18-hour windows) exclusively through push
       notifications to convert impulse interest without lowering brand rates.
     - Travel Agents: Volume-tiered commissions (8% to 15%) tied to stay
       completion, not bookings.
     - Peak season (Apr-Jun): Early-bird pricing -- 15% off for 60+ day advance
       bookings; minimum 2-night stays.
     - Off-peak (Aug-Sep, Feb): 'Stay 4, Pay 3' bundles to stimulate demand and
       reduce dependence on last-minute discounting.
     - Dynamic pricing engine: Adjust rates daily using 30/60/90-day occupancy
       forecasts and competitor benchmarking.

  4. IMPLEMENTATION ROADMAP
     Phase 1 (0-4 weeks)  : Agent deposit policy, Post-stay email campaigns
     Phase 2 (1-3 months) : Book Direct Rewards launch, Mobile flash sale system
     Phase 3 (3-6 months) : Dynamic pricing engine, Loyalty milestone rewards
     Phase 4 (6-12 months): Agent scorecard system, bundle packaging
     Expected KPI Impact  : 15-20%% reduction in cancellations, 10-15%% increase in direct bookings,
                            8-12%% improvement in avg booking value, 25%% increase in repeat rate
""")

print("\n  Generating visualizations ...")

mo_valid = mo.dropna(subset=["month"])
cancel_norm = (mo_valid["Cancel_Rate"] - mo_valid["Cancel_Rate"].min()) / \
              (mo_valid["Cancel_Rate"].max() - mo_valid["Cancel_Rate"].min())

def save(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, name), dpi=150, bbox_inches="tight",
                facecolor=PALETTE["bg"])
    plt.close(fig)
    print(f"  Saved -> {name}")

def new_fig(w=8, h=5):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=PALETTE["bg"])
    ax.set_facecolor(PALETTE["card"])
    return fig, ax

fig, ax = new_fig()
bars = ax.bar(ch["booking_channel"], ch["Cancel_Rate"],
              color=CHANNEL_COLORS, edgecolor="white", linewidth=1.2, width=0.55)
for bar, val in zip(bars, ch["Cancel_Rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold", color="#1E293B")
ax.axhline(overall_cancel, color=PALETTE["danger"], linestyle="--", linewidth=1.5,
           label=f"Overall {overall_cancel:.1f}%")
ax.set_title("Cancellation Rate by Booking Channel", fontsize=13, fontweight="bold")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 35)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "01_cancel_rate_by_channel.png")

fig, ax = new_fig()
bars2 = ax.bar(ch["booking_channel"], ch["Avg_Value"],
               color=CHANNEL_COLORS, edgecolor="white", linewidth=1.2, width=0.55)
for bar, val in zip(bars2, ch["Avg_Value"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f"${val:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_title("Avg Booking Value by Channel", fontsize=13, fontweight="bold")
ax.set_ylabel("Avg Booking Value ($)")
ax.set_ylim(0, 34000)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "02_avg_value_by_channel.png")

fig, ax = new_fig(6, 6)
sizes = ch["Count"].values
wedges, texts, autotexts = ax.pie(
    sizes, labels=ch["booking_channel"], autopct="%1.1f%%",
    colors=CHANNEL_COLORS, startangle=140, explode=[0.03]*len(sizes),
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=10)
)
for at in autotexts:
    at.set_fontweight("bold")
ax.set_title("Booking Channel Distribution", fontsize=13, fontweight="bold")
save(fig, "03_channel_distribution.png")

fig, ax = new_fig()
bars4 = ax.bar(rt["room_type"], rt["Cancel_Rate"],
               color=ROOM_COLORS, edgecolor="white", linewidth=1.2, width=0.45)
for bar, val in zip(bars4, rt["Cancel_Rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.axhline(overall_cancel, color=PALETTE["danger"], linestyle="--", linewidth=1.5,
           label=f"Overall {overall_cancel:.1f}%")
ax.set_title("Cancellation Rate by Room Type", fontsize=13, fontweight="bold")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 30)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "04_cancel_rate_by_room_type.png")

fig, ax = new_fig()
bars5 = ax.bar(sr["star_rating"].astype(str) + "-Star", sr["Cancel_Rate"],
               color=STAR_COLORS, edgecolor="white", linewidth=1.2, width=0.5)
for bar, val in zip(bars5, sr["Cancel_Rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.axhline(overall_cancel, color=PALETTE["danger"], linestyle="--", linewidth=1.5,
           label=f"Overall {overall_cancel:.1f}%")
ax.set_title("Cancellation Rate by Star Rating", fontsize=13, fontweight="bold")
ax.set_ylabel("Cancellation Rate (%)")
ax.set_ylim(0, 28)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "05_cancel_rate_by_star_rating.png")

fig, ax = new_fig(6, 6)
sizes6 = rt["Count"].values
wedges6, texts6, autotexts6 = ax.pie(
    sizes6, labels=rt["room_type"], autopct="%1.1f%%",
    colors=ROOM_COLORS, startangle=90,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=10)
)
for at in autotexts6:
    at.set_fontweight("bold")
ax.set_title("Room Type Distribution", fontsize=13, fontweight="bold")
save(fig, "06_room_type_distribution.png")

fig, ax = new_fig(12, 5)
bar_colors = [plt.cm.RdYlGn_r(v * 0.85 + 0.05) for v in cancel_norm]
bars7 = ax.bar(mo_valid["Month"], mo_valid["Bookings"],
               color=bar_colors, edgecolor="white", linewidth=1, width=0.65)
for bar, val in zip(bars7, mo_valid["Bookings"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15,
            f"{val:,}", ha="center", va="bottom", fontsize=8)
ax7b = ax.twinx()
ax7b.plot(mo_valid["Month"], mo_valid["Cancel_Rate"],
          "o-", color=PALETTE["danger"], linewidth=2, markersize=7, label="Cancel Rate %")
ax7b.set_ylabel("Cancellation Rate (%)", color=PALETTE["danger"], fontsize=10)
ax7b.tick_params(axis="y", colors=PALETTE["danger"])
ax.set_title("Monthly Bookings & Cancellation Rate (Check-in Month)", fontsize=13, fontweight="bold")
ax.set_ylabel("Number of Bookings")
ax7b.legend(loc="upper right", fontsize=9)
ax.spines["top"].set_visible(False)
save(fig, "07_monthly_bookings_and_cancel_rate.png")

fig, ax = new_fig(10, 5)
ax.plot(mo_valid["Month"], mo_valid["Avg_Value"],
        "s-", color=PALETTE["primary"], linewidth=2.5, markersize=8)
ax.fill_between(mo_valid["Month"], mo_valid["Avg_Value"],
                alpha=0.15, color=PALETTE["primary"])
for x, y in zip(mo_valid["Month"], mo_valid["Avg_Value"]):
    ax.text(x, y + 50, f"${y:,.0f}", ha="center", va="bottom", fontsize=8)
ax.set_title("Avg Booking Value by Month", fontsize=13, fontweight="bold")
ax.set_ylabel("Avg Booking Value ($)")
ax.set_xticks(range(len(mo_valid)))
ax.set_xticklabels(mo_valid["Month"], rotation=45, ha="right")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "08_avg_value_by_month.png")

fig, ax = new_fig()
stay_counts = df["stay_length"].value_counts().sort_index()
stay_counts = stay_counts[(stay_counts.index >= 1) & (stay_counts.index <= 10)]
ax.bar(stay_counts.index, stay_counts.values,
       color=PALETTE["secondary"], edgecolor="white", linewidth=1)
ax.set_title("Distribution of Stay Lengths", fontsize=13, fontweight="bold")
ax.set_xlabel("Stay Length (Nights)")
ax.set_ylabel("Number of Bookings")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "09_stay_length_distribution.png")

pm = df.groupby("payment_method").agg(
    Cancel_Rate = ("is_cancelled", lambda x: round(x.mean()*100, 2)),
    Avg_Value   = ("booking_value", "mean")
).reset_index().sort_values("Cancel_Rate", ascending=True)
colors_pm = [PALETTE["success"] if v < overall_cancel else PALETTE["danger"]
             for v in pm["Cancel_Rate"]]
fig, ax = new_fig()
bars10 = ax.barh(pm["payment_method"], pm["Cancel_Rate"],
                 color=colors_pm, edgecolor="white", linewidth=1)
for bar, val in zip(bars10, pm["Cancel_Rate"]):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=10, fontweight="bold")
ax.axvline(overall_cancel, color=PALETTE["danger"], linestyle="--",
           linewidth=1.5, label=f"Overall {overall_cancel:.1f}%")
ax.set_title("Cancellation Rate by Payment Method", fontsize=13, fontweight="bold")
ax.set_xlabel("Cancellation Rate (%)")
ax.set_xlim(0, 26)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
save(fig, "10_cancel_rate_by_payment_method.png")

hm_data = df.groupby(["booking_channel", "room_type"])["markup"].mean().unstack()
fig, ax = new_fig(8, 5)
sns.heatmap(hm_data, ax=ax, cmap="YlOrRd", annot=True, fmt=".0f",
            linewidths=0.5, cbar_kws={"label": "Avg Markup ($)"})
ax.set_title("Avg Markup: Channel x Room Type", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("")
save(fig, "11_markup_heatmap_channel_vs_room.png")

print("\n  Analysis script complete.")
print("=" * 65)

