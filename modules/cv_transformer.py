import pandas as pd
import numpy as np
import os
from datetime import datetime
import calendar
from typing import List, Optional


class CVTransformer:
    """
    A module to transform raw CV data from CSV files to a standardized format.
    
    This transformer handles the conversion of marketing growth reports from their
    original wide format (with days as columns) to a long format with proper
    date handling and column standardization.
    """
    
    def __init__(self, data_folder: str = "gh_data"):
        """
        Initialize the transformer.
        
        Args:
            data_folder: Path to the folder containing CSV files
        """
        self.data_folder = data_folder
        
    def get_csv_files(self) -> List[str]:
        """
        Get all CSV files in the data folder.
        
        Returns:
            List of CSV file paths
        """
        csv_files = []
        if os.path.exists(self.data_folder):
            for file in os.listdir(self.data_folder):
                if file.endswith('.csv'):
                    csv_files.append(os.path.join(self.data_folder, file))
        return csv_files
    
    def extract_month_year_from_filename(self, filename: str) -> tuple:
        """
        Extract month and year from filename.
        
        Args:
            filename: CSV filename
            
        Returns:
            Tuple of (month, year)
        """
        # Extract month and year from filename like "Ghana - Marketing_Growth 360 Report - 2025 - June 2025 Overview.csv"
        parts = filename.split(' - ')
        if len(parts) >= 4:
            year_part = parts[3].split(' ')[0]  # Get year
            month_part = parts[3].split(' ')[1]  # Get month
            
            # Convert month name to number
            month_map = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            
            month = month_map.get(month_part, 1)
            year = int(year_part)
            return month, year
        
        return 1, 2025  # Default values
    
    def get_days_in_month(self, month: int, year: int) -> int:
        """
        Get the number of days in a given month.
        
        Args:
            month: Month number (1-12)
            year: Year
            
        Returns:
            Number of days in the month
        """
        return calendar.monthrange(year, month)[1]
    
    def transform_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Transform a single CSV file.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Transformed DataFrame
        """
        # Load the CSV
        df = pd.read_csv(csv_path)
        
        # Extract month and year from filename
        filename = os.path.basename(csv_path)
        month, year = self.extract_month_year_from_filename(filename)
        
        # Transpose the dataframe
        df = df.sort_index().transpose()
        
        # Set column names from first row
        df.columns = df.iloc[0]
        
        # Remove the first row (which became column names)
        df = df[1:]
        
        # Rename specific columns
        df = df.rename(columns={
            'Cost Growth': 'Cost Digital', 
            'Cost Marketing ': 'Cost offline '
        })
        
        # Clean column names
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace(r'[+\-./]', '', regex=True)
        
        # Add report_day column and convert dates
        df.columns = ['report_day'] + df.columns.tolist()[1:]
        
        # Convert date format (e.g., "June 1" to "2025-06-01")
        df['report_day'] = pd.to_datetime(df['report_day'], format='%B %d')
        df['report_day'] = df['report_day'].dt.strftime(f'{year}-%m-%d')
        
        # Add additional columns that might be needed
        df['new_install_first_dis'] = np.nan
        df['signupfirst_dis'] = np.nan
        df['cac_incl_branding'] = np.nan
        df['first_disbursement_all'] = np.nan
        df['fsfirst_disb'] = np.nan
        df['first_disbursement_fidobiz'] = np.nan
        
        return df
    
    def transform_all_files(self) -> pd.DataFrame:
        """
        Transform all CSV files in the data folder.
        
        Returns:
            Combined DataFrame with all transformed data
        """
        csv_files = self.get_csv_files()
        
        if not csv_files:
            raise FileNotFoundError(f"No CSV files found in {self.data_folder}")
        
        transformed_dfs = []
        
        for csv_file in csv_files:
            try:
                print(f"Processing: {csv_file}")
                transformed_df = self.transform_csv(csv_file)
                transformed_dfs.append(transformed_df)
            except Exception as e:
                print(f"Error processing {csv_file}: {str(e)}")
                continue
        
        if not transformed_dfs:
            raise ValueError("No files were successfully transformed")
        
        # Combine all transformed dataframes
        combined_df = pd.concat(transformed_dfs, ignore_index=True)
        
        return combined_df
    
    def save_transformed_data(self, output_path: str = "transformed_cv_data.csv"):
        """
        Transform all files and save to CSV.
        
        Args:
            output_path: Path to save the transformed data
        """
        df = self.transform_all_files()
        df.to_csv(output_path, index=False)
        print(f"Transformed data saved to: {output_path}")
        return df


def main():
    """
    Main function to run the transformer.
    """
    transformer = CVTransformer()
    
    try:
        # Transform all files and save
        df = transformer.save_transformed_data()
        
        print(f"Successfully transformed data with {len(df)} rows and {len(df.columns)} columns")
        print("\nFirst few rows:")
        print(df.head())
        
        print("\nColumn names:")
        print(df.columns.tolist())
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 