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


def generate_text(prompt):
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
        repetition_penalty=1.2,  # Penaliza repeticiones
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def generate_property_features(property_data):
    """
    Genera una lista simplificada de características de propiedad.

    :param property_data: Diccionario con datos de la propiedad.
    :return: Lista de características como texto.
    """
    feature_map = {
        "lotarea": lambda v: f"Lot size: {v} sq ft.",
        "grlivarea": lambda v: f"Living area: {v} sq ft.",
        "yearbuilt": lambda v: f"Year built: {v}.",
        "overallqual": lambda v: f"Quality rating: {v}/10.",
        "fullbath": lambda v: f"{v} full bathroom{'s' if v > 1 else ''}.",
        "garagecars": lambda v: f"Garage: space for {v} car{'s' if v > 1 else ''}.",
        "neighborhood": lambda v: f"Neighborhood: {v}.",
        "housestyle": lambda v: f"Style: {v}.",
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
        f"Write a professional real estate listing for the property described below. "
        f"Include only the provided details. The description should:\n"
        f"- Be concise and persuasive.\n"
        f"- Avoid repeating features.\n"
        f"- Focus only on the property without adding unrelated details.\n\n"
        f"Property Highlights: {description}\n"
        f"Property Features:\n{features_text}"
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


def generate_customer_profiles_prompt(listing_text):
    """
    Genera un prompt claro y estructurado para generar perfiles de clientes.
    """
    return (
        "You are a market analyst specializing in real estate. "
        "Based on the property listing below, generate five distinct customer profiles of potential buyers who might be interested in purchasing this property. "
        "Each profile should be in the following format:\n\n"
        "- **Occupation**: [e.g., Software Engineer, Doctor, Retired Teacher]\n"
        "- **Annual Income Range**: [$100,000-$150,000, $50,000-$80,000, etc.]\n"
        "- **Key Reasons for Interest**: [Describe why this property suits them.]\n"
        "- **Lifestyle or Demographic Information**: [Family with kids, young professionals, etc.]\n\n"
        f"Property Listing:\n{listing_text}\n\n"
        "Please list each profile as a bullet point and keep the responses concise."
    )


def generate_customer_profiles(listing_text):
    """
    Genera perfiles de cliente para un listado de propiedades.
    """
    if not listing_text.strip():  # Manejo de entradas vacías o solo espacios
        return "No customer profiles"

    prompt = generate_customer_profiles_prompt(listing_text)
    return generate_text(prompt)


def generate_customer_profiles(listing_text):
    """
    Genera perfiles de cliente para un listado de propiedades.
    """
    if not listing_text.strip():  # Manejo de entradas vacías o solo espacios
        return "No customer profiles"

    prompt = f"Generate customer profiles for the following listing:\n{listing_text}"
    return generate_text(prompt)
