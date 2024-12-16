
# Elasticity Analysis Toolkit

This toolkit provides methods for analyzing trade elasticity in response to changes in external factors, such as exchange rates.

## Features
1. **HS Code Level Analysis**: Elasticity computations for trade metrics (e.g., exports) at different HS code levels.
2. **Country-Level Analysis**: Elasticity computations for trade metrics at the country level.
3. **Top-N Weighted Trade**: Identifies top trade categories or countries contributing to elasticity.
4. **Data Export**: Saves results to Excel for further analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Prepare your export, import, and exchange rate data.
2. Update file paths in `elasticity_analysis_toolkit.py`.
3. Run the script:
   ```bash
   python elasticity_analysis_toolkit.py
   ```

## Requirements
- Python 3.7 or later
- Libraries: pandas, numpy, openpyxl

## License
This project is licensed under the MIT License.
