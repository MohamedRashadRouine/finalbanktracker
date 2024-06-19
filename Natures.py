import pandas as pd
import numpy as np  # Import numpy for handling NaN values

def calculate_natures(input_file, output_file):
    # Read the output.xlsx file
    output_df = pd.read_excel(input_file, parse_dates=["Date d`opération"])


    # Drop duplicates
    output_df = output_df.drop_duplicates()
    
    # Initialize nature counts
    nature_counts = {
        "Date de valeur à régulariser": 0,
        "Différence minime": 0,
        "Frais correspondants": 0,
        "Frais de tenue de compte": 0,
        "Interest": 0,
        "Northern": 0,
        "Autres": 0,
        "Total": 0,
    }

    # Initialize service counts
    service_counts = {
        "Opérations de marchés et des IAT": nature_counts.copy(),
        "Opérations du trésor": nature_counts.copy(),
        "Opérations courantes": nature_counts.copy(),
        "Paiements sur ressources extérieures": nature_counts.copy(),
        "N/Ref": nature_counts.copy(),
        "Tout les services": nature_counts.copy(),
    }

    # Iterate through rows to calculate natures and services
    for i, row in output_df.iterrows():
        # Increment Total for non-empty service column
        if pd.notna(row["Service"]):
            nature_counts["Total"] += 1
            service_counts["Tout les services"]["Total"] += 1



        # Check for "Date de valeur à régulariser"
        date_val_to_regularize = output_df[
            (output_df["Correspondant"] == row["Correspondant"]) &
            (output_df["Devise"] == row["Devise"]) &
            (output_df["Montant"] == row["Montant"]) &
            (output_df["De"] != row["De"]) &
            (output_df["Date de valeur"] != row["Date de valeur"])
        ]

        # Print information about rows contributing to the count
        print(f"Rows contributing to Date de valeur à régulariser count: {date_val_to_regularize}")
        print(f"Count for current row: {len(date_val_to_regularize)}")

        nature_counts["Date de valeur à régulariser"] += len(date_val_to_regularize)
        service_counts[row["Service"]]["Date de valeur à régulariser"] += len(date_val_to_regularize)
        service_counts["Tout les services"]["Date de valeur à régulariser"] += len(date_val_to_regularize)

        # Check for "Différence minime"
        min_diff = 0.01  # Minimum difference to consider as "Différence minime"
        max_diff = 0.99  # Maximum difference to consider as "Différence minime"
        diff_minime = output_df[
            (output_df["Correspondant"] == row["Correspondant"]) &
            (output_df["Devise"] == row["Devise"]) &
            (output_df["Date de valeur"] == row["Date de valeur"]) &
            (output_df["Montant"].apply(lambda x: min_diff <= abs(x - row["Montant"]) <= max_diff))
        ]
        nature_counts["Différence minime"] += len(diff_minime)
        service_counts[row["Service"]]["Différence minime"] += len(diff_minime)
        service_counts["Tout les services"]["Différence minime"] += len(diff_minime)

        # Check for "Frais correspondants"
        if pd.notna(row["Comment"]) and "frais" in str(row["Comment"]).lower() and "frais de tenue de compte" not in str(row["Comment"]).lower():
            nature_counts["Frais correspondants"] += 1
            service_counts[row["Service"]]["Frais correspondants"] += 1
            service_counts["Tout les services"]["Frais correspondants"] += 1

        # Check for "Frais de tenue de compte"
        if pd.notna(row["Comment"]) and ("frais de tenue de compte" in str(row["Comment"]).lower() or "charges" in str(row["Comment"]).lower()):
            nature_counts["Frais de tenue de compte"] += 1
            service_counts[row["Service"]]["Frais de tenue de compte"] += 1
            service_counts["Tout les services"]["Frais de tenue de compte"] += 1

        # Check for "Interest"
        if pd.notna(row["Comment"]) and ("interest" in str(row["Comment"]).lower() or "interet" in str(row["Comment"]).lower()):
            nature_counts["Interest"] += 1
            service_counts[row["Service"]]["Interest"] += 1
            service_counts["Tout les services"]["Interest"] += 1

        # Check for "Northern" in a case-insensitive manner
        if pd.notna(row["Correspondant"]) and "northern trust company" in str(row["Correspondant"]).lower():
            print(f"Northern row found: {row}")
            nature_counts["Northern"] += 1
            service_counts[row["Service"]]["Northern"] += 1
            service_counts["Tout les services"]["Northern"] += 1


    # Calculate "Autres"
    nature_counts["Autres"] = nature_counts["Total"] - sum(nature_counts[nature] for nature in ["Date de valeur à régulariser", "Différence minime", "Frais correspondants", "Frais de tenue de compte", "Interest", "Northern"])
    service_counts["Tout les services"]["Autres"] = nature_counts["Autres"]

    # Define the order of natures
    nature_order = [        
        "Northern",
        "Frais correspondants",
        "Date de valeur à régulariser",
        "Frais de tenue de compte",
        "Interest",
        "Différence minime",
        "Autres",
        "Total",
    ]

    # Create the Natures DataFrame with ordered columns
    natures_df = pd.DataFrame(list(nature_counts.items()), columns=["Nature", "Nombre"])
    natures_df = natures_df.set_index("Nature").reindex(nature_order).reset_index()

    # Create the Services DataFrame with ordered columns
    services_df = pd.DataFrame(columns=["Service", "Nature", "Nombre"])
    for service, counts in service_counts.items():
        for nature, count in counts.items():
            if nature != "Total" and count > 0:
                services_df = pd.concat([services_df, pd.DataFrame([{"Service": service, "Nature": nature, "Nombre": count}])], ignore_index=True)

    # Calculate the maximum content length in the "Nature" column
    max_length_natures = natures_df["Nature"].apply(len).max()
    max_length_services = services_df["Nature"].apply(len).max()

    # Apply styles to the DataFrames for a modern look
    styler_natures = natures_df.style.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#4CAF50"),
                ("color", "white"),
                ("border", "1px solid #ddd"),
                ("padding", "8px"),
                ("text-align", "left"),
            ]
        },
        {
            "selector": "tr:hover",
            "props": [
                ("background-color", "#f5f5f5"),
            ]
        },
        {
            "selector": "tr",
            "props": [
                ("border", "1px solid #ddd"),
            ]
        },
        {
            "selector": "td",
            "props": [
                ("border", "1px solid #ddd"),
                ("padding", "8px"),
                ("text-align", "left"),
            ]
        },
        {
            "selector": "td.col0",
            "props": [
                ("width", f"{max_length_natures * 10}px"),  # Adjust column width based on content length
            ]
        },
    ])

    styler_services = services_df.style.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#4CAF50"),
                ("color", "white"),
                ("border", "1px solid #ddd"),
                ("padding", "8px"),
                ("text-align", "left"),
            ]
        },
        {
            "selector": "tr:hover",
            "props": [
                ("background-color", "#f5f5f5"),
            ]
        },
        {
            "selector": "tr",
            "props": [
                ("border", "1px solid #ddd"),
            ]
        },
        {
            "selector": "td",
            "props": [
                ("border", "1px solid #ddd"),
                ("padding", "8px"),
                ("text-align", "left"),
            ]
        },
        {
            "selector": "td.col1",
            "props": [
                ("width", f"{max_length_services * 10}px"),  # Adjust column width based on content length
            ]
        },
    ])

    # Write to Natures.xlsx
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        natures_df.to_excel(writer, index=False, sheet_name="Nature par service", startrow=1, header=False)
        worksheet_natures = writer.sheets["Nature par service"]

        # Get the xlsxwriter workbook and worksheet objects
        workbook_natures = writer.book
        worksheet_natures = writer.sheets["Nature par service"]

        # Add a header format
        header_format_natures = workbook_natures.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "vcenter",
            "align": "center",
            "fg_color": "#4CAF50",
            "border": 1
        })

        # Write the column headers with the defined format
        for col_num, value in enumerate(natures_df.columns.values):
            worksheet_natures.write(0, col_num, value, header_format_natures)

        # Add a border format
        border_format_natures = workbook_natures.add_format({"border": 1})

        # Apply the border format to the entire range of data
        worksheet_natures.conditional_format(1, 0, natures_df.shape[0], natures_df.shape[1] - 1, {"type": "no_errors", "format": border_format_natures})

        # Save the styled DataFrame to Excel
        styler_natures.to_excel(writer, sheet_name="Nature par service", startrow=1, header=False, index=False)

        # Write to Services.xlsx
        services_df.to_excel(writer, index=False, sheet_name="Nature par service", startrow=1, header=False, startcol=natures_df.shape[1]+2)
        worksheet_services = writer.sheets["Nature par service"]

        # Get the xlsxwriter workbook and worksheet objects
        workbook_services = writer.book
        worksheet_services = writer.sheets["Nature par service"]

        # Add a header format
        header_format_services = workbook_services.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "vcenter",
            "align": "center",
            "fg_color": "#4CAF50",
            "border": 1
        })

        # Write the column headers with the defined format
        for col_num, value in enumerate(services_df.columns.values):
            worksheet_services.write(0, natures_df.shape[1]+2+col_num, value, header_format_services)

        # Add a border format
        border_format_services = workbook_services.add_format({"border": 1})

        # Apply the border format to the entire range of data
        worksheet_services.conditional_format(1, natures_df.shape[1]+2, services_df.shape[0], natures_df.shape[1] - 1 + services_df.shape[1] + 2, {"type": "no_errors", "format": border_format_services})

        # Save the styled DataFrame to Excel
        styler_services.to_excel(writer, sheet_name="Nature par service", startrow=1, header=False, index=False, startcol=natures_df.shape[1]+2)

if __name__ == "__main__":
    input_file = "output.xlsx"
    output_file = "Natures.xlsx"

    calculate_natures(input_file, output_file)
