import os

# Define old and new folder names
old_names = [
    '5021.070.978 NATIXIS - PARIS',
    '5021.072.978 SOCIETE GENERALE-PARIS',
    '5021.075.978 UNION TUNISIENNE DE BANQUES-PARIS',
    '5021.081.756 BANQUE NATIONALE SUISSE-ZURICH',
    '5021.169.840 CITIBANK-TUNIS',
    '5021.187.840 THE RIGGS NATIONAL BANK WASHINGTON',
    '5021.346.392 EUROCLEAR - BRUXELLES',
    '5021.346.840 EUROCLEAR-BRUXELLES',
    '5021.346.978 EUROCLEAR-BRUXELLES',
    '5021.369.504 BANK EL MAGHRIB CV - UMA',
    '5021.449.840 CLEARSTREAM BANKING LUXEMBOURG',
    '5021.449.978 CLEARSTREAM BANKING LUXEMBOURG',
    '5021.041.756 CREDIT SUISSE ZURICH',
    '5021.068.978 BANQUE DE FRANCE-PARIS',
    '5021.125.978 COMMERZBANK-FRANKFURT',
    '5021.003.840 CITIBANK-NEW-YORK',
    '5021.007.840 FEDERAL RESERVE BANK OF NEW-YORK - NEW-YORK',
    '5021.009.840 DEUTSCHE BANK TRUST COMPANY AMERICAS NEW-YORK',
    '5021.069.978 BANQUE NATIONALE DE PARIS-PARIS',
    '5021.062.682 ARAB NATIONAL BANK-RIADH',
    '5021.024.978 DEUTSCHE BUNDESBANK-FRANKFURT',
    '5021.034.978 INTESA SANPAOLO SPA -MILAN',
    '5021.053.752 SVERIGES RIKSBANK-STOCKHOLM',
    '5021.056.978 UNICREDIT BANK AUSTRIA AG - VIENNE',
    '5021.059.978 NORDEA BANK HELSINKI',
    '5021.061.978 BANCO SANTANDER S.A-MADRID',
    '5021.346.756 EUROCLEAR - BRUXELLES',
    '5021.463.634 QATAR NATIONAL BANK - DOHA',
    '5021.129.682 THE NATIONAL COMMERCIAL BANK-JEDDAH',
    '5021.477.124 BANK OF MONTREAL - TORONTO',
    '5021.449.392 CLEARSTREAM BANKING LUXEMBOURG',
    '5021.475.840 NORTHERN TRUST COMPANY',
    '5021.346.826 EUROCLEAR BRUXELLES',
    '5021.449.826 CLEARSTREAM BANKING LUXEMBOURG',
    '5021.472.978 BANQUE CENTRALE DU LUXEMBOURG',
    '5021.055.578 DEN NORSKE BANK-OSLO',
    '5021.051.752 SKANDINAVISKA ENSKILDA BANKEN - STOCKHOLM',
    '5021.132.784 U.A.E CENTRAL BANK ABU-DHABI',
    '5021.042.756 UNION DE BANQUE SUISSE ZURICH',
    '5021.338.826 BANK OF ENGLAND-LONDON',
    '5021.022.978 DEUTSCHE BANK-FRANKFURT',
    '5021.100.392 BANK OF TOKYO-MITSUBISHI UFJ,LTD-TOKYO',
    '5021.495.840 DEUTSCHE BANK AG- NEW YORK',
    '5021.480.156 BANK OF CHINA HONG KONG',
    '5021.155.826 JPMORGAN BANK LONDRES',
    '5021.181.978 CREDIT AGRICOLE CIB',
    '5021.004.840 JPMORGAN BANK',
    '5021.493.208 NORDEA BANK DANMARK AS',
    '5021.069.826 BNP'
]

new_names = [
    '1234.567.890 ALPHA BANK - ATHENS',
    '2345.678.901 BETA FINANCE - LONDON',
    '3456.789.012 GAMMA TRUST - NEW YORK',
    '4567.890.123 DELTA INVEST - ZURICH',
    '5678.901.234 EPSILON BANK - PARIS',
    '6789.012.345 ZETA CREDIT - TOKYO',
    '7890.123.456 ETA HOLDINGS - DUBAI',
    '8901.234.567 THETA CAPITAL - SINGAPORE',
    '9012.345.678 IOTA SAVINGS - TORONTO',
    '0123.456.789 KAPPA INVESTMENTS - SYDNEY',
    '1324.567.890 LAMBDA SECURITIES - FRANKFURT',
    '2435.678.901 MU ASSET MANAGEMENT - HONG KONG',
    '3546.789.012 NU WEALTH - SAN FRANCISCO',
    '4657.890.123 XI BANKING - MUMBAI',
    '5768.901.234 OMICRON FUNDS - SAO PAULO',
    '6879.012.345 PI FINANCIAL - JOHANNESBURG',
    '7980.123.456 RHO EQUITIES - SHANGHAI',
    '8091.234.567 SIGMA CREDIT - MOSCOW',
    '9202.345.678 TAU HOLDINGS - RIO DE JANEIRO',
    '0313.456.789 UPSILON ASSETS - SEOUL',
    '1424.567.890 PHI CAPITAL - MEXICO CITY',
    '2535.678.901 CHI FUNDS - DUBLIN',
    '3646.789.012 PSI BANK - AMSTERDAM',
    '4757.890.123 OMEGA INVEST - VIENNA',
    '5868.901.234 ZETA HOLDINGS - HELSINKI',
    '6979.012.345 ETA TRUST - OSLO',
    '7080.123.456 IOTA FINANCE - STOCKHOLM',
    '8191.234.567 KAPPA BANK - COPENHAGEN',
    '9202.345.678 LAMBDA SECURITIES - LUXEMBOURG',
    '0313.456.789 MU BANK - BRUSSELS',
    '1424.567.890 NU CAPITAL - ZURICH',
    '2535.678.901 XI TRUST - GENEVA',
    '3646.789.012 OMICRON BANK - VIENNA',
    '4757.890.123 PI WEALTH - TORONTO',
    '5868.901.234 RHO INVEST - BRUSSELS',
    '6979.012.345 SIGMA CAPITAL - OSLO',
    '7080.123.456 TAU SECURITIES - STOCKHOLM',
    '8191.234.567 UPSILON BANK - COPENHAGEN',
    '9202.345.678 PHI TRUST - LUXEMBOURG',
    '0313.456.789 CHI CAPITAL - LONDON',
    '1424.567.890 PSI FUNDS - FRANKFURT',
    '2535.678.901 OMEGA BANK - PARIS',
    '3646.789.012 ZETA FINANCE - BERLIN',
    '4757.890.123 ETA CAPITAL - BRUSSELS',
    '5868.901.234 IOTA HOLDINGS - LUXEMBOURG',
    '6979.012.345 KAPPA TRUST - LONDON',
    '7080.123.456 LAMBDA WEALTH - ZURICH',
    '8191.234.567 MU FUNDS - VIENNA',
    '9202.345.678 NU BANK - OSLO',
    '0313.456.789 XI SECURITIES - GENEVA'
]

# Get the current working directory
folder_path = os.path.dirname(__file__)
print(f"Script directory: {folder_path}")

# Rename the folders
for old_name, new_name in zip(old_names, new_names):
    old_folder = os.path.join(folder_path, old_name)
    new_folder = os.path.join(folder_path, new_name)
    if os.path.exists(old_folder):
        os.rename(old_folder, new_folder)
        print(f"Renamed '{old_name}' to '{new_name}'")
    else:
        print(f"Folder '{old_name}' does not exist")


print("Renaming complete.")