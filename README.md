# Sample Pooling For NGS

Input = Clariostar file with concentrations of up to 96 samples ready for NGS pooling 
Output = Echo ready file to pool samples at equimolar concentration 

## High-level workflow 

PART 1: Qubit assay

Input = input sample plate with samples in Echo 384 PP plate in quadrant A1. Standard 1 [0 ng/uL] in B2 (30 uL) and Standard 2 [50 ng/uL] in D2 (30 uL)

Run SAMI program: Qubit_Echo_Clario. The following steps will be performed: 

Step 1. Transfer of samples and standards from the input plate to the assay plate 
Step 2. Transfer of working solution from Echo reservoir to assay plate (use 1450nl*120wells=1710nL + dv of 250 nL -> ~ 2.2ml)
Step 3. Plate shaken on BS2 for 30 sec at 2000 rpm
Step 4. Plate read on Clariostar followed by 

Output: Automatically exported file containing concentrations utmatic generation of concentrations based on standard curve and export of the data into a standard format 









