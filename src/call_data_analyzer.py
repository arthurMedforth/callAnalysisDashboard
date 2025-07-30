import pandas as pd
import streamlit as st


class CallDataAnalyzer:
    def __init__(self, file_input):
        """Initialize analyzer with data from Excel file"""
        try:
            self.master_df = pd.read_excel(file_input)
            self._validate_dataframe()
            self._clean_category_data() 
            self.get_category_stats() # Add new cleaning step
            self.computeMetrics()
            self.master_df['country'] = self.master_df['calling phone number'].apply(self.get_country_from_number)
        except Exception as e:
            raise ValueError(f"Error processing file: {str(e)}")

    def _validate_dataframe(self):
        """Validate dataframe structure and content"""
        required_columns = ['date', 'calling phone number', 'flagged', 'category']
        
        # Check columns exist
        missing_columns = [col for col in required_columns if col not in self.master_df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Validate data types
        if not pd.api.types.is_datetime64_any_dtype(self.master_df['date']):
            self.master_df['date'] = pd.to_datetime(self.master_df['date'])

        # Validate flagged values
        valid_flags = ['neutral', 'spam', 'fraud']
        invalid_flags = self.master_df[~self.master_df['flagged'].isin(valid_flags)]['flagged'].unique()
        if len(invalid_flags) > 0:
            raise ValueError(f"Invalid flag values found: {invalid_flags}")

    def _clean_category_data(self):
        """Clean and standardize category data"""
        # Replace NaN, empty strings, and whitespace-only strings with 'Other'
        self.master_df['category'] = self.master_df['category'].fillna('Other')
        self.master_df['category'] = self.master_df['category'].replace(r'^\s*$', 'Other', regex=True)
        self.master_df['category'] = self.master_df['category'].str.strip()
        
        # Set category to 'undefined' for:
        # 1. Spam calls with no category (Other)
        # 2. Spam calls with generic 'spam' category
        spam_undefined_mask = (
            (self.master_df['flagged'] == 'spam') & 
            ((self.master_df['category'] == 'Other') | 
             (self.master_df['category'] == 'Spam'))
        )
        self.master_df.loc[spam_undefined_mask, 'category'] = 'undefined'

    def computeMetrics(self):
        """Compute all metrics based on current master_df"""
        # Calculate key metrics from scratch
        self.total_calls = len(self.master_df)
        self.spam_calls = len(self.master_df[self.master_df['flagged'] == 'spam'])
        self.fraud_calls = len(self.master_df[self.master_df['flagged'] == 'fraud'])
        self.neutral_calls = len(self.master_df[self.master_df['flagged'] == 'neutral'])
        self.total_blocked = self.spam_calls + self.fraud_calls
        self.protection_rate = (self.total_blocked / self.total_calls) * 100

    @staticmethod
    def get_country_from_number(phone_number):
        """
        Extract country from phone number prefix
        Returns country name with flag emoji
        """
        string_num = str(phone_number).strip()
        
        # Define country codes and their representations
        country_codes = {
            '33': 'France 🇫🇷',
            '49': 'Germany 🇩🇪',
            '39': 'Italy 🇮🇹',
            '34': 'Spain 🇪🇸',
            '351': 'Portugal 🇵🇹',
            '31': 'Netherlands 🇳🇱',
            '1': 'North America 🇺🇸🇨🇦',
            '44': 'UK 🇬🇧',
            '353': 'Ireland 🇮🇪'
        }
        
        # Check for longer codes first (e.g., 351 before 31)
        for prefix in sorted(country_codes.keys(), key=len, reverse=True):
            if string_num.startswith(prefix):
                return country_codes[prefix]
        
        return 'Other 🌍'

    def get_daily_stats(self):
        daily_stats = self.master_df.groupby('date').agg({
            'calling phone number': 'count',
            'flagged': lambda x: (x.isin(['spam', 'fraud'])).sum()
        }).reset_index()
        daily_stats.columns = ['date', 'total_calls', 'blocked_calls']
        daily_stats['protection_rate'] = (daily_stats['blocked_calls'] / daily_stats['total_calls']) * 100
        daily_stats['date_str'] = daily_stats['date'].dt.strftime('%b %d')
        return daily_stats

    def get_category_stats(self):
        """Get statistics for spam calls by category, with combined undefined category"""
        # Filter for spam calls only
        spam_df = self.master_df[self.master_df['flagged'] == 'spam']
        
        # Get category counts
        category_counts = spam_df['category'].value_counts()
        
        return category_counts
