import streamlit as st

def show_recovery_actions():
    st.subheader("🔧 Recovery Actions")
    if st.button("Restart Apache Service"):
        st.success("Apache service restarted.")
    if st.button("Run Disk Cleanup"):
        st.info("Disk cleanup initiated.")