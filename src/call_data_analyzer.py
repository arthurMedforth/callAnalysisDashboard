import pandas as pd


def load_excel_data(csv_path):
    """Load Excel file data"""
    return pd.read_excel(csv_path)


class CallDataAnalyzer:
    def __init__(self, csv_path):
        self.protection_rate = None
        self.total_blocked = None
        self.neutral_calls = None
        self.fraud_calls = None
        self.spam_calls = None
        self.total_calls = None
        self.master_df = load_excel_data(csv_path)  # No cache needed here
        self.computeMetrics()
        self.master_df['country'] = self.master_df['calling phone number'].apply(self.get_country_from_number)

    def computeMetrics(self):
        # Calculate key metrics
        self.total_calls = len(self.master_df)
        self.spam_calls = len(self.master_df[self.master_df['flagged'] == 'spam'])
        self.fraud_calls = len(self.master_df[self.master_df['flagged'] == 'fraud'])
        self.neutral_calls = len(self.master_df[self.master_df['flagged'] == 'neutral'])
        self.total_blocked = self.spam_calls + self.fraud_calls
        self.protection_rate = (self.total_blocked / self.total_calls) * 100

    @staticmethod
    def get_country_from_number(phone_number):
        """Extract country from phone number prefix"""
        string_num = str(phone_number)
        if string_num.startswith('44'):
            return 'UK'
        elif string_num.startswith('353'):
            return 'Ireland'
        elif string_num.startswith('49'):
            return 'Germany'
        elif string_num.startswith('1'):
            return 'North America'
        else:
            return 'Other'

    def get_daily_stats(self):
        """Cache daily statistics computation"""
        daily_stats = self.master_df.groupby('date').agg({
            'calling phone number': 'count',
            'flagged': lambda x: (x.isin(['spam', 'fraud'])).sum()
        }).reset_index()
        daily_stats.columns = ['date', 'total_calls', 'blocked_calls']
        daily_stats['protection_rate'] = (daily_stats['blocked_calls'] / daily_stats['total_calls']) * 100
        daily_stats['date_str'] = daily_stats['date'].dt.strftime('%b %d')
        return daily_stats
