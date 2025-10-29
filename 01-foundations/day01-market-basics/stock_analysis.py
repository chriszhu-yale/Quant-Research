"""
Day 1: Stock Data Analysis
Author: Your Name
Date: 2024-10-29

This script demonstrates basic stock data analysis:
- Download historical data
- Calculate returns and volatility
- Create visualizations
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class StockAnalyzer:
    """A class to analyze stock data"""
    
    def __init__(self, ticker, start_date=None, end_date=None):
        """
        Initialize the analyzer
        
        Parameters:
        -----------
        ticker : str
            Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        start_date : str
            Start date in 'YYYY-MM-DD' format
        end_date : str
            End date in 'YYYY-MM-DD' format
        """
        self.ticker = ticker
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.data = None
        
    def download_data(self):
        """Download stock data from Yahoo Finance"""
        print(f"📥 Downloading data for {self.ticker}...")
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False)
        print(f"✅ Downloaded {len(self.data)} trading days of data")
        return self.data
    
    def calculate_returns(self):
        """Calculate simple and log returns"""
        if self.data is None:
            self.download_data()
        
        # Simple returns
        self.data['Simple_Return'] = self.data['Adj Close'].pct_change()
        
        # Log returns (preferred in quant finance)
        self.data['Log_Return'] = np.log(self.data['Adj Close'] / self.data['Adj Close'].shift(1))
        
        print(f"\n📊 Returns Summary:")
        print(f"   Mean Daily Return: {self.data['Log_Return'].mean():.4%}")
        print(f"   Daily Volatility: {self.data['Log_Return'].std():.4%}")
        print(f"   Annualized Return: {self.data['Log_Return'].mean() * 252:.2%}")
        print(f"   Annualized Volatility: {self.data['Log_Return'].std() * np.sqrt(252):.2%}")
        
        return self.data
    
    def calculate_rolling_metrics(self, window=30):
        """Calculate rolling statistics"""
        if 'Log_Return' not in self.data.columns:
            self.calculate_returns()
        
        # Rolling volatility (30-day)
        self.data['Rolling_Vol'] = self.data['Log_Return'].rolling(window=window).std() * np.sqrt(252)
        
        # Rolling mean return
        self.data['Rolling_Mean'] = self.data['Log_Return'].rolling(window=window).mean() * 252
        
        return self.data
    
    def plot_analysis(self, save_path='outputs/'):
        """Create comprehensive visualization"""
        if 'Rolling_Vol' not in self.data.columns:
            self.calculate_rolling_metrics()
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle(f'{self.ticker} Stock Analysis', fontsize=16, fontweight='bold')
        
        # 1. Price and Volume
        ax1 = axes[0, 0]
        ax1_twin = ax1.twinx()
        
        ax1.plot(self.data.index, self.data['Adj Close'], color='#2E86AB', linewidth=2, label='Price')
        ax1_twin.bar(self.data.index, self.data['Volume'], alpha=0.3, color='gray', label='Volume')
        
        ax1.set_title('Price & Volume', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price ($)', color='#2E86AB')
        ax1_twin.set_ylabel('Volume', color='gray')
        ax1.tick_params(axis='y', labelcolor='#2E86AB')
        ax1_twin.tick_params(axis='y', labelcolor='gray')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        
        # 2. Returns Distribution
        ax2 = axes[0, 1]
        returns_clean = self.data['Log_Return'].dropna()
        ax2.hist(returns_clean, bins=50, alpha=0.7, color='#A23B72', edgecolor='black')
        ax2.axvline(returns_clean.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {returns_clean.mean():.4f}')
        ax2.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
        
        ax2.set_title('Daily Log Returns Distribution', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Log Return')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Rolling Volatility
        ax3 = axes[1, 0]
        ax3.plot(self.data.index, self.data['Rolling_Vol'], color='#F18F01', linewidth=2)
        ax3.fill_between(self.data.index, self.data['Rolling_Vol'], alpha=0.3, color='#F18F01')
        
        ax3.set_title('30-Day Rolling Volatility (Annualized)', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Volatility')
        ax3.grid(True, alpha=0.3)
        
        # 4. Cumulative Returns
        ax4 = axes[1, 1]
        cumulative_returns = (1 + self.data['Simple_Return']).cumprod()
        ax4.plot(self.data.index, cumulative_returns, color='#06A77D', linewidth=2)
        ax4.fill_between(self.data.index, 1, cumulative_returns, where=(cumulative_returns >= 1), 
                         alpha=0.3, color='green', label='Profit')
        ax4.fill_between(self.data.index, 1, cumulative_returns, where=(cumulative_returns < 1), 
                         alpha=0.3, color='red', label='Loss')
        ax4.axhline(y=1, color='black', linestyle='--', linewidth=1)
        
        ax4.set_title('Cumulative Returns', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Cumulative Return (1 = no change)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save figure
        import os
        os.makedirs(save_path, exist_ok=True)
        filename = f"{save_path}{self.ticker}_analysis_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n💾 Chart saved to: {filename}")
        
        plt.show()
    
    def generate_report(self):
        """Generate a summary report"""
        if self.data is None:
            self.download_data()
        if 'Log_Return' not in self.data.columns:
            self.calculate_returns()
        
        returns = self.data['Log_Return'].dropna()
        
        report = f"""
{'='*60}
        STOCK ANALYSIS REPORT: {self.ticker}
{'='*60}

