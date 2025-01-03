from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Variables globales
model = None
tokenizer = None
MODEL_NAME = "google/flan-t5-large"


def get_llm_model_and_tokenizer():
    """
    Carga el modelo y el tokenizer compatibles desde HuggingFace.
    """
    global model, tokenizer
    if model is None or tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return model, tokenizer


def generate_text(prompt, temperature=0.5, top_p=0.8):
    """
    Genera texto basado en un prompt usando el modelo cargado.

    :param prompt: Texto de entrada para el modelo.
    :return: Respuesta generada por el modelo.
    """
    model, tokenizer = get_llm_model_and_tokenizer()
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.5,  # Reduce la creatividad
        top_p=0.8,  # Focaliza las palabras más probables
        do_sample=True,
        repetition_penalty=1.3,  # Penaliza repeticiones
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_property_features(property_data):
    """
    Genera una lista simplificada de características de propiedad.

    :param property_data: Diccionario con datos de la propiedad.
    :return: Lista de características como texto.
    """
    feature_map = {
        # Tamaño y áreas
        "lotarea": lambda v: f"Lot size: {v} sq ft.",
        "grlivarea": lambda v: f"Living area: {v} sq ft.",
        "totalbsmtsf": lambda v: f"Basement area: {v} sq ft.",
        "garagesqft": lambda v: f"Garage area: {v} sq ft.",

        # Fecha y calidad de construcción
        "yearbuilt": lambda v: f"Year built: {v}.",
        "yearremodadd": lambda v: f"Last remodel year: {v}.",
        "overallqual": lambda v: f"Overall quality: {v}/10.",
        "overallcond": lambda v: f"Overall condition: {v}/10.",

        # Baños, habitaciones y otras estructuras
        "fullbath": lambda v: f"{v} full bathroom{'s' if v > 1 else ''}.",
        "halfbath": lambda v: f"{v} half bathroom{'s' if v > 1 else ''}.",
        "bedroomabvgr": lambda v: f"{v} bedroom{'s' if v > 1 else ''} above ground.",
        "totrmsabvgrd": lambda v: f"Total rooms: {v}.",
        "kitchenabvgr": lambda v: f"{v} kitchen{'s' if v > 1 else ''}.",
        "fireplaces": lambda v: f"{v} fireplace{'s' if v > 1 else ''}.",

        # Características externas
        "neighborhood": lambda v: f"Neighborhood: {v}.",
        "housestyle": lambda v: f"Style: {v}.",
        "roofstyle": lambda v: f"Roof style: {v}.",
        "paveddrive": lambda v: f"Paved driveway: {'Yes' if v == 'Y' else 'No'}.",
        "fence": lambda v: f"Fence: {v}.",

        # Precio de venta
        "saleprice": lambda v: f"Price: ${v:,.2f}.",

        # Características adicionales
        "wooddecksf": lambda v: f"Wooden deck area: {v} sq ft.",
        "screenporch": lambda v: f"Screened porch area: {v} sq ft.",
        "poolarea": lambda v: f"Pool area: {v} sq ft.",
        "garagecars": lambda v: f"Garage: space for {v} car{'s' if v > 1 else ''}.",
        "centralair": lambda v: f"Central air: {'Yes' if v == 1 else 'No'}.",
    }

    features = [
        formatter(value) for column, formatter in feature_map.items()
        if (value := property_data.get(column))  # Solo incluye características con valores no nulos
    ]
    return features


def generate_prompt_for_sales_listing(description, property_data):
    """
    Genera el prompt para crear un listado de ventas.
    """
    features = generate_property_features(property_data)
    features_text = "\n- ".join(features)

    return (
        f"You are a professional real estate copywriter. Write a sales listing using only the provided details. "
        f"DO NOT invent details for price, street, city, or other attributes not explicitly listed below.\n\n"
        f"Property Highlights: {description}\n"
        f"Property Details:\n- {features_text}\n\n"
        f"The listing should:\n"
        f"- Be concise and persuasive.\n"
        f"- Avoid repeating features.\n"
        f"- Avoid showing price.\n"
        f"- Only use the highlights and details provided above."
    )


def generate_sales_listing(description, property_data):
    """
    Genera un listado de ventas basado en los datos de una propiedad y una descripción.

    :param description: Texto proporcionado por el usuario sobre las mejores características de la propiedad.
    :param property_data: Diccionario que contiene los datos de la propiedad.
    :return: Texto generado para el listado de ventas.
    """
    prompt = generate_prompt_for_sales_listing(description, property_data)
    return generate_text(prompt)


def generate_customer_profiles_prompt(description, property_data):
    property_price = property_data.get('saleprice', 0)
    bedrooms = property_data.get('bedroomabvgr', 0)
    bathrooms = property_data.get('fullbath', 0)
    if property_data.get('halfbath'):
        bathrooms += property_data.get('halfbath', 0) * 0.5
    sqft = property_data.get('grlivarea', 0)
    min_income = property_price / 4

    return (
        f"Task: List 5 potential buyer profiles for a ${property_price} home.\n\n"
        f"Property details:\n"
        f"- Highlights: {description}\n"
        f"- Size: {sqft} square feet\n"
        f"- Bedrooms: {bedrooms}\n"
        f"- Bathrooms: {bathrooms}\n\n"
        f"- Area: {sqft} sq ft\n\n"
        f"Instructions:\n"
        f"Generate a list of 5 different occupations with their annual salaries. "
        f"Each buyer should have an annual income of at least ${min_income:,.0f}. "
        f"Make each occupation unique.\n\n"
        f"Expected format example:\n"
        f"1. Software Engineer - Annual salary: $150,000\n"
        f"2. Medical Doctor - Annual salary: $280,000\n"
        f"And so on...\n\n"
        f"Generate the list:"
    )


def generate_customer_profiles(description, property_data):
    """
    Genera perfiles de cliente para un listado de propiedades.
    """
    if not property_data:  # Manejo de entradas vacías o solo espacios
        return "No info given, impossible to create customer profiles"

    prompt = generate_customer_profiles_prompt(description, property_data)
    return generate_text(prompt, temperature=0.6)
