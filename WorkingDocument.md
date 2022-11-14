High level strategy:
1. Find out what max concentration in file is: c(max)
2. Calculate weights for all samples: weight(i) = c(max)/c(i)
3. Sum all the weights: Σ(i=1,i=n) weight(i)
4. Calculate weight_normalised for all samples: weight_norm(i)=weight(i)/Σ(i=1,i=n) weight(i)
5. QC: sum of the weights normalised = 1 
6. Calculate volume to pipette for each sample based on weight_norm and final volume desired: vol_in_pool(i)=weight_norm(i)*v(f)
7. Edge case 1: sample has too high concentration ≡ vol_in_pool(i) < min_pipetting_capacity → remove sample from pool ≡ drop from output file + log issue in report file
8. Edge case 2: sample has too low concentration ≡ vol_in_pool(i) > vol_available_in_well → remove sample from pool ≡ drop from output file + log issue in report file

To Do's:
- Remove standards from the input file
- Add parrameter to select which robot to use and assign pipetting range from it 
- Refine input file to remove outliers etc... + create a report file 
- Requirements file
- Install in foundry office 
- Create GUI 
- Improve Clariostar template with features like automated outlier removal 

Workflow:

PART 1: Run Qubit assay

Input = input sample plate with samples in Echo 384 PP plate in quadrant A1. Standard in B2 (same vol as samples). Working solution in D2 with 18 uL to be transfered so a min of 33 uL available to include 15 uL dead volume.  

Run SAMI program: Qubit_Echo_Clario
Step 1. Transfer of samples and standards from the input plate to the assay plate (Greiner 384)
Step 2. Transfer of working solution from Echo reservoir to assay plate (use 1450nl*120wells=1710nL + dv of 250 nL -> ~ 2ml)
Step 3. Plate shaken on BS2 for 30 sec at 2000 rpm 
Step 4. Plate read on Clariostar with KB_Qubit384_1quadrant program

Output = file containing concentrations for the 96 samples on the plate saved in "C:\Users\Beckman Coulter\Documents\Keltoum\Clariostar\AutomatedExportQubit"

PART 2: Run data processing and normalisation 

Input = file output from the Part 1

Step 1: Plug the file output from part 1 into the Echo program using the appropriate parametters for the pooling: C:\Users\Beckman Coulter\Documents\Keltoum\Echo\NGS pooling
Step 2: Launch the Echo program using:
    1. Source plate: Input plate with samples in 
    2. Destination plate: Greiner 384-well plate 








