
def exp():
    validated = {'user_id': 'USR12345', 'sample_id': 'SAMPLE-001', 'trace_id': 'trace_185a7a59-eb02-4cb9-82a4-ef7c4a9c7ad6', 'biomarkers': {'ApoB': 102, 'LDL-P': 1650, 'LDL-C': 132, 'Lp(a)': 28, 'HbA1c': 5.8, 'Fasting Glucose': 98, 'Fasting Insulin': 9.1, 'HOMA-IR': 2.2, 'CRP High Sensitivity': 1.9, 'MPO': 410, 'IL-6': 3.2, 'Triglycerides': 160, 'HDL Cholesterol': 42, 'ApoA1': 128, 'Cholesterol Total': 210, 'Non-HDL Cholesterol': 168, 'ESR': 12, 'Ferritin': 185, 'Ox-LDL': 62, 'GGT': 38, 'Creatinine': 1.02, 'eGFR': 91, 'Hemoglobin': 14.8, 'WBC Count': 6.7, 'Platelet Count': 255, 'RDW': 12.8, 'Neutrophil/Lymphocyte Ratio': 2.1, 'Sodium': 138, 'Potassium': 4.3, 'Chloride': 103, 'ALT (SGPT)': 28, 'AST (SGOT)': 32, 'Alkaline Phosphatase': 84, 'Uric Acid': 6.2, 'Fructosamine': 235, 'C-peptide': 2.1, '25-OH Vitamin D': 24, 'Lactate Dehydrogenase': 180, 'hs-Troponin': 12, 'NT-proBNP': 55}, 'metadata': {'age': 42, 'sex': 'male', 'lab_name': 'ABC Diagnostics', 'sample_collected_at': '2025-12-08T09:30:00Z', 'fasting_status': 'fasting', 'medications': [], 'lifestyle': [], 'collection_notes': 'No issues reported'}}

    for alias_name in validated['biomarkers'].keys():
        print(alias_name)


if __name__ == '__main__':
    exp()
