import streamlit as st
from itertools import combinations
import calendar
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Electricity Bill Splitter", layout="centered")

# --------------- Title & Intro ---------------
st.markdown(
    "<h1 style='text-align: center;'>⚡ Smart Electricity Bill Splitter</h1>"
    "<p style='text-align: center; color: gray;'>Split bills fairly by usage and stay duration — without spreadsheets!</p>",
    unsafe_allow_html=True
)

st.divider()

# --------------- Helper Functions ---------------
def compute_set_ratios(sets, original_ratios):
    n = len(sets)
    result = {}

    for r in range(1, n + 1):
        for indices in combinations(range(n), r):
            common = set.intersection(*[sets[i] for i in indices])
            other_indices = set(range(n)) - set(indices)
            for other_i in other_indices:
                common -= sets[other_i]

            key = "common_in_" + "_".join(f"set_{i+1}" for i in indices)
            included_ratios = [original_ratios[i] for i in indices]
            total = sum(included_ratios)
            keys = [str(i+1) for i in indices]
            adjusted_ratios = [ratio / total for ratio in included_ratios]
            my_dict = {k: v for k, v in zip(keys, adjusted_ratios)}

            result[key] = {
                "elements": common,
                "ratios": my_dict
            }
    return result

def list_to_set(lists):
    sets = []
    for lst in lists:
        flat_list = []
        for item in lst:
            if isinstance(item, list):
                flat_list.extend(item)
            else:
                flat_list.append(item)
        sets.append(set(flat_list))
    return sets

def duration_to_list(duration_list):
    range_list = []
    for duration in duration_list:
        if "," in duration:
            sub_ranges = duration.split(",")
            sub_range_list = []
            for sub in sub_ranges:
                try:
                    first, second = sub.split("-")
                    sub_range_list.append(list(range(int(first), int(second)+1)))
                except:
                    continue
            range_list.append(sub_range_list)
        else:
            try:
                first, second = duration.split("-")
                range_list.append(list(range(int(first), int(second)+1)))
            except:
                range_list.append([])
    return range_list

# --------------- Step 1: General Info ---------------
with st.container():
    st.header("📝 Step 1: Bill Basics")
    col1, col2 = st.columns(2)
    with col1:
        total = st.number_input("💰 Total electricity bill (VND)", min_value=0.0)
    with col2:
        roommates = st.number_input("👥 Number of roommates", min_value=1, step=1)

    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("📅 Month", range(1, 13), format_func=lambda x: calendar.month_name[x])
    with col2:
        selected_year = st.number_input("📆 Year", min_value=2000, max_value=2100, value=datetime.now().year)

    days_in_month = calendar.monthrange(selected_year, selected_month)[1]
    pay_per_day = total / days_in_month if days_in_month else 0

    st.success(f"📆 {calendar.month_name[selected_month]} {selected_year} has **{days_in_month} days**.")
    st.info(f"💡 Base cost per day: **{pay_per_day:,.2f} VND**")

# --------------- Step 2: Usage Ratios ---------------
with st.container():
    st.header("⚖️ Step 2: Usage Ratios")
    st.markdown("Enter your **electricity usage share**. Leave the last person blank to autofill.")

    ratio_list = []
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            if i == int(roommates) - 1:
                ratio = st.number_input(f"Person {i+1} (auto)", min_value=0.0, max_value=1.0, step=0.01, key=f"ratio_{i}")
            else:
                ratio = st.number_input(f"Person {i+1}", min_value=0.0, max_value=1.0, step=0.01, key=f"ratio_{i}")
            ratio_list.append(ratio)

    if len(ratio_list) > 1:
        filled = ratio_list[:-1]
        if all(r > 0 for r in filled) and ratio_list[-1] == 0.0:
            last = round(1.0 - sum(filled), 3)
            if last >= 0:
                ratio_list[-1] = last
                st.success(f"✅ Auto-filled last ratio: **{last:.3f}**")
            else:
                st.error("❌ Ratios exceed 1.0 — please fix.")

# --------------- Step 3: Duration of Stay ---------------
with st.container():
    st.header("📆 Step 3: Duration of Stay")
    st.markdown("Use format `01-15` or multiple like `01-10,20-30`.")
    duration_list = []
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            duration = st.text_input(f"Person {i+1}", key=f"duration_{i}")
            duration_list.append(duration)

# --------------- Step 4: Calculate & Visualize ---------------
st.divider()
if st.button("🧮 Calculate & Show Results"):
    my_set = list_to_set(duration_to_list(duration_list))
    result = compute_set_ratios(my_set, ratio_list)

    bill_list = []
    for i in range(int(roommates)):
        topay = 0
        for v in result.values():
            days = len(v["elements"])
            ratios = v["ratios"]
            if str(i+1) in ratios:
                topay += pay_per_day * ratios[str(i+1)] * days
        bill_list.append(round(topay, 2))

    total_calculated = sum(bill_list)
    discrepancy = total - total_calculated

    st.subheader("💸 Bill Breakdown")
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            st.metric(label=f"Person {i+1}", value=f"{bill_list[i]}")

    st.markdown(f"**🧾 Original Total:** {total:,.2f} VND")
    st.markdown(f"**📊 Calculated Total:** {total_calculated:,.2f} VND")

    if abs(discrepancy) > 0.01:
        st.warning(f"⚠️ Discrepancy of {discrepancy:.2f} VND due to rounding. Adjusting...")
        weights = [bill / total_calculated for bill in bill_list]
        adjustments = [round(discrepancy * w, 2) for w in weights]
        adjustments[-1] += discrepancy - sum(adjustments)
        bill_list = [a + b for a, b in zip(bill_list, adjustments)]
        st.info("🔧 Adjusted final values:")

    # 📊 PIE CHART VISUALIZATION
    st.subheader("📈 Share Visualization")
    labels = [f"Person {i+1}" for i in range(int(roommates))]
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=bill_list,
            hole=0.4,
            textinfo="label+percent",
            marker=dict(line=dict(color='#000000', width=1))
        )]
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