📅 Period: {self.start_date} to {self.end_date}
📊 Trading Days: {len(self.data)}

💰 PRICE STATISTICS
   Starting Price: ${self.data['Adj Close'].iloc[0]:.2f}
   Ending Price: ${self.data['Adj Close'].iloc[-1]:.2f}
   Highest Price: ${self.data['Adj Close'].max():.2f}
   Lowest Price: ${self.data['Adj Close'].min():.2f}
   Total Return: {((self.data['Adj Close'].iloc[-1] / self.data['Adj Close'].iloc[0]) - 1) * 100:.2f}%

📈 RETURN METRICS
   Daily Mean Return: {returns.mean():.4%}
   Daily Std Dev: {returns.std():.4%}
   Annualized Return: {returns.mean() * 252:.2%}
   Annualized Volatility: {returns.std() * np.sqrt(252):.2%}
   Sharpe Ratio (Rf=0): {(returns.mean() / returns.std()) * np.sqrt(252):.2f}

📊 RISK METRICS
   Max Daily Gain: {returns.max():.2%}
   Max Daily Loss: {returns.min():.2%}
   95% VaR (daily): {np.percentile(returns, 5):.2%}
   Skewness: {returns.skew():.2f}
   Kurtosis: {returns.kurtosis():.2f}

{'='*60}
"""
        print(report)
        return report


def compare_stocks(tickers, start_date=None, end_date=None):
    """Compare multiple stocks"""
    print(f"\n🔍 Comparing {len(tickers)} stocks: {', '.join(tickers)}\n")
    
    # Download all data
    data = {}
    for ticker in tickers:
        analyzer = StockAnalyzer(ticker, start_date, end_date)
        analyzer.download_data()
        analyzer.calculate_returns()
        data[ticker] = analyzer.data
    
    # Create comparison plot
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Normalized prices
    ax1 = axes[0]
    for ticker in tickers:
        normalized = data[ticker]['Adj Close'] / data[ticker]['Adj Close'].iloc[0] * 100
        ax1.plot(data[ticker].index, normalized, label=ticker, linewidth=2)
    
    ax1.set_title('Normalized Price Comparison (Base = 100)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Normalized Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Volatility comparison
    ax2 = axes[1]
    for ticker in tickers:
        rolling_vol = data[ticker]['Log_Return'].rolling(30).std() * np.sqrt(252)
        ax2.plot(data[ticker].index, rolling_vol, label=ticker, linewidth=2)
    
    ax2.set_title('Rolling 30-Day Volatility Comparison', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Annualized Volatility')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('outputs/comparison.png', dpi=300, bbox_inches='tight')
    print("\n💾 Comparison chart saved to: outputs/comparison.png")
    plt.show()
    
    # Summary table
    summary = pd.DataFrame({
        ticker: {
            'Annual Return': data[ticker]['Log_Return'].mean() * 252,
            'Annual Volatility': data[ticker]['Log_Return'].std() * np.sqrt(252),
            'Sharpe Ratio': (data[ticker]['Log_Return'].mean() / data[ticker]['Log_Return'].std()) * np.sqrt(252),
            'Max Drawdown': ((data[ticker]['Adj Close'] / data[ticker]['Adj Close'].cummax()) - 1).min()
        }
        for ticker in tickers
    }).T
    
    print("\n📊 Summary Comparison:")
    print(summary.to_string())
    
    return summary


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(" " * 20 + "DAY 1: STOCK ANALYSIS")
    print("=" * 70)
    
    # Example 1: Single stock analysis
    print("\n" + "="*70)
    print("EXAMPLE 1: Analyzing Apple (AAPL)")
    print("="*70)
    
    # Create analyzer
    aapl = StockAnalyzer('AAPL', start_date='2023-01-01')
    
    # Download and analyze
    aapl.download_data()
    aapl.calculate_returns()
    aapl.calculate_rolling_metrics()
    
    # Generate report
    aapl.generate_report()
    
    # Create visualizations
    aapl.plot_analysis()
    
    # Example 2: Compare multiple stocks
    print("\n" + "="*70)
    print("EXAMPLE 2: Comparing Tech Stocks")
    print("="*70)
    
    tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
    comparison = compare_stocks(tech_stocks, start_date='2023-01-01')
    
    print("\n✅ Day 1 Complete! Check the 'outputs/' folder for charts.")
    print("\n📝 Next Steps:")
    print("   1. Try analyzing different stocks")
    print("   2. Experiment with different time periods")
    print("   3. Read the reflection questions in README.md")
    print("   4. Update your learning log!")

