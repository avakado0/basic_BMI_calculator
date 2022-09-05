import os
print(os.getcwd())
import pandas as pd
import json
from numpy import int64
import datetime
from modules.loggers import Logger
import os
class Engine:
    def __init__(self):
        self.bmi = BMIFunctions()
        self.validator = Validation()
        self.logger = Logger()
    def import_json(self, filename: str) -> pd.DataFrame:
        absolute_path_to_input_file = self.locate_config(filename)
        input_ = open(absolute_path_to_input_file, "r")
        return pd.DataFrame(json.load(input_))
    def locate_config(self, filename):
        path = os.getcwd()
        os.path.join(os.path.abspath(os.path.join(path, os.pardir)), filename)
        return os.path.join(path, filename)
    def get_configs(self) -> tuple:
        '''Gets configurations from the file (config.txt)
                
                - The first line, "name_of_input_file" is the name input JSON file
                - The second line, "create_new_outputs_in_every_run" determines
                whether, when the program is run again, a new output excel file 
                and an new observation file which contains the number of overveight
                people in the date set
                    - It can be edited to be a boolean value: True or False
                '''
        file = open("/home/draco/docs/business challenges/config.txt", "r")
        'create_new_outputs_in_every_run = '.split("=")[-1].strip().lower()
        configurations = file.readlines()
        input_filename = configurations[0].split("=")[-1].strip()
        append_string = configurations[1].split("=")[-1].strip().lower()
        append_value = self.load_boolean_string(append_string)
        return  input_filename, append_value
    def load_boolean_string(self, text: str) -> bool:
        if text == 'true':
            return True
        elif text == 'false' or '':
            return False
    def process_solution(self, solution_df: pd.DataFrame, append_value) -> None:
        if append_value:
            now = datetime.datetime.now().__str__().split(".")[0].replace(':','')
            output_filename = f"OUTPUT   --{now}.xls"
        else:
            output_filename = "OUTPUT.xls"
        solution_df.to_excel(
            output_filename,  #Output file name
            index = False
            )
        self.bmi.generate_analysis(output_filename.strip('.xls'), self.bmi.get_overweight_number(solution_df), append_value)
        print(f"""----- Answer for Question 1 written to file called OUTPUT excel
                 BMI Table:

                   {solution_df}
                  ----- Answer for Question 2:
                            Number of people whose BMI falls into "overweight" category => {self.bmi.get_overweight_number(solution_df)}
                                            This stat is also written right 
                                            next to the top right corner of the excel OUTPUT""")
        return None
    def main(self):
        
        try:
            input_file_name, append_outputs = self.get_configs()
            input_df = self.import_json(input_file_name)
        except:
            self.logger.stop_and_warn("Input JSON couldn't be imported.")
        
        if self.validator.check_data_validity(input_df):
            bmi_stats_table = self.bmi.add_three_columns(input_df)
            self.process_solution(bmi_stats_table, append_outputs)          
        else:
            self.logger.error("Input JSON couldn't be imported.")

        return None

