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
    data = dataset.copy()  # It's good practice to work on a copy to avoid modifying the original

    # Create interaction terms if interactions=True
    if interactions:
        treatment_column = data[treatment_field]
        for col_name in data.columns:
            if col_name not in [outcome_field, treatment_field]:
                data[f'{treatment_field}_x_{col_name}'] = treatment_column * data[col_name]

    return data


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
        features = [
            col for col in self.data.columns
            if col not in [self.outcome_field, self.treatment_field]
            and not col.startswith(f"{self.treatment_field}_x_{self.treatment_field}")
        ]
        return self.data[features]


    def get_Y(self):
        """Returns target variable Y."""
        return self.data[self.outcome_field]

    def get_treatment(self):
        """Returns treatment variable."""
        return self.data[self.treatment_field]


def vt_data_python(dataset, outcome_field, treatment_field, interactions=True, **kwargs):
    """
    Python equivalent of the R vt.data function.
    Formats the dataset and creates a VTObject.

    Args:
        dataset (pd.DataFrame): The input dataset.
        outcome_field (str): Name of the outcome variable column.
        treatment_field (str): Name of the treatment variable column.
        interactions (bool, optional): Whether to create interaction terms. Defaults to True.
        **kwargs:  Additional keyword arguments to be passed to VTObject.

    Returns:
        VTObject: A VTObject containing the formatted data.
    """
    # Format the dataset
    formatted_data = format_rct_dataset_python(dataset, outcome_field, treatment_field, interactions=interactions)
    
    # Initialize the VTObject and pass outcome_field and treatment_field
    vt_object = VTObject(
        data=formatted_data,
        outcome_field=outcome_field,  # Pass the outcome_field here
        treatment_field=treatment_field,  # Pass the treatment_field here
        interactions=interactions,
        **kwargs
    )
    
    return vt_object



class VTForest:
    def __init__(self, forest_type, vt_data, model_trt1, model_trt0):
        """
        Initializes the VTForest for treatment effect estimation.

        Args:
            forest_type (str): Type of the forest (usually 'double').
            vt_data (VTObject): The VTObject containing the dataset.
            model_trt1 (RandomForestClassifier): The random forest model for the treatment group.
            model_trt0 (RandomForestClassifier): The random forest model for the control group.
        """
        self.forest_type = forest_type
        self.vt_data = vt_data
        self.model_trt1 = model_trt1
        self.model_trt0 = model_trt0
        self.P1_hat = None
        self.P0_hat = None
        self.ITE = None
        self._apply_virtual_twin_forest()

    def _apply_virtual_twin_forest(self):
        """Apply the double random forest method using the provided models."""
        X = self.vt_data.get_X()
        self.P1_hat = self.model_trt1.predict_proba(X)[:, 1]
        self.P0_hat = self.model_trt0.predict_proba(X)[:, 1]
        self.ITE = self.P1_hat - self.P0_hat
