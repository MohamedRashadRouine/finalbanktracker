import os
import pandas as pd

def search_substring_in_files(base_folder, target_substring):
    found_in_files = []

    for folder_name in [
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
    ]:
        folder = os.path.join(base_folder, folder_name)
        for file_name in os.listdir(folder):
            if file_name.endswith((".xls", ".xlsx")):
                file_path = os.path.join(folder, file_name)
                df = pd.read_excel(file_path, header=None)  # Read Excel file without header

                # Check if the target substring is present in any cell content (case-insensitive)
                if df.apply(lambda x: x.astype(str).str.contains(target_substring, case=False)).stack().any():
                    found_in_files.append(file_path)

    return found_in_files

# Example usage
base_folder = "."  # Replace with the actual path
target_substring = "Date valeur à régulariser"

found_files = search_substring_in_files(base_folder, target_substring)

if found_files:
    print(f"Target substring '{target_substring}' found in the following files:")
    for file_path in found_files:
        print(file_path)
else:
    print(f"Target substring '{target_substring}' not found in any files.")
