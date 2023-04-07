import streamlit as st
import numpy_financial as npf
import pandas as pd

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


def anualidades():
    def tabla_amortizacion_pv(pv,pmt,nper,interest,type = 'end'):
        data = {'Saldo Inicial': [],'Cuota': [], 'Pago de Intereses': [], 'Pago de Capital': [], 'Saldo Final': []}
        balance = pv
        if type == 'begin':
            data['Saldo Inicial'].append(balance)
            data['Cuota'].append(round(pmt,2))
            data['Pago de Intereses'].append(0)
            data['Pago de Capital'].append(round(pmt,2))
            balance -= pmt
            nper = nper - 1
            data['Saldo Final'].append(round(balance,2))
        else:
            data['Saldo Inicial'].append(balance)
            data['Cuota'].append(0)
            data['Pago de Intereses'].append(0)
            data['Pago de Capital'].append(0)
            data['Saldo Final'].append(balance)
        for i in range(int(nper)):
            interest_payment = balance * (interest/100)
            principal_payment = pmt - interest_payment
            balance -= principal_payment
            data['Saldo Inicial'].append(round(balance + principal_payment,2))
            data['Cuota'].append(round(pmt,2))
            data['Pago de Intereses'].append(round(interest_payment,2))
            data['Pago de Capital'].append(round(principal_payment,2))
            data['Saldo Final'].append(round(balance,2))
        df = pd.DataFrame(data, index=range(nper+1))
        return df

    def tabla_amortizacion_fv(pmt,nper,interest,type = 'end'):
        data = {'Saldo Inicial': [],'Cuota': [], 'Intereses Obtenidos': [], 'Total Depósito': [], 'Saldo Total': []}
        balance = 0
        if type == 'begin':
            data['Saldo Inicial'].append(0)
            data['Cuota'].append(round(pmt,2))
            data['Intereses Obtenidos'].append(0)
            data['Total Depósito'].append(round(pmt,2))
            balance += pmt
            nper = nper
            data['Saldo Total'].append(round(balance,2))
        else:
            data['Saldo Inicial'].append(0)
            data['Cuota'].append(0)
            data['Intereses Obtenidos'].append(0)
            data['Total Depósito'].append(0)
            data['Saldo Total'].append(0)
        for i in range(int(nper)):    
            interest_payment = balance * (interest/100)
            data['Saldo Inicial'].append(round(balance,2))
            if type == 'begin' and i == nper-1:
                pmt = 0    
            principal_payment = pmt + interest_payment
            balance += principal_payment
            data['Cuota'].append(round(pmt,2))
            data['Intereses Obtenidos'].append(round(interest_payment,2))
            data['Total Depósito'].append(round(principal_payment,2))
            data['Saldo Total'].append(round(balance,2))
        df = pd.DataFrame(data, index=range(nper+1))
        return df

    st.title('Anualidades')
    st.write('---')
    option = st.selectbox('Seleccione el tipo de anualidad', ('Anualidad Ordinaria', 'Anualidad Anticipada'))
    if option == 'Anualidad Ordinaria':
       type = 'end'
    if option == 'Anualidad Anticipada':
        type = 'begin'
    st.write('---')
    target = st.selectbox('Seleccione lo que quiere obtener', ('Valor Presente', 'Valor Futuro','Pago','Interés','Número Periodos'))
    st.write('---')

    if target == 'Valor Presente':
        col1, col2 = st.columns(2)
        with col1:
            pmt = st.number_input('Ingrese el valor de la anualidad', min_value=0.0,value=1000.0, step=100.0)
            interest = st.number_input('Ingrese la tasa de interés (%)',0.0,100.0, value=round(1.0,1), step=0.1)
        with col2:
            nper = st.number_input('Ingrese el número de pagos', min_value=1, value=12, step=1)
            fv = st.number_input('Ingrese el valor futuro', value=0.0, step=100.0)

        pv = -1*float(npf.pv(interest/100,nper,pmt,fv=-fv,when=type))
        st.write('---')
        c1,col,c2 = st.columns([1.5,2,1])
        with col:
            st.metric('Valor Presente:', f"{pv:,.2f}")


    elif target == 'Valor Futuro':
        col1, col2 = st.columns(2)
        with col1:
            pmt = st.number_input('Ingrese el valor de la anualidad',min_value=0.0, value=1000.0, step=100.0)
            interest = st.number_input('Ingrese la tasa de interés (%)',0.0,100.0, value=round(1.0,1), step=0.1)
        with col2:
            nper = st.number_input('Ingrese el número de pagos', min_value=1, value=12, step=1)
            pv = st.number_input('Ingrese el valor presente', value=0.0, step=100.0)

        fv = -1*float(npf.fv(interest/100,nper,pmt,pv=-pv,when=type))
        st.write('---')
        c1,col,c2 = st.columns([1.5,2,1])
        with col:
            st.metric('Valor Futuro:', f"{fv:,.2f}")

    elif target == 'Pago':
        col1, col2 = st.columns(2)
        with col1:
            pv = st.number_input('Ingrese el valor presente',min_value=0.0, value=1000.0, step=100.0)
            interest = st.number_input('Ingrese la tasa de interés (%)',0.0,100.0, value=round(1.0,1), step=0.1)
        with col2:
            nper = st.number_input('Ingrese el número de pagos', min_value=1, value=12, step=1)
            fv = st.number_input('Ingrese el valor futuro', min_value=0.0, value=0.0, step=100.0)
        pmt = -1*float(npf.pmt(interest/100,nper,pv=pv,fv=fv,when=type))
        st.write('---')
        c1,col,c2 = st.columns([1.5,2,1])
        with col:
            st.metric('Pago:', f"{pmt:,.2f}")

    elif target == 'Interés':
        col1, col2 = st.columns(2)
        with col1:
            pv = st.number_input('Ingrese el valor presente',min_value=0.0, value=1000.0, step=100.0)
            pmt = st.number_input('Ingrese el valor de la anualidad',min_value=0.0, value=1000.0, step=100.0)
        with col2:
            nper = st.number_input('Ingrese el número de pagos', min_value=1, value=12, step=1)
            fv = st.number_input('Ingrese el valor futuro', min_value=0.0, value=0.0, step=100.0)

        interest = float(npf.rate(nper,-pmt,pv,fv,when=type))
        st.write('---')
        c1,col,c2 = st.columns([1.5,2,1])
        with col:
            st.metric('Tasa de interés (%):', f"{interest*100:,.2f} %")

    elif target == 'Número Periodos':
        col1, col2 = st.columns(2)
        with col1:
            pv = st.number_input('Ingrese el valor presente',min_value=0.0, value=1000.0, step=100.0)
            pmt = st.number_input('Ingrese el valor de la anualidad',min_value=0.0, value=1000.0, step=100.0)
        with col2:
            interest = st.number_input('Ingrese la tasa de interés (%)',0.0,100.0, value=round(1.0,1), step=0.1)
            fv = st.number_input('Ingrese el valor futuro', min_value=0.0, value=0.0, step=100.0)

        nper = float(npf.nper(interest/100,-pmt,pv,fv,when=type))
        st.write('---')
        c1,col,c2 = st.columns([1.5,2,1])
        with col:
            st.metric('Número de Periodos', f"{nper:,.2f}")

    st.write('---')
    st.write('Tabla de Amortización')
    if target != 'Valor Futuro':
        df = tabla_amortizacion_pv(pv,pmt,nper,interest,type)
        st.dataframe(df, 700, 500)
    else:
        df = tabla_amortizacion_fv(pmt,nper,interest,type)
        st.dataframe(df, 700, 500)

pages = {
    "Valor Presente/Futuro": pv_fv_calculator,
    "Anualidades": anualidades
}

st.sidebar.title("Navegación")
selection = st.sidebar.radio("Seleccione una herramienta", list(pages.keys()))
page = pages[selection]
page()
