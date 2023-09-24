# Structured Visual Noise 

### What was Created?
A program that takes some basic parameters ( length of M-sequence, image size in pixels, and length of time to show each frame, total duration of frame display ) and creates the corresponding visual noise frames. Once the program runs its course, a file is outputed with the parameters given, along with a timestamp for each frame presented and the initial state of each row so that the frame can be reproduced in the future.

![Param Input Window](https://github.com/msoni122/visualNoise/assets/36343747/cfcdbef1-1694-4db8-8a19-21b02d1144d0)
![Visual Noise Display Window](https://github.com/msoni122/visualNoise/assets/36343747/1c259302-dc47-4885-980c-9d6f02df7fe8)

### Tell Me a little more about M-Sequences
"Maximum Length Sequence," is a type of pseudorandom binary sequence. M-sequences are generated using Linear Feedback Shift Registers (LFSRs). 

The length of an M-sequence is equal to 2^n - 1, where "n" is the number of stages (bits) in the LFSR. This means that the sequence repeats after 2^n - 1 bits, and it contains all possible binary states except an all-zero state.

Basic algothm to generate m-sequence:
1. Start with the initial state.
2. Enter a loop that generates bits for the M-sequence.
3. For each iteration of the loop:
- Calculate the next bit in the sequence by performing an XOR operation on the values of the cells corresponding to the tap positions defined by the feedback polynomial.
- Shift the state to the right (or left) to make room for the new bit and insert the new bit at the leftmost cell.
- Append the new bit to the M-sequence.
4. Repeat the loop until you have generated the desired number of bits for the M-sequence.

## Assumptions Made
- An m-sequence creates a one-dimensional array of bits, but the image sent to me was two-dimensional. I assumed that I should create multiple rows of m-sequences to create a image that looks similar to what was sent
- I wasn't really sure what valid inputs would be, so I made judgement call regarding validation logic
- It would be a better UI to have a default loop run if inputed parameters didn't meet basic validation rules
- We wouldn't want infinate noise running, so I capped the loop at 2 minutes
- Rather than having active logging to a file, it would be okay to log all the frames to the file once the program was terminated
- File names are fine as visualNoise_[date].json 
- Timestamp is okay in local time rather needing to be in any specific typezone, such as UTC
- We want the information in the file to be easily readable, ie.. json format, so that we can later create a feature to use the data easily
- We don't want any extra noise around our noise [ noise being x, y axis, titles, timers, etc ]
- I took the prompt as is... I did not have any information about future uses or features and didn't want to overengineer in terms of scalability or deployment needs

### Extra Libraries Used
- [PyQt5](https://www.pythonguis.com/tutorials/pyqt-basic-widgets/) and matplotlib to display the visual noise
- [Scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.max_len_seq.html) -- used the max_len_seq function to create the m-sequence arrays
- Numpy -- numpy arrays created by scipy libraries and used in displaying noise

## How to Run Application?!
I'm assuming that along with a fresh install of Ubuntu, you have github already set up locally
```
### clone code and move directories ###
git clone https://github.com/msoni122/visualNoise.git
cd visualNoise

### Set up a virtual enviroment as to not mess us the python and dependencies on your local ###
python -m venv venv 
    ### Depending on how you have python setup, if the executable is pointing to python 2 or python 3, you may need to do python3 -m venv venv... you can check your python version with the command `python --version`
    ### The command above worked fine on mac, but on windows wsl, ubuntu subsystem, I also needed to `sudo apt install python3.10-venv` first
source venv/bin/activate

### Download dependencies and package ###
pip install -r requirements.txt
pip install -e .

### The setup should have created an executable, just run this command and the program should start ###
visualNoise
```

## Code Overview
```
visualNoise
|   .gitignore
|   README.md
|   requirements.txt
|   setup.py
└─── app
|    |    __init.py__
|    |    app.py
|    |    parameterValidation.py
|    |    noiseWindow.py
|    |    fileOutputLog.py
|
└───  tests
|    |    __init__.py
|    |    test_parameterValidations.py
|    |    test_fileOutputLog.py
└───  files
|    |    visualNoise_{date}.json
└─── venv
```

## Todo List
---
### Known Bugs
- [ ] When the window first opens, it waits the interval to display anything other than the axises
- [ ] In doing some extra testing, I tried running this on wsl ubuntu distro on Windows laptop -- I was had trouble getting the wsl to link to the proper pluggins needed for PyQT5 to work properly with the NVIDIA Graphics card

### Set Up Github and CI/CD
- [ ] Create develop and main branches
- [ ] Require review to merge
- [ ] Unittest to run before merge available
- [ ] Linter run before merge available
- [ ] SetUp proper CI/CD -- automate deploy on merge to main branch

### Maintainabilty Going Forward
- [ ] Use tox or similar package for better dependency managent
- [ ] More testing coverage
- [ ] Create Docker Image or similar so that onboarding users don't need to deal with dependencies or getting project up and running on their own

### Some Likely Features
- [ ] Ability to upload a file and create corresponding visual noise loop
