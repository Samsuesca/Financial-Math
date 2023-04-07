import streamlit as st
import numpy_financial as npf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def crear_diagrama_flujo_pv(pv,pmt, nper, interest, tipo,scale = 0.4):
    fig, ax = plt.subplots(figsize=(10,5))
    fig.set_facecolor('white')
    # fig.patch.set_visible(False)
    ax.axis('off')
    ax.set_title('Diagrama de Flujo de Efectivo', fontsize=15)
    ax.axhline(y=0, color='gray', linestyle='--')
    if tipo == 'begin':
        cashflows = np.repeat(-pmt*scale*3, nper)
        stem = ax.stem(cashflows, linefmt='C0-', markerfmt='C0o', basefmt='C0-',label='Pagos')
        stem[1].set_color('Orange') 
        stem = ax.stem([pv*scale], linefmt='C0-', markerfmt='C0o', basefmt='C0-')
        stem[1].set_color('Blue') 
    elif tipo == 'end':
        cashflows = np.repeat(-pmt*scale*3, nper)
        cashflows = np.append([0], cashflows)
        stem = ax.stem(cashflows, linefmt='C1-', markerfmt='C1o', basefmt='C1-',label='Pagos')
        stem[1].set_color('Orange')
        stem = ax.stem([pv*scale], linefmt='C0-', markerfmt='C0o', basefmt='C0-')
        stem[1].set_color('Blue') 
        ax.set_xlim([-0.5, nper + 0.5])
    ax.annotate(format(pv, '.2f'), xy=(0, pv*scale), xytext=(-15, 5), textcoords='offset points', ha='right', va='bottom')
    for i in range(0, nper, 5):
        ax.annotate(format(cashflows[i]/(-scale*3), '.2f'), xy=(i, cashflows[i]), xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom')
    ax.text(nper/2, pv*0.5*scale, f"Tasa de interés fija: {interest:.2f}%", ha='center', fontsize=12)
    return fig

def crear_diagrama_flujo_fv(fv,pmt, nper, interest, tipo,scale =0.4):
    fig, ax = plt.subplots(figsize=(10,5))
    fig.set_facecolor('white')
    # fig.patch.set_visible(False)
    ax.axis('off')
    ax.set_title('Diagrama de Flujo de Efectivo', fontsize=15)
    ax.axhline(y=0, color='gray', linestyle='--')
    if tipo == 'begin':
        cashflows = np.repeat(pmt*scale*3, nper)
        stem = ax.stem(cashflows, linefmt='C0-', markerfmt='C0o', basefmt='C0-',label='Pagos')
        stem[1].set_color('Orange') 
        stem = ax.stem(nper,[-fv*scale], linefmt='C0-', markerfmt='C0o', basefmt='C0-')
        stem[1].set_color('Blue') 
    elif tipo == 'end':
        cashflows = np.repeat(pmt*1.2, nper)
        cashflows = np.append([0], cashflows)
        stem = ax.stem(cashflows, linefmt='C1-', markerfmt='C1o', basefmt='C1-',label='Pagos')
        stem[1].set_color('Orange')
        stem = ax.stem(nper,[-fv*scale], linefmt='C0-', markerfmt='C0o', basefmt='C0-')
        stem[1].set_color('Blue') 
        ax.set_xlim([-0.5, nper + 0.5])
    ax.annotate(format(fv, '.2f'), xy=(nper, -fv*scale), xytext=(-15, 5), textcoords='offset points', ha='right', va='bottom')
    for i in range(0, nper, 5):
        ax.annotate(format(cashflows[i]/1.2, '.2f'), xy=(i, cashflows[i]), xytext=(-5, 5), textcoords='offset points', ha='right', va='bottom')
    ax.text(nper/2, -fv*scale*0.5, f"Tasa de interés fija: {interest:.2f}%", ha='center', fontsize=12)
    return fig

def tabla_amortizacion_pv(pv,pmt,nper,interest,tipo = 'end'):
    data = {'Saldo Inicial': [],'Cuota': [], 'Pago de Intereses': [], 'Pago de Capital': [], 'Saldo Final': []}
    balance = pv
    if tipo == 'begin':
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

def tabla_amortizacion_fv(pmt,nper,interest,tipo = 'end'):
    data = {'Saldo Inicial': [],'Cuota': [], 'Intereses Obtenidos': [], 'Total Depósito': [], 'Saldo Total': []}
    balance = 0
    if tipo == 'begin':
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
        if tipo == 'begin' and i == nper-1:
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
    tipo = 'end'
if option == 'Anualidad Anticipada':
    tipo = 'begin'
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

    pv = -1*float(npf.pv(interest/100,nper,pmt,fv=-fv,when=tipo))
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

    fv = -1*float(npf.fv(interest/100,nper,pmt,pv=-pv,when=tipo))
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
    pmt = -1*float(npf.pmt(interest/100,nper,pv=pv,fv=fv,when=tipo))
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

    interest = float(npf.rate(nper,-pmt,pv,fv,when=tipo))
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

    nper = float(npf.nper(interest/100,-pmt,pv,fv,when=tipo))
    st.write('---')
    c1,col,c2 = st.columns([1.5,2,1])
    with col:
        st.metric('Número de Periodos', f"{nper:,.2f}")

st.write('---')
st.write('Diagrama de Flujo')
if target != 'Valor Futuro':
    fig = crear_diagrama_flujo_pv(pv,pmt,nper,interest,tipo)
    st.pyplot(fig)
else:
    fig = crear_diagrama_flujo_fv(fv,pmt,nper,interest,tipo)
    st.pyplot(fig)


st.write('---')
st.write('Tabla de Amortización')
if target != 'Valor Futuro':
    df = tabla_amortizacion_pv(pv,pmt,nper,interest,tipo)
    st.dataframe(df, 700, 500)
else:
    df = tabla_amortizacion_fv(pmt,nper,interest,tipo)
    st.dataframe(df, 700, 500)

