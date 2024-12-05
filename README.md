# Soccer Results Scraper

A Python-based scraper built with Selenium to extract football match results and store them in a PostgreSQL database for data analysis and reporting.

---

## 📜 Description

This project scrapes football match results from a specified webpage, processes the data into a structured format, and saves it in a PostgreSQL database for further analysis. The tool is ideal for academic, research, and business purposes like statistical analysis, prize distribution, and recommendation systems.

---

## 🏗️ Project architecture

The project is structured as follows:

```
scrap_bests/
│
├── README.md
├── requirements.txt
├── autors.md
├── origin_data.txt
├── .gitignore
├── src/
│   ├── stage3/
│   │   ├── confi.py
│   │   ├── model.py
│   │   ├── reader_excel.py
│   │   ├── scraper.py
│   │   ├── treat_data.py
│   │   └── main.py
```

## 📦 Package descriptions

1. **src/stage3**: Contains files of classes and functions for web scraping, data transformation, and database interactions in stage 3.


## 🛠️ Technologies Used

- **Python**: Core programming language.
- **Selenium**: Web scraping framework to interact with webpages.
- **PostgreSQL**: Database for storing scraped data.
- **Pandas**: Data analysis and manipulation library.
- **SQLAlchemy**: ORM for managing database interactions.

## 🚀 Steps: installation and configuration

1. Clone this repository:

```bash
git clone [https://github.com/your-username/soccer-results-scraper.git](https://github.com/DarFelix/scrap_bets.git)
```
1. Create a virtual environment using the following command, making sure you are in the project folder path (...activity3/):

```bash
python -m venv venv1
```

2. Activate the virtual environment from the same path using the command:

```bash
venv1\Scripts\activate
```

3. Install the required packages from the same path using the following command. This process may take a few seconds:

```bash
pip install psycopg2-binary pandas openpyxl sqlalchemy selenium webdriver-manager
```

4. Update Python's pip to avoid the yellow warning that appeared earlier:

```bash
python.exe -m pip install --upgrade pip
```

5. Ensure that the Chrome Driver executable file used in class (chromedriver.exe) is located in the following path:

```bash
...\activity3\src\stage3\static\driver\chromedriver.exe
```

6. Run the project's main script (make sure the Excel file containing the general list of teams is not open):

```bash
.../activity3/src/stage3/main.py
```

7. Check the console logs, scraping results, and the creation of tables with records in the PostgreSQL database.

8. Execute the Power BI file and confirm the connection to the tb_report table to view the updated report.

### Prerequisites

1. **Install Python**: Download and install [Python 3.7+](https://www.python.org/downloads/).
2. **Set Up PostgreSQL**: Install and configure [PostgreSQL](https://www.postgresql.org/download/).
3. **Download ChromeDriver**: Ensure it matches your browser version ([ChromeDriver](https://sites.google.com/chromium.org/driver/)).

## ⚠️ Additional Considerations
Terms of Service: Ensure that scraping complies with the target website’s terms of service.
Rate Limiting: Adjust scraping frequency to avoid server bans.
Error Handling: The scraper includes basic exception handling but may require customization for specific scenarios.

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.

## 🤝 Contributions
Contributions are welcome!

Fork the repository.
Create a _feature branch_ (git checkout -b feature-name).
Submit a _pull request_ with a detailed description of your changes.

Happy scraping! ⚽
