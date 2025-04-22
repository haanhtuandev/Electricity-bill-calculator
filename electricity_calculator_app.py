import streamlit as st
from itertools import combinations

st.set_page_config(page_title="Electricity Bill Splitter", layout="centered")

st.title("⚡ Fair Electricity Bill Splitter")
st.markdown("Split your **dorm electricity bill** based on how much each person **used** and **how long** they stayed.")

st.divider()

# ------------------ Helper Functions ------------------
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

# ------------------ Step 1: General Info ------------------
with st.expander("📝 Step 1: General Information", expanded=True):
    total = st.number_input("💰 Total electricity bill (VND)", min_value=0.0)
    roommates = st.number_input("👥 Number of roommates", min_value=1, step=1)
    days_in_month = st.slider("📅 Number of days in month", 1, 31, 30)
    pay_per_day = total / days_in_month if days_in_month else 0
    st.info(f"💡 Daily cost per person (base): **{pay_per_day:.2f} VND**")

# ------------------ Step 2: Usage Ratios ------------------
with st.expander("⚖️ Step 2: Usage Ratios", expanded=True):
    st.markdown("Enter how much electricity each person **tends to use**.")
    ratio_list = []
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            ratio = st.number_input(f"Person {i+1}", min_value=0.1, step=0.1, key=f"ratio_{i}")
            ratio_list.append(ratio)

# ------------------ Step 3: Duration of Stay ------------------
with st.expander("📆 Step 3: Duration of Stay", expanded=True):
    st.markdown("Enter days like `01-15`, or multiple ranges like `01-10,20-30`.")
    duration_list = []
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            duration = st.text_input(f"Person {i+1}", key=f"duration_{i}")
            duration_list.append(duration)

# ------------------ Step 4: Calculate ------------------
st.divider()
if st.button("🧮 Calculate Bill Distribution"):
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

    st.success("✅ Calculation complete!")
    st.subheader("💸 Bill Breakdown")
    cols = st.columns(int(roommates))
    for i in range(int(roommates)):
        with cols[i]:
            st.metric(label=f"Person {i+1}", value=f"{bill_list[i]:,.2f} VND")

    st.markdown("---")
    st.markdown(f"**🧾 Original Total:** {total:,.2f} VND")
    st.markdown(f"**📊 Calculated Total:** {total_calculated:,.2f} VND")

    if abs(discrepancy) > 0.01:
        st.warning(f"⚠️ Discrepancy of {discrepancy:.2f} VND due to rounding. Adjusting...")

        weights = [bill / total_calculated for bill in bill_list]
        adjustments = [round(discrepancy * w, 2) for w in weights]
        adjustments[-1] += discrepancy - sum(adjustments)
        bill_list = [a + b for a, b in zip(bill_list, adjustments)]

        st.subheader("🔧 Adjusted Amounts")
        cols = st.columns(int(roommates))
        for i in range(int(roommates)):
            with cols[i]:
                st.metric(label=f"Person {i+1}", value=f"{bill_list[i]:,.2f} VND (adjusted)")
