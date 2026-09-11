"""Disease labels and farmer-friendly recommendations for KisanSense."""

CLASS_NAMES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Citrus_Canker", "Orange___Haunglongbing_(Citrus_greening)", "Orange___Multiple_Diseases",
    "Orange___Nutrient_Deficiency", "Orange___healthy", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight",
    "Potato___healthy", "Raspberry___healthy", "Soybean___Bacterial_Pustule", "Soybean___Brown_Spot",
    "Soybean___Crestamento", "Soybean___Ferrugen", "Soybean___Frogeye_Leaf_Spot", "Soybean___Mosaic_Virus",
    "Soybean___Powdery_Mildew", "Soybean___Rust", "Soybean___Septoria", "Soybean___Southern_Blight",
    "Soybean___Sudden_Death_Syndrome", "Soybean___Target_Leaf_Spot", "Soybean___Yellow_Mosaic",
    "Soybean___healthy", "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
]


def _display(label):
    return label.replace("___", " — ").replace("_", " ").replace("  ", " ").strip()


DISEASE_INFO = {}
for _label in CLASS_NAMES:
    _healthy = _label.lower().endswith("healthy")
    if _healthy:
        description = "The model classified the submitted leaf as healthy. No characteristic disease pattern was detected."
        treatment = "Continue regular irrigation, balanced nutrition, field sanitation and routine pest scouting."
    else:
        description = f"The image pattern is consistent with {_display(_label)}. Confirm the diagnosis in the field before treatment."
        treatment = "Remove severely affected leaves when practical, improve airflow, avoid unnecessary overhead irrigation, and follow locally approved integrated pest and disease management guidance."
    DISEASE_INFO[_label] = {
        "title": _display(_label),
        "description": description,
        "treatment": treatment,
        "is_healthy": _healthy,
    }

# More specific farmer guidance for common classes.
_OVERRIDES = {
    "Tomato___Late_blight": ("Tomato Late Blight", "Rapidly spreading dark water-soaked lesions can occur under cool, humid conditions.", "Remove badly infected foliage, keep leaves dry, improve airflow, and use only locally registered fungicides according to the label."),
    "Tomato___Early_blight": ("Tomato Early Blight", "Dark leaf spots with concentric target-like rings are typical of early blight.", "Remove lower infected leaves, mulch soil splash, avoid overhead watering, and follow local fungicide label guidance."),
    "Potato___Late_blight": ("Potato Late Blight", "A destructive disease that can spread quickly in cool, wet conditions.", "Inspect the crop frequently, remove heavily infected material, avoid prolonged leaf wetness, and follow local extension guidance."),
    "Apple___Apple_scab": ("Apple Scab", "Olive-green to dark lesions can develop on leaves and fruit.", "Sanitize fallen leaves, improve canopy airflow, and follow a locally approved preventive spray program."),
    "Orange___Citrus_Canker": ("Citrus Canker", "Raised corky lesions with yellow halos can occur on citrus leaves and fruit.", "Avoid moving infected plant material, sanitize tools, reduce wind-driven splash where possible, and contact local agriculture authorities for management guidance."),
}
for _label, (_title, _description, _treatment) in _OVERRIDES.items():
    if _label in DISEASE_INFO:
        DISEASE_INFO[_label].update(title=_title, description=_description, treatment=_treatment, is_healthy=False)


def get_recommendations(class_name):
    """Return a stable recommendation object for a model class."""
    if class_name in DISEASE_INFO:
        return DISEASE_INFO[class_name]
    return {
        "title": _display(str(class_name)),
        "description": "The model returned a class without a matching recommendation entry.",
        "treatment": "Treat this result as a screening signal and confirm the crop condition with a qualified local agronomist before applying chemicals.",
        "is_healthy": False,
    }
