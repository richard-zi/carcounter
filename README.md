# Car Counter

## Description

Car Counter is a potent tool designed to count and categorize vehicles in real-time. With the use of advanced object detection algorithms, this application processes video streams to identify and classify various vehicle types, offering crucial insights and data.

## Features

- **Real-Time Vehicle Counting:** Process video streams to enumerate vehicles in real-time.
- **Vehicle Classification:** Distinguish and categorize diverse vehicle types.
- **Data Visualization:** Represent the processed data for enhanced insights and comprehension.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/richard-zi/carcounter.git
```

2. Go to the project directory:
```bash
cd carcounter
```

3. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the main application:
```bash
streamlit run main.py
```

2. Start the server application:
```bash
python manage.py runserver
```

## Technologies Used

Several state-of-the-art technologies underpin this project to conduct object detection and vehicle counting:

- **YOLOv8:** A superior object detection algorithm employed for instantaneous object detection. YOLOv8 excels at spotting and categorizing multiple objects in images and videos promptly and precisely.

- **ByteTrack:** A top-tier tracking algorithm harnessed to preserve the identities of spotted objects over several video frames. It guarantees reliable and precise vehicle tracking across the video sequences.

- **Streamlit:** A swift, intuitive open-source app framework tailored for crafting bespoke web apps in machine learning and data science domains. In this initiative, Streamlit facilitates the design of a dashboard that manifests the outcomes and insights drawn from the vehicle counting mechanism.

## Dashboard

The Streamlit dashboard, crafted for user ease, permits users to engage with the application, designate video streams for processing, and monitor the results instantaneously. The dashboard offers a panoramic view of the data, delineating the vehicle counts and types in a coherent and discernible fashion.

## How to Access the Dashboard

1. Post launching the main application, a local web server will initialize.
2. Activate your web browser and proceed to the URL shown in the terminal.
3. Engage with the dashboard to designate video streams and observe the processed outcomes.

## Acknowledgements

Our gratitude extends to the ingenious creators behind YOLOv8, ByteTrack, and Streamlit for conceiving and sustaining these stellar technologies. Their contributions have significantly propelled the triumph of this endeavor.

## Contributors

This endeavor is a joint venture between:

- [Richard Zimmermann](https://github.com/richard-zi) 
- [Moritz von Angern](https://github.com/movonangern)

Our heartfelt appreciation goes out to Moritz von Angern for his pivotal contributions and partnership throughout this application's evolution. His acumen and insights have been instrumental in realizing the project's vision.

For queries, challenges, or potential contributions, please feel free to approach us.

## License

This project is open-source and can be accessed under the [MIT License](LICENSE). 
