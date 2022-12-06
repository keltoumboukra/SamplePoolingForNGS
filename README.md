# Sample Pooling For NGS

* **Input**: Clariostar file with concentrations of up to 96 samples ready for NGS pooling
* **Output**: Echo ready file to pool samples at equimolar concentration

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

### Part 1: Qubit assay

**Input**:
    Input samples plate with samples in Echo 384-well PP-0200 plate (25 uL) in quadrant A1.
    Standard 1 [0 ng/uL] in B2 (30 uL) and Standard 2 [50 ng/uL] in D2 (30 uL)

* Run SAMI program: Qubit_Echo_Clario. The following steps will be performed:

    * Transfer of samples and standards from the input plate to the assay plate
    * Transfer of working solution from Echo reservoir to assay plate (use 1450nl*120wells=1710nL + dv of 250 nL -> ~ 2. 2ml)
    * Plate shaken on BS2 for 30 sec at 2000 rpm
    * Plate read on Clariostar

**Output**:
    Automatically exported file containing concentrations of samples based on standard curve.

### Part 2: Generation of samples volumes for pooling

**Input**: Clariostar file from PART 1

* Run Main.py and use GUI to enter desired parametters for the pooling:
    * Input file folder location
    * Input file name
    * Desired volume for final pool
    * Desired well in 384 well plate for pooling
    * Minimum pipetting capacity (currently set to 25 nL as using Echo)
    * Volume of sample available for pipetting  (for e.g, if there is 20 uL in the well, 5000 nL is what can be available as 15 uL is the minimum working range in the PP-0200 Echo plate)

**Output**: Folder labbeled "NGSpooling-[Date]-[Time]" two folders:

* InputFiles:
    * InputFile.csv: Copy of the file input by user
    * InputTrimmedFile.csv: Input file modified to remove standards and empty wells
* OutputFiles:
    * ExceptionsReport.csv: Report specifying wells excluded from the processing (e.g empty wells)
    * ProcessingDetails.csv: File containing the details of the data processing stages for each sample
    * EchoFile.csv: Echo ready file containing volumes of samples to be pipetted into the final pool

### Part 3: Generation of samples volumes for pooling

**Input**: Echo ready file from PART 2

1. Open Echo Cherry Pick software
2. Open C:\Users\Beckman Coulter\Documents\Keltoum\Echo\NGS pooling\Pooling_Post_Qubit.ecp
3. In the "Pick List" section, import the Echo file from PART 2
4. Press "Run"
5. Follow the instruction on the Echo software and place on the tray the:
    * Source plate: Echo 384-well PP-0200 plate containing the input samples (the same plate as the one used in PART 1)
    * Destination plate: Greiner 384 PS 781096 plate

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

- [ ] Add parrameter to select which robot to use and assign pipetting range from it
- [ ] Install project in Foundry's Beckman workcell
- [ ] Improve Clariostar template with features like automated outlier removal
- [ ] Reduce number of decimals in output files
- [ ] Add option for user to remove list of wells
- [ ] Make the workflow easily adaptable for different numbers of columns / samples
- [ ] Write SOP
- [ ] Test low dead volume plates to reduce amount required as input for Echo + Test low volume assay plate (test robotic arm or find high profile low volume plates)

## License

[London Biofoundry](https://www.londonbiofoundry.org/)
