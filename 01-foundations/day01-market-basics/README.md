# Day 1: Financial Markets Basics

## 🎯 Learning Objectives
- Understand fundamental concepts: stocks, returns, volatility
- Learn to download and analyze stock data
- Calculate key financial metrics
- Create basic visualizations

## ⏱️ Time Allocation (1 hour)

### Part 1: Concepts (30 min)
- [ ] Watch: Khan Academy - Stocks intro (10 min)
- [ ] Read: What is market capitalization? (5 min)
- [ ] Understand: Simple vs Log returns (5 min)
- [ ] Learn: Historical volatility concept (10 min)

### Part 2: Hands-on Coding (30 min)
- [ ] Setup: Install yfinance and test download (5 min)
- [ ] Code: Download stock data for AAPL (5 min)
- [ ] Calculate: Returns and volatility (10 min)
- [ ] Visualize: Price, returns, volatility charts (10 min)

## 📝 Deliverables
- [ ] `stock_analysis.py` - Complete script
- [ ] `analysis.ipynb` - Jupyter notebook with explorations
- [ ] `stock_analysis.png` - Visualization output

## 🔑 Key Concepts

**Stock Price**: Market value per share  
**Return**: Percentage change in price  
- Simple return: (P_t - P_{t-1}) / P_{t-1}
- Log return: ln(P_t / P_{t-1})

**Volatility**: Measure of price fluctuation (risk)  
- Calculated as standard deviation of returns
- Annualized: daily_vol × √252

**Sharpe Ratio**: Risk-adjusted return metric  
- Formula: (Return - Risk_free_rate) / Volatility

## 📊 Expected Output

You should be able to:
1. Download any stock's historical data
2. Calculate daily/monthly returns
3. Compute rolling volatility
4. Generate professional-looking charts

## 🤔 Reflection Questions
1. Why do we use log returns instead of simple returns?
2. What does high volatility indicate?
3. How would you compare two stocks' performance?

## 🔗 Next
Tomorrow: Build your first trading strategy!
