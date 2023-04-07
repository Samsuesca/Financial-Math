import streamlit as st

def pv_fv_calculator():
    def calculate_present_value(future_value, interest_rate, nper):
        present_value = future_value / ((1 + interest_rate) ** nper)
        return present_value

    def calculate_future_value(present_value, interest_rate, nper):
        future_value = present_value * ((1 + interest_rate) ** nper)
        return future_value
    st.title('Calculadora de Valor Presente y Valor Futuro')

    option = st.selectbox('Seleccione un cálculo', ('Valor Presente', 'Valor Futuro'))

    interest = st.number_input('Tasa de Interés (%)',0.0,100.0, value=round(1.0,1), step=0.1)
    nper = st.number_input('Tiempo', min_value = 0,value=12, step=1)
    value = st.number_input('Valor', value=1000.0, step=100.0)

    if option == 'Valor Presente':
        valor_presente = calculate_present_value(value, interest/100, nper)
        st.write('Valor Presente:', f"{valor_presente:,.2f}")

    if option == 'Valor Futuro':
        valor_futuro = calculate_future_value(value, interest/100, nper)
        st.write('Valor Futuro:', f"{valor_futuro:,.2f}")

pv_fv_calculator()