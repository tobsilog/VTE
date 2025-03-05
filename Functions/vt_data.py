import pandas as pd

def format_rct_dataset_python(dataset, outcome_field, treatment_field, interactions=True):
    """
    Formats a dataset for RCT analysis, potentially creating interaction terms.

    Args:
        dataset (pd.DataFrame): The input dataset.
        outcome_field (str): Name of the outcome variable column.
        treatment_field (str): Name of the treatment variable column.
        interactions (bool, optional): Whether to create interaction terms. Defaults to True.

    Returns:
        pd.DataFrame: The formatted dataset.
    """
    data = dataset.copy() # It's good practice to work on a copy to avoid modifying the original

    # 1. Identify outcome and treatment columns (already given as strings)

    # 2. Create interaction terms if interactions=True
    if interactions:
        treatment_column = data[treatment_field]
        for col_name in data.columns:
            if col_name not in [outcome_field, treatment_field]: # Interact treatment with all other columns
                data[f'{treatment_field}_x_{col_name}'] = treatment_column * data[col_name] # Simple interaction (can be adjusted)

    
class VTObject:
    """
    Basic Virtual Twin Object.
    """
    def __init__(self, data, **kwargs):
        """
        Initializes the VTObject.

        Args:
            data (pd.DataFrame): The formatted dataset.
            **kwargs:  Keyword arguments to be stored (for future extension to mimic ... in R).
        """
        self.data = data
        self.params = kwargs # Store any extra parameters passed via ... for potential future use

    def get_data(self):
        """
        Returns the formatted data.
        """
        return self.data

    # You would add methods here for analysis, prediction, etc., 
    # based on what VT.object is supposed to do.
    # For example, prediction, causal inference methods, etc.

def vt_data_python(dataset, outcome_field, treatment_field, interactions=True, **kwargs):
    # """
    # Python equivalent of the R vt.data function.
    # Formats the dataset and creates a VTObject.

    # Args:
    #     dataset (pd.DataFrame): The input dataset.
    #     outcome_field (str): Name of the outcome variable column.
    #     treatment_field (str): Name of the treatment variable column.
    #     interactions (bool, optional): Whether to create interaction terms. Defaults to True.
    #     **kwargs:  Additional keyword arguments to be passed to VTObject.

    # Returns:
    #     VTObject: A VTObject containing the formatted data.
    # """
    
        formatted_data = format_rct_dataset_python(dataset, outcome_field, treatment_field, interactions=interactions)
        vt_object = VTObject(data=formatted_data, **kwargs)
        return vt_object