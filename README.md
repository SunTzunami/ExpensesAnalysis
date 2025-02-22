# Personal Expenses Analysis Dashboard
Been tracking my expenses meticulously as a working adult so I thought of digging into the data to understand and improve my spending habits. Hope it helps others too!

## Features

### Current Features
- **Flexible Data Upload**
  - Support for `.xls` and `.xlsx` file formats
  - Automatic data validation and formatting

- **Advanced Time-Based Analysis**
  - Year-wise analysis
  - Monthly analysis
  - Daily analysis
  - Custom date range analysis
  
- **Interactive Visualizations**
  - Category distribution charts
  - Sunburst charts for hierarchical category view
  - Cumulative expense tracking
  - Daily expense timeseries
  - Interactive tooltips and legends

- **Dynamic Metrics**
  - Total expenses calculation
  - Daily average expenses
  - Monthly average expenses
  - Period-specific analytics

### Upcoming Features
- **Expense Prediction Capabilities**
  - Machine learning-based expense forecasting
  - Category-wise spending predictions
  - Anomaly detection for unusual spending patterns
  - Customizable prediction timeframes
  - Budget planning recommendations

## Data Format Requirements

### Required Columns
| Column Name | Description | Format/Type |
|-------------|-------------|-------------|
| Date | Transaction date | YYYY-MM-DD |
| Expense | Amount spent | Numeric |
| Category | Expense category | String |
| Remarks | Transaction description | String |
| Onetime | One-time expense flag | Boolean (0.0/1.0) |
| For Others | Expenses made for others | Boolean (0.0/1.0) |
| NewCategory | Mapped broader category | String |

### Category Mapping
I had too many categories so I combined the ones I thought were similar:

```python
category_mapping = {
    # Food and Dining
    'grocery': 'Food',
    'snacks': 'Food',
    'dining': 'Food',
    
    # Health and Personal Care
    'medicines': 'Personal Care and Medicines',
    'personal care': 'Personal Care and Medicines',
    
    # Entertainment
    'entertainment': 'Entertainment and Books',
    'books': 'Entertainment and Books',
    
    # Housing
    'housing': 'Housing and Utilities',
    'utility': 'Housing and Utilities',
    
    # Household Items
    'clothing': 'Household and Clothing',
    'household': 'Household and Clothing',
    
    # Home Improvement
    'furniture': 'Electronics and Furniture',
    'electronics': 'Electronics and Furniture',
    
    # Fitness and Sports
    'supplements': 'Fitness',
    'shoes': 'Fitness',
    'sports event': 'Fitness',
    'sports watch': 'Fitness',
    'sports clothing': 'Fitness',
    'sports rental': 'Fitness',
    'gym': 'Fitness',
    'sports equipment': 'Fitness',
    
    # Transportation
    'commute': 'Transportation',
    'ride share': 'Transportation',
    'metro': 'Transportation',
    'flight tickets': 'Transportation',
    
    # Gifts and Special Occasions
    'souvenirs': 'Souvenirs/Gifts/Treats',
    'treat': 'Souvenirs/Gifts/Treats',
    'gift': 'Souvenirs/Gifts/Treats',
    
    # Other
    'misc': 'Miscellaneous'
}
```

## Installation and Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Libraries
```bash
streamlit
pandas
plotly
seaborn
numpy
```

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-analysis-dashboard.git
   cd expense-analysis-dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. **Data Preparation**
   - Ensure your Excel file follows the required format
   - Verify date formatting (YYYY-MM-DD)
   - Check for consistent category names

2. **Launching the Dashboard**
   - Access the dashboard through your web browser
   - Upload your expense data file
   - Select your preferred analysis period

3. **Analysis Options**
   - Choose between yearly, monthly, or custom date range views
   - Toggle category grouping options
   - Interact with visualizations for detailed insights

4. **Interpreting Results**
   - Review key metrics at the top of the dashboard
   - Explore category distributions through various charts
   - Analyze spending trends over time
   - Export visualizations or data as needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dad: When I moved to Canada for 3 months, he suggested keeping a track of expenses, I didn't ¯\_(ツ)_/¯. But when after I moved to Japan, I have kept a record since day 1.
- Samarth: He gave me the idea to make an app instead of using jupyter notebooks.

## Support

For support, please open an issue in the GitHub repository or contact Sajag directly.
