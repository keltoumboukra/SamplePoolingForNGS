# Sample Pooling For NGS

* **Input**: Clariostar file with concentrations of up to 96 samples ready for NGS pooling
* **Output**: Echo or Biomek ready file to pool samples at equimolar concentration

## Installation (first time use only)

1. Clone the repository into your computer
2. Use Pip to install the requirements:

```bash
pip3 install -r requirements.txt
```

## Usage

* To run via the Terminal:  

```bash
python3 Main.py
```

* To run via via executable:

Open the executable file:

```bash
SamplePoolingForNGS/Executable/dist/Main/Main.exe
```

**Tip**: You can also create a shortcut in your location of interest.

A GUI will guide you through the process. Test input files are available in the repository.

## High-level workflow

This protocol can be run either using the Echo 525 for non genomic DNA samples, or the Biomek i7 for genomic DNA samples. Bellow is an overview of the steps involved, although the setup and transfer volumes will depend on which robot is used.

### Part 1: Qubit assay

**Input**: 1-24 Samples in a plate format
**Step Description**: Samples are mixed with Qubit working solution in a plate.
**Output**: Clariostar file with the estimated concentrations of the samples

### Part 2: Generation of samples volumes for pooling

**Input**: Clariostar file from PART 1
**Step Description**: Using the present automated data processing tool, a file will be generated to perform the transfers of the samples into the final pool. This file will be fit for either, Echo 525 or Biomek i7 depending on the option selected by the user. The following files will be generated in a folder, during the processing:

* InputFiles:
    * InputFile.csv: Copy of the file input by user
    * InputTrimmedFile.csv: Input file modified to remove standards and empty wells
* OutputFiles:
    * ExceptionsReport.csv: Report specifying wells excluded from the processing (e.g empty wells)
    * ProcessingDetails.csv: File containing the details of the data processing stages for each sample
    * EchoFile.csv or BeckmanFile.csv: Echo or Beckman ready file containing volumes of samples to be pipetted into the final pool

### Part 3: Generation of samples volumes for pooling

**Input**: Echo or Beckman ready file from PART 2
**Step Description**: The Echo or Biomek robot will transfer the volumes specified in the list into the same well.  
**Output**: Destination plate with final pool in the selected well and with the desired volume.

## Data processing details

1. Find out what max concentration in file is: c(max)
2. Calculate weights for all samples: weight(i) = c(max)/c(i)
3. Sum all the weights: Σ(i=1,i=n) weight(i)
4. Calculate weight_normalised for all samples: weight_normalised(i)=weight(i)/Σ(i=1,i=n) weight(i)
5. QC: sum of the weights normalised = 1
6. Calculate volume to pipette for each sample based on weight_normalised and final volume desired: vol_in_pool(i)=weight_norm(i) * v(f)
7. Edge case 1: sample has too high concentration ≡ vol_in_pool(i) < min_pipetting_capacity → remove sample from pool ≡ drop from output file + log issue in report file
8. Edge case 2: sample has too low concentration ≡ vol_in_pool(i) > vol_available_in_well → remove sample from pool ≡ drop from output file + log issue in report file
9. Calculate final pool concentration for QC (all v in nL and c in ng/uL): C(final pool) = (Σ(i=1,i=n) c1(i) * v1(i)) / v(final pool)

## Task List

- [ ] Install project in Foundry's Beckman workcell
- [ ] Improve Clariostar template with features like automated outlier removal
- [ ] Reduce number of decimals in output files
- [ ] Add option for user to remove list of wells
- [ ] Make the workflow easily adaptable for different numbers of columns / samples
- [ ] Write SOP (missing Echo one)
- [ ] Test low dead volume plates to reduce amount required as input for Echo + Test low volume assay plate (test robotic arm or find high profile low volume plates)

## License

[London Biofoundry](https://www.londonbiofoundry.org/)
