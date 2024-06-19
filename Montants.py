import pandas as pd

# Read the output.xlsx file
output_df = pd.read_excel("output.xlsx")

# Group by 'Devise', 'De', 'Signe' and calculate the sum of 'Montant'
result_df = output_df.groupby(['Devise', 'De', 'Signe'])['Montant'].sum().reset_index()

# Save the result to Montants.xlsx
result_df.to_excel("Montants.xlsx", index=False)
