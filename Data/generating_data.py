from get_data import *


lista_teste = [
'ABEV3','ASAI3','AZUL4','BTOW3','B3SA3','BIDI11','BBSE3','BRML3','BBDC4','BRAP4','BBAS3','BRKM5','BRFS3','BPAC11',
'CRFB3','CCRO3','CMIG4','HGTX3','CIEL3','COGN3','CPLE6','CSAN3','CPFE3','CVCB3','CYRE3','ECOR3','ELET3','EMBR3','ENBR3','ENGI11','ENEV3','EGIE3',
'EQTL3','EZTC3','FLRY3','GGBR4','GOAU4','GOLL4','NTCO3','HAPV3','HYPE3','IGTA3','GNDI3','IRBR3','ITSA4','ITUB4','JBSS3','JHSF3',
'KLBN11','RENT3','LCAM3','LWSA3','LAME4','LREN3','MGLU3','MRFG3','BEEF3','MRVE3','MULT3','PCAR3','PETR4','BRDT3','PRIO3',
'QUAL3','RADL3','RAIL3','SBSP3','SANB11','CSNA3','SULA11','SUZB3','TAEE11','VIVT3','TIMS3','TOTS3','UGPA3','USIM5','VALE3','VVAR3','WEGE3','YDUQ3'
]

# baixando preços
df_only = get_equity_data(lista_teste, start_date = '2010-01-01')
df_only = df_only['adjclose']
df_only.to_pickle("./equity_only.pkl")

# baixando cdi
df_cdi = get_sgs_data([4389])
df_cdi.to_pickle('./cdi.pkl')

# baixando ibov
df_ibov = get_equity_data(['^BVSP'], start_date = '2010-01-01')
df_ibov = df_ibov['adjclose']
df_ibov.to_pickle("./ibov.pkl")