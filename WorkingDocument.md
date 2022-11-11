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
- Add parrameter to select which robot to use and assign pipetting range from it 
- Refine input file to remove outliers etc... + create a report file 
- Requirements file
- Install in foundry office 
- create GUI 
