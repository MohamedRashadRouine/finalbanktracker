

import os
import pandas as pd

def process_excel_files(folder_path, output_file):
    final_output_df = pd.DataFrame(columns=["Service", "De", "Compte", "Correspondant", "Date d`opération", "Montant", "Date de valeur", "Signe", "Devise", "Comment"])

    correspondant_folders = [
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

    for correspondant_folder in correspondant_folders:
        folder = os.path.join(folder_path, "Correspondants", correspondant_folder)
        if os.path.exists(folder) and os.listdir(folder):
            for file_name in os.listdir(folder):
                if file_name.endswith((".xls", ".xlsx")):
                    file_path = os.path.join(folder, file_name)
                    df = pd.read_excel(file_path, parse_dates=["Date d`opération"])

                    # Convert the 'Date d`opération' column to datetime with dayfirst=True
                    df["Date d`opération"] = pd.to_datetime(df["Date d`opération"], dayfirst=True)

                    # Process data based on correspondant_folder
                    if "4757.890.123 OMEGA INVEST - VIENNA" in correspondant_folder:
                        # Process '4757.890.123 OMEGA INVEST - VIENNA' data directly
                        service_name = "Opérations de marchés et des IAT"

                        # Use a try-except block to handle potential KeyError
                        try:
                            # For Omega Invest, use the process_correspondant_data function
                            process_data = process_correspondant_data(df, correspondant_folder)
                            process_data["Service"] = service_name  # Update the "Service" column for Omega Invest
                            process_data["Compte"] = "4757.890.123"  # Update the "Compte" column for Omega Invest
                            process_data["Correspondant"] = "OMEGA INVEST - VIENNA"  # Update the "Correspondant" column for Omega Invest
                        except KeyError:
                            process_data = pd.DataFrame(columns=["Service", "De", "Compte", "Correspondant", "Date d`opération", "Montant", "Date de valeur", "Signe", "Devise", "Comment"])

                    else:
                        # Process data for other folders
                        process_data = process_correspondant_data(df, correspondant_folder)

                    final_output_df = pd.concat([final_output_df, process_data], ignore_index=True)
        else:
            # Handle empty folder
            compte, correspondant = correspondant_folder.split(' ', 1)
            empty_folder_data = pd.DataFrame({
                "Service": ["N/Ref"],
                "De": [None],  # Add this line to set "De" column
                "Compte": [compte],
                "Correspondant": [correspondant],
                "Date d`opération": [pd.NaT],
                "Montant": [0],
                "Date de valeur": [pd.NaT],
                "Signe": [pd.NaT],
                "Devise": [pd.NaT],
                "Comment": [""]
            })
            final_output_df = pd.concat([final_output_df, empty_folder_data], ignore_index=True)


    # Remove duplicate lines
    final_output_df = final_output_df.drop_duplicates().reset_index(drop=True)

    # Check and update service names based on conditions
    final_output_df.loc[(final_output_df['Service'] == 'N/Ref') & (final_output_df['Comment'].str.contains('TS-P')), 'Service'] = 'Paiements sur ressources extérieures'
    final_output_df.loc[(final_output_df['Service'] == 'N/Ref') & (final_output_df['Comment'].str.contains('T016')), 'Service'] = 'Opérations de marchés et des IAT'

    # Styler to format the output DataFrame
    styler = final_output_df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
    styler.set_properties(**{'text-align': 'center'}).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'center')]
    }]).set_properties(subset=["Service", "De", "Compte", "Correspondant", "Date d`opération", "Montant", "Date de valeur", "Signe", "Devise", "Comment"], **{'width': '170px'})

    print("Final Output DataFrame:")
    print(styler)

    # Using ExcelWriter with xlsxwriter engine
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        final_output_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=1, header=False)
        worksheet = writer.sheets['Sheet1']

        # Autofit columns
        for i, col in enumerate(final_output_df.columns):
            max_len = max(final_output_df[col].astype(str).apply(len).max(), len(col))
            writer.sheets['Sheet1'].set_column(i, i, max_len + 4)  # Adding a little extra space

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # Add a header format
        header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center', 'fg_color': '#D7E4BC', 'border': 1})

        # Write the column headers with the defined format
        for col_num, value in enumerate(final_output_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Add a border format
        border_format = workbook.add_format({'border': 1})

        # Apply the border format to the entire range of data
        worksheet.conditional_format(1, 0, final_output_df.shape[0], final_output_df.shape[1] - 1, {'type': 'no_errors', 'format': border_format})

def identify_service_name(reference_columns):
    service_mapping = {'L221': 'Opérations de marchés et des IAT', 'L213': 'Paiements sur ressources extérieures', 'L212': 'Opérations du trésor', 'L211': 'Opérations courantes'}

    for col in reference_columns:
        if isinstance(col, str) and any(prefix in col for prefix in service_mapping):
            return service_mapping[next(prefix for prefix in service_mapping if prefix in col)]

    return "N/Ref"

def process_correspondant_data(df, correspondant_folder):
    reference_columns = [col for col in df.columns if col.startswith('Référence')]
    print("Reference Columns:", reference_columns)

    # Use str.contains to filter rows
    selected_lines = df[df[reference_columns].apply(lambda x: any(isinstance(s, str) and s.strip() != '' for s in x.dropna()), axis=1)].reset_index(drop=True)

    print("Selected Lines:")
    print(selected_lines)

    output_data = pd.DataFrame(columns=["Service", "De", "Compte", "Correspondant", "Date d`opération", "Montant", "Date de valeur", "Signe", "Devise", "Comment"])

    # Process lines where service is identified
    for index, row in selected_lines.iterrows():
        service_name = identify_service_name(row[reference_columns])
        date_operation = row["Date d`opération"].to_pydatetime()  # Convert to Python datetime
        montant = row["Montant"]
        date_valeur = row["Date de valeur"]
        signe = row["Signe"]
        devise = row["Devise"]
        comment = ' '.join(row[reference_columns].astype(str))

        # Extract Compte and Correspondant from the folder name
        compte, correspondant = correspondant_folder.split(' ', 1)

        output_data = pd.concat([output_data, pd.DataFrame({
            "Service": [service_name],
            "De": [row["De"]],  # Add this line to set "De" column
            "Compte": [compte],
            "Correspondant": [correspondant],
            "Date d`opération": [date_operation],
            "Montant": [montant],
            "Date de valeur": [date_valeur],
            "Signe": [signe],
            "Devise": [devise],
            "Comment": [comment]
        })], ignore_index=True)

    return output_data

# Example usage
if __name__ == "__main__":
    folder_path = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(folder_path, "output.xlsx")
    process_excel_files(folder_path, output_file)
