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
    Basic Virtual Twin Object to handle data formatting and processing.
    """
    def __init__(self, data, outcome_field, treatment_field, interactions=True):
        """
        Initializes the VTObject.

        Args:
            data (pd.DataFrame): The dataset.
            outcome_field (str): The outcome variable name.
            treatment_field (str): The treatment variable name.
            interactions (bool): Whether to create interaction terms.
        """
        self.data = data.copy()
        self.outcome_field = outcome_field
        self.treatment_field = treatment_field
        self.interactions = interactions
        self._format_data()

    def _format_data(self):
        """Formats data and creates interaction terms if specified."""
        if self.interactions:
            treatment_col = self.data[self.treatment_field]
            for col in self.data.columns:
                if col not in [self.outcome_field, self.treatment_field]:
                    self.data[f"{self.treatment_field}_x_{col}"] = treatment_col * self.data[col]

    def get_X(self):
        """Returns feature matrix X."""
        features = [col for col in self.data.columns if col not in [self.outcome_field, self.treatment_field]]
        return self.data[features]

    def get_Y(self):
        """Returns target variable Y."""
        return self.data[self.outcome_field]

    def get_treatment(self):
        """Returns treatment variable."""
        return self.data[self.treatment_field]

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