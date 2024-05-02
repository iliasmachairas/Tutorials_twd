pre[class*="shiki"] {
    position: relative;
    margin: 5px 0;
    padding: 1.75rem 0 1.75rem 1rem;
}

.markup-docs > pre > .button-copy-code {
    @apply rounded;
    @apply bg-gray-300;
    @apply py-2 px-2;
    position: absolute;
    top: 85px;
    right: 15px;
}

@screen sm {
    .markup-docs > pre > .button-copy-code {
        top: 85px;
        right: 10px;
    }
}

.markup-docs > pre > .button-copy-code:hover {
    @apply border-2 border-gray-600;
    @apply bg-gray-200;
}

.markup-docs > pre > .button-copy-code:focus {
    @apply bg-gray-300;
}

.copy-docs-icon {
    fill: #0a001f;
}

.docs-copied-icon {
    color: #148a25 !important;
    fill: #148a25 !important;
}

# Fatal Road Accidents (FRA) Dashboard

## Description

![dash_LinkedIn-ezgif com-video-to-gif-converter](https://github.com/iliasmachairas/Tutorials_twd/assets/47300069/19cf7061-cdf6-4a8a-8a9c-a31fbb1c4d0b)

This project aims to visualize fatal road accidents (FRA) data in Athens from 2011 to 2015 using Dash, a Python framework for building analytical web applications. The dashboard allows users to explore FRA data based on vehicle type and year, presenting visualizations such as bar charts, pie charts, and a map.

## Installation

To run this application locally, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have Python installed. This project is developed using Python 3.
3. Install the required libraries by running:

pip install pandas dash plotly numpy

4. Run the application by executing the following command:

Dash_App_FRA app.py

5. Open a web browser and navigate to http://127.0.0.1:8050/ to view the dashboard.

## Usage

Upon launching the application, users are presented with options to select a vehicle type and year. Based on the selection, the dashboard dynamically updates to display relevant visualizations:

- **Bar Charts**: Displays the distribution of age groups involved in fatal road accidents.
- **Pie Chart**: Shows the distribution of accidents based on time of occurrence.
- **Map**: Visualizes the geographic distribution of accidents using a scatter map.

Users can interact with the dashboard to gain insights into the FRA data for Athens.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or feedback, feel free to contact the project maintainer:
- [Ilias Machairas]



