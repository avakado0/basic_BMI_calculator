- This small application processes weight, height, gender information into BMI figures for each individual in input file.
- It generates an output excel file and an observation excel file with number of overweight people in input file.

- config.txt file must be configured before running the application. 
 - It has the name of the input file -there is a sample json file called "input.json" in the project folder).
  - The " = " after name_of_input_file should be added a name for input json file. Default is "input.json"
   - Before running the program, make sure the name of the json file indicated in config.txt is same as the name of your input json file.
  - The " = " after create_new_outputs_in_every_run should be added:
   - Either true or a false value. If no value is added after '=' sign. It will be assumed false
  - Correct usage exampes
  
  -------
      - Example 1
      
      		name_of_input_file = input.json
      		create_new_outputs_in_every_run = true

      - Example 2


      		name_of_input_file = info.json
      		create_new_outputs_in_every_run = false

      - Example 3


      		name_of_input_file = info.json
      		create_new_outputs_in_every_run = 

      - Example 2


      		name_of_input_file = info.json
      		create_new_outputs_in_every_run = True
----


----------------Usage:       Open a terminal in /project directory and run the py file called "run.py"
-------------------------	In some operation systems its "python run.py" command, in some it's "python3 run.py" command.
Project Layout

project/
│
├── modules/
│   ├── solution.py
│   ├── loggers.py
│   └── exceptions.py
├── run.py
├── config.txt
├── input.json
├── README.md

└── setup.py
