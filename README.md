# Real Estate Sales and Customer Profiling Application

This repository hosts a Real Estate Sales and Customer Profiling Application, a robust toolset designed for analyzing,
marketing, and managing property data. Leveraging state-of-the-art Machine Learning (ML) models and Large Language
Models (LLMs), the application enables the prediction of property prices, the generation of professional sales listings,
and the creation of tailored customer profiles for potential buyers.

The backend API is built with Django and Django Rest Framework, and the user interface is developed using Gradio for a
seamless and interactive experience. Additionally, the project is fully compatible with Google Colab, allowing for quick
deployment and showcasing without the need for local setup.

## Features

### Tabs Overview

#### 1. **Predict Property Prices and Record Verified Sales**

- **Predict Property Prices**:
    - Input various property parameters such as:
        - Lot size, living area, neighborhood, year built, and more.
    - Uses a pre-trained regression model based on the **Ames Housing Dataset** to predict property sale prices.
    - Model: A PyTorch-based neural network trained on features from the dataset.
- **Record Verified Sales**:
    - Users can save "verified" sales properties to the database for future analysis.
    - Ensures accurate tracking of actual market values for further predictions.

#### 2. **Search, Generate Sales Listings, and Customer Profiles**

- **Search for Closest Properties**:
    - Find properties most similar to user-defined parameters.
    - Includes filters like lot size, overall quality, number of bathrooms, and neighborhood.
- **Generate Salesy Listings**:
    - Creates professional property listings using:
        - User-provided highlights (e.g., "Has a private tennis court").
        - Detailed property features derived from the dataset (e.g., "Lot size: 12000 sq ft").
    - Model: **google/flan-t5-large**, a powerful transformer-based language model.
    - Ensures that the generated listings:
        - Are concise, accurate, and persuasive.
        - Do not fabricate missing information.
- **Generate Customer Profiles**:
    - Generates realistic buyer profiles tailored to the property, including:
        - Occupation.
        - Approximate annual income.
        - Reasons why the property suits their needs.
        - Lifestyle preferences.
    - Profiles are generated based on both the listing description and property features.
    - Model: **google/flan-t5-large**.

Also, the built-in Django Admin allows administrators to inspect and modify data, including properties, listings, and
verified sales.

## Dataset

The application is built on the **Ames Housing Dataset**, a rich and detailed dataset of property features.

## Installation

### Prerequisites

- Python 3.10+
- Pipenv or virtualenv
- Internet connection (for downloading Hugging Face models)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/faustow/respp.git
   cd respp
   ```

2. Set up a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure access tokens for Hugging Face and Ngrok:
   ```bash
   export HUGGINGFACE_TOKEN=<your_huggingface_token>
   export NGROK_TOKEN=<your_ngrok_token>
   ```

5. Apply database migrations:
   This will load the initial data into the database, splitting it into `training`, `validation` and `testing` datasets.
   ```bash
   python manage.py migrate
   ```

6. Run the Django development server and Gradio UI:
   ```bash
   python startservers.py
   ```

### License

This project is licensed under the MIT License.
