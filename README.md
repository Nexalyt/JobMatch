# Coin Flip Simulator

A simple and interactive web application for simulating coin flips with an adjustable bias. The app keeps track of cumulative results and provides a visual comparison of the number of flips for each side.

## Features

- **Adjustable Bias**: Use a slider to set the probability of landing on "Cara."
- **Interactive Flipping**: Flip the coin by pressing a button and see the result immediately.
- **Cumulative Tracking**: The app remembers and displays the total number of "Cara" and "Cruz" flips.
- **Visual Representation**: A dynamic bar chart updates after every flip to compare the results.

## How to Use

1. Launch the app using Streamlit.
2. Adjust the bias probability using the slider.
3. Press the **Flip the Coin** button to flip the coin.
4. View the result and observe how the cumulative counts and the chart are updated.

## Installation

To run this app locally, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/Loretonavarro/app_test
   cd app_test
   ```

2. Install the required dependencies:

   ```bash
   pip install streamlit matplotlib
   ```

3. Run the app:

   ```bash
   streamlit run app.py --server.runOnSave true
   ```

4. Open the app in your browser at the URL provided by Streamlit.

## Example Usage

![Coin Flip Simulator](LINK)

1. Set the probability of landing on "Cara" using the slider.
2. Click the **Flip the Coin** button to see the result.
3. Watch as the cumulative results and chart update in real time.

## Technologies Used

- **Python**: The core programming language.
- **Streamlit**: For creating the interactive web interface.
- **Matplotlib**: For generating the bar chart visualizations.

## Contributing

Contributions are welcome! If you have suggestions for features or find any issues, feel free to open a pull request or submit an issue.

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy flipping coins and exploring probabilities with the Coin Flip Simulator!