class BMIFunctions:
    '''- Class with functions dealing with BMI calcuation processes.
        - generate_analysis method could later be specialized for
          for further insights using the input parameters

    Methods
    -------
    add_three_columns(dataframe: pd.DataFrame) -> pd.DataFrame
        Creates an output dataframe with additional columns with BMI stats
    calculate_bmi(self, weight: int, height: int) -> float
        Calculates BMI
    get_BMI_category_and_health_risks(bmi: float) -> tuple:
        Calculates the BMI category and corresponding health risk
        for input BMI value
    get_overweight_number(dataframe: pd.DataFrame) -> int:
        Extracts number of overweight people from input dataframe which
        is the processed output of the original input dataframe with 
        height, weight and gender values
    generate_analysis(target_file_name: str, overweight_number: int, append) -> None:
        Generates analytical figures from the output dataframe into OBSERVATONS 
        text file
        '''
    def __init__(self):
        self.logger = Logger()
        self.validate = Validation()
    def add_three_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        '''Creates the dataframe with three additional 
        columns with information regarging each 
        individual on raws to the input dataset. '''
        list_for_new_columns = []
        for raw_number in range(len(dataframe)):
            gender = dataframe.iloc[raw_number]['Gender']
            height = dataframe.iloc[raw_number]['HeightCm']
            weight = dataframe.iloc[raw_number]['WeightKg']
            bmi = self.calculate_bmi(weight, height)
            
            
            bmi_result_tuple = self.get_BMI_category_and_health_risks(bmi)
            bmi_category = bmi_result_tuple[0]
            health_risk = bmi_result_tuple[1]
            bmi_category, health_risk = self.get_BMI_category_and_health_risks(bmi)

            list_for_new_columns.append({
                'BMI' : bmi,
                'BMI Category': bmi_category,
                'Health Risk': health_risk
            })
        new_dataframe_with_answers = pd.DataFrame(list_for_new_columns)
        return pd.concat([dataframe, new_dataframe_with_answers], axis = 1)
    def calculate_bmi(self, weight: int, height: int) -> float:
        'Calculates BMI'
        #self.validate(weight, height)
        meters_height = height / 100
        bmi = weight / (meters_height ** 2)
        return round(bmi, 2) 
    def get_BMI_category_and_health_risks(self, bmi: float) -> tuple:
        try:
            if bmi >= 40:
                category = 'Very severely obese', 'Very high risk'
            elif bmi >= 35:
                category = 'Severely obese', 'High risk'
            elif bmi >= 30:
                category = 'Moderately obese', 'Medium risk'
            elif bmi >= 25:
                category = 'Overweight', 'Enhanced risk'
            elif bmi >= 18.5:
                category = 'Normal weight', 'Low risk'
            elif bmi == '0':
                self.logger.zeroBMI_warning()
            else:
                category = 'Underweight', 'Malnutrition risk'
        except:
            self.logger.invalidBMI_warning()
            
        return category
    def get_overweight_number(self, dataframe: pd.DataFrame) -> int:
        return len(dataframe[dataframe.iloc[ : , 4] == 'Overweight'])
    def generate_analysis(self, target_file_name: str, overweight_number: int, append) -> None:
        '''Creates a text file with observation figures from output data
           Current version extracts the number of overweight people'''
        if append:
            target_file_name = "OBSERVATIONS" + target_file_name.split("---")[-1]
        else:
            target_file_name = "OBSERVATIONS"
        file = open(target_file_name + '.txt', "w")
        file.write(f"Number of overweight people in input dataset = {overweight_number}")
        file.close()
        return None


class Validation:
    '''- Class with functions dealing with processes of input data validation.
       - It makes sure if all the input values are valid and logs if invalid
         input values are spotted.'''
    def __init__(self):
        self.logger = Logger()
    def validate_BMI_inputs(self, weight: str, height: str) -> bool:
        'Stops the program if invalid input values are spotted.'
        if weight == 0 or height == 0:
            if weight != 0:
                self.logger.zeroBMI_input_warning("height")
            else:
                self.logger.zeroBMI_input_warning("weight")
        else:
            return False
    def validate_raw(self, gender: str, height: int, weight: int) -> bool:
        ''' - Validates values of each raw.
            - Returns False if there is any 
            cell with invalid value'''
        if self.validate_gender(gender) and self.validate_integer(weight) and self.validate_integer(height):
            return True
        else:
            return False        
    def validate_string(self, text: str) -> bool:
        '''Checks if type of the input string is string.'''
        if isinstance(text, str):
            return True
        else:
            return False
    def validate_integer(self, text: int64) -> bool:
        '''Checks if type of the input string is integer.'''
        if isinstance(text, int64):
            return True
        else:
            return False
    def check_data_validity(self, dataframe: pd.DataFrame) -> bool :
        '''Used to check the validitY of 
         the values of all cells of input file'''
        pd.Series
        
        g = (dataframe['Gender'])
        h = (dataframe['HeightCm'])
        w = (dataframe['WeightKg'])
        print (g, h ,w)
        for i in range(len(dataframe)):
            print (g[i], h[i], w[i])
            if self.validate_raw(g[i], h[i], w[i]):
                pass
            else:
                error_text = 'Invalid value in raw number' + str(i)
                self.logger.error(error_text)        
                return False
        return True
        
        
        
        
        
        try:
            dataframe.apply(self.check_cell_validity)
        except:
            self.logger.error("Input couldn't be loaded. It has invalid cell values.")
    def validate_gender(self, gender_str: str) -> bool:
        'Checks if the value taken from input is a valid gender string'
        if self.validate_string(gender_str):
            genders = ['Agender', 'Androgyne', 'Bigender', 'Butch', 'Transgender Female', 'Transgender Male', 'Male', 'Female', 'Prefers Not To Say']
            
            if gender_str in genders:
                return True
            else:
                return False
        else:
            return False



    
if __name__ == '__main__':
    engine = Engine()
    engine.main()
    

#s = BMIFunctions()


