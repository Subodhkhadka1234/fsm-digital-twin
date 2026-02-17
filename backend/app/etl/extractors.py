"""
ETL Extractors for various data sources
"""
import logging
import pandas as pd
import zipfile
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class CSVExtractor:
    """Extract data from CSV files"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        
    def extract(self) -> pd.DataFrame:
        """Extract data from CSV file"""
        try:
            logger.info(f"Extracting data from {self.file_path}")
            df = pd.read_csv(self.file_path)
            logger.info(f"Extracted {len(df)} rows from {self.file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Failed to extract from {self.file_path}: {str(e)}")
            raise


class ZipExtractor:
    """Extract CSV files from ZIP archive"""
    
    def __init__(self, zip_path: str, extract_to: str = "./data/extracted"):
        self.zip_path = Path(zip_path)
        self.extract_to = Path(extract_to)
        
    def extract(self) -> Dict[str, Path]:
        """Extract all CSV files from ZIP"""
        try:
            logger.info(f"Extracting ZIP file: {self.zip_path}")
            self.extract_to.mkdir(parents=True, exist_ok=True)
            
            extracted_files = {}
            
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    # Only extract CSV files, skip __MACOSX
                    if file_info.filename.endswith('.csv') and '__MACOSX' not in file_info.filename:
                        # Extract to destination
                        zip_ref.extract(file_info, self.extract_to)
                        
                        # Get the extracted file path
                        extracted_path = self.extract_to / file_info.filename
                        file_name = Path(file_info.filename).name
                        extracted_files[file_name] = extracted_path
                        
                        logger.info(f"Extracted: {file_name}")
            
            logger.info(f"Extracted {len(extracted_files)} CSV files")
            return extracted_files
            
        except Exception as e:
            logger.error(f"Failed to extract ZIP: {str(e)}")
            raise


class DataFrameExtractor:
    """Extract data from pandas DataFrame (for API/database sources)"""
    
    def __init__(self, data: Any):
        self.data = data
        
    def extract(self) -> pd.DataFrame:
        """Convert data to DataFrame"""
        try:
            if isinstance(self.data, pd.DataFrame):
                return self.data
            elif isinstance(self.data, list):
                return pd.DataFrame(self.data)
            elif isinstance(self.data, dict):
                return pd.DataFrame([self.data])
            else:
                raise ValueError(f"Unsupported data type: {type(self.data)}")
        except Exception as e:
            logger.error(f"Failed to extract data: {str(e)}")
            raise


def extract_datasets_zip(zip_path: str = "./datasets (2).zip") -> Dict[str, pd.DataFrame]:
    """
    Extract and load all datasets from the provided ZIP file
    
    Returns:
        Dict mapping dataset names to DataFrames
    """
    try:
        logger.info("Starting dataset extraction...")
        
        # Extract ZIP
        extractor = ZipExtractor(zip_path)
        extracted_files = extractor.extract()
        
        # Load each CSV into DataFrame
        datasets = {}
        for file_name, file_path in extracted_files.items():
            csv_extractor = CSVExtractor(file_path)
            df = csv_extractor.extract()
            
            # Use filename without extension as key
            dataset_name = file_name.replace('.csv', '')
            datasets[dataset_name] = df
            
            logger.info(f"Loaded {dataset_name}: {df.shape[0]} rows, {df.shape[1]} columns")
        
        logger.info(f"Successfully extracted {len(datasets)} datasets")
        return datasets
        
    except Exception as e:
        logger.error(f"Failed to extract datasets: {str(e)}")
        raise


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    datasets = extract_datasets_zip()
    
    print("\nExtracted datasets:")
    for name, df in datasets.items():
        print(f"- {name}: {df.shape}")
        print(f"  Columns: {list(df.columns)[:5]}...")
