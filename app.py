import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

# Load the model
try:
    model = load_model("Custom_Structure_Animal_Classification_VGG16_v2.h5")
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()  # Stop the app if model loading fails

# Class labels (update these with your actual class names)
CLASS_NAMES = ['Class A', 'Class B', 'Class C', 'Class D']  # Replace with your model's class labels

# Function to preprocess the uploaded image
def preprocess_image(image):
    try:
        # Resize the image to 224x224 (VGG16 expected input size)
        image = image.resize((224, 224))
        # Convert image to array and normalize pixel values
        image_array = img_to_array(image) / 255.0
        # Add batch dimension
        return np.expand_dims(image_array, axis=0)
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None

# Streamlit App
st.title("Animal Classification App")
st.write("Upload an image of an animal to classify it.")

# Upload image
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Open and display the uploaded image
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Preprocess the image and make predictions
        st.write("Processing image...")
        img_data = preprocess_image(image)

        if img_data is not None:
            predictions = model.predict(img_data)
            
            # Determine the predicted class
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class = CLASS_NAMES[predicted_class_index]
            confidence = predictions[0][predicted_class_index] * 100  # Convert to percentage

            # Display the prediction and confidence level
            st.write(f"### Predicted Class: {predicted_class}")
            st.write(f"Confidence: {confidence:.2f}%")
        else:
            st.error("Image preprocessing failed.")
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")
