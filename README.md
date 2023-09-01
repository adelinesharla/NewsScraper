# Reuters News Scraper Robot

## Overview

The Reuters News Scraper Robot is an automation bot designed to run on RobotCorp. Built in Python and leveraging RPA (Robotic Process Automation), it searches for news articles on Reuters.com based on user-defined search terms, date ranges, and categories. The results are then exported to an Excel spreadsheet, featuring several key data points such as money patterns, term count, article titles, images, and dates.

## Features

- Searches Reuters.com for news articles using a given search term.
- Filters articles based on a defined number of months and category.
- Exports the extracted data to an Excel file with the following fields:
  - `money_pattern`: Count of money patterns like dollar values in the title.
  - `count_term`: Count of occurrences of the search term in the title.
  - `title`: Title of the news article.
  - `image`: Image related to the news article.
  - `date`: Publication date of the news article.

## Technology Stack

- Python
- RPA (Robotic Process Automation)
- Selenium WebDriver
- Excel for output
- Logging

## Design Patterns

- Object-Oriented Programming (OOP)
- Page Object Model (POM) for better code reusability and maintenance.
- Resilient Action Decorator for enhanced error handling and retries with wait times.

## Getting Started

### Input Schema

Here's an example of an input configuration:

```json
{
    "settings": {
        "base_url": "https://www.reuters.com/",
        "wait_time": 10
    },
    "search_term": "brazil womens",
    "month_number": 3,
    "category": "all"
}
```

### Main Entry Point

The entry point for the robot is the `main` function, which orchestrates all the steps in a sequential manner.

## Documentation

You can find detailed documentation in the `docs` folder. It contains:

- Input Schema: Describes the format for the input settings.
- Flowchart: Provides a visual representation of the bot's main workflow. Available in both PlantUML and png formats.

## Testing

The `tests` folder contains unit tests focused on the critical components of the system.

### Running Tests

```
python -m unittest test_data_extractor.py
python -m unittest test_scraper.py
```

## Known Issues and Limitations

### Main

- Investigate whether the `assets` Robotcorp would be more suitable for uploading Excel and PNG files.
- Parameters validation for the inputs should be implemented.

### Scraper

- Currently, the scraper does not handle news articles that feature carousels or videos in place of images.
- The `click_category_selection` function in `result_page` needs to be fixed for proper usage in `search_for_term_by_category`.
- It's unclear why some news articles are not being scraped. This needs further investigation.

### Decorator (Resilient Action)

- Parameterization of functions within the decorator is not fully understood. Requires further testing and analysis.
- Investigate other exceptions that could be handled and retried by the decorator.
- Look into preparatory actions that should be executed before retrying an operation. For example, in `open_website`, all other open windows should probably be closed before a retry attempt.