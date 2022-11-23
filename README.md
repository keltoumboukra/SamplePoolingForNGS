# Sample Pooling For NGS

Input = Clariostar file with concentrations of up to 96 samples ready for NGS pooling 
Output = Echo ready file to pool samples at equimolar concentration 

## Installation 

1. Clone the repository into your computer
2. Use Pip to install the requirements: 

```bash
pip install requirements.txt
```

## Usage

To run: 

```bash
python3 Main.py 
```

A GUI will guide you through the process. Test input files are available in the repository. 

## High-level workflow 

### PART 1: Qubit assay

Input = Input samples plate with samples in Echo 384-well PP-0200 plate (25 uL) in quadrant A1. Standard 1 [0 ng/uL] in B2 (30 uL) and Standard 2 [50 ng/uL] in D2 (30 uL)

Run SAMI program: Qubit_Echo_Clario. The following steps will be performed: 

    - Step 1. Transfer of samples and standards from the input plate to the assay plate 
    - Step 2. Transfer of working solution from Echo reservoir to assay plate (use 1450nl*120wells=1710nL + dv of 250 nL -> ~ 2. 2ml)
    - Step 3. Plate shaken on BS2 for 30 sec at 2000 rpm
    - Step 4. Plate read on Clariostar

Output: Automatically exported file containing concentrations of samples based on standard curve. 

### PART 2: Generation of samples volumes for pooling

Input = Clariostar file from PART 1

Run Main.py and use GUI to enter desired parametters for the pooling:
    - Input file folder location
    - Input file name
    - Desired volume for final pool
    - Desired well in 384 well plate for pooling 
    - Minimum pipetting capacity (currently set to 25 nL as using Echo)
    - Volume of sample available for pipetting  (for e.g, if there is 20 uL in the well, 5000 nL is what can be available as 15 uL is the minimum working range in the PP-0200 Echo plate)

Output = Folder labbeled "NGSpooling-[Date]-[Time]" two folders:
    1. InputFiles:
        - InputFile.csv: Copy of the file input by user
        - InputTrimmedFile.csv: Input file modified to remove standards and empty wells 
    2. OutputFiles:
        - ExceptionsReport.csv: Report specifying wells excluded from the processing (e.g empty wells)
        - ProcessingDetails.csv: File containing the details of the data processing stages for each sample
        - EchoFile.csv: Echo ready file containing volumes of samples to be pipetted into the final pool

### PART 3: Generation of samples volumes for pooling

Input = Echo ready file from PART 2

    1. Open Echo Cherry Pick software
    2. Open C:\Users\Beckman Coulter\Documents\Keltoum\Echo\NGS pooling\Pooling_Post_Qubit.ecp
    3. In the "Pick List" section, import the Echo file from PART 2
    4. Press "Run"
    5. Follow the instruction on the Echo software and place on the tray the:
        - Source plate: Echo 384-well PP-0200 plate containing the input samples (the same plate as the one used in PART 1)
        - Destination plate: Greiner 384 PS 781096 plate

Output = Destination plate with final pool in the selected well and with the desired volume. 

## License

[London Biofoundry](https://www.londonbiofoundry.org/)










