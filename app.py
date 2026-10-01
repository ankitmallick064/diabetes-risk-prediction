import streamlit as st
import numpy as np
import pickle
from pathlib import Path

class sav:
    """Utility wrapper for pickle-based model files (.sav/.sav)."""

    @staticmethod
    def load(path):
        """Load a serialized object from a .sav/.sav file."""
        file_path = Path(path)
        candidates = [file_path]

        if file_path.suffix.lower() not in {'.sav', '.sav'}:
            candidates.extend([
                file_path.with_suffix('.sav'),
                file_path.with_suffix('.sav')
            ])

        for candidate in candidates:
            if candidate.exists():
                with candidate.open('rb') as file:
                    return pickle.load(file)

        raise FileNotFoundError(f"Model file not found: {file_path}")

    @staticmethod
    def save(path, obj):
        """Save an object to a .sav file."""
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('wb') as file:
            pickle.dump(obj, file)
        return file_path


loaded_model = sav.load('diabetes_model.sav')
pickle.load(open('diabetes_model.sav'))

# 1. Custom CSS for Visual Styling (Colors, Fonts, Backgrounds)
# This acts like your palette, setting the aesthetic tone of the page.
st.markdown("""
<style>
    /* Changes the background color of the main app */
    .stApp {
        background-color: #f5f5dc;
    }
    
    /* Styles the main title */
    h1 {
        color: #5c4033;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Styles the secondary text */
    p {
        font-size: 18px;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

# 2. Building the Visual Structure
st.title('🩺 Diabetes Risk Predictor')
st.write("---")

st.markdown("<p style='text-align: center;'>Enter your health metrics below for an instant preliminary screening.</p>", unsafe_allow_html=True)
st.write("") 

# 3. Arranging Elements in a Grid with explicit step values
col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Patient Age:', min_value=0, max_value=120, value=0, step=1)
    glucose = st.number_input('Glucose Level(in milligrams per deciliter):', min_value=0, value=0, step=1)
    insulin = st.number_input('insulin level(in microunits per milliliter):', min_value=0, value=0 , step=1)
    diabetespedigreefunction = st.number_input('diabetes pedigree function:', min_value=0, value=0, step=1)
    blood_pressure = st.number_input('Blood Pressure (mm Hg):', min_value=0, value=0, step=1)


with col2:
    weight = st.number_input('Weight (kg):', min_value=0, value=150, step=1)
    height_cm = st.number_input('Height (cm):', min_value=0, value=200, step=1)
    number_of_pregnancies = st.number_input('Number of pregnancies :',min_value=0, value=0, step=1)     
    skinthickness = st.number_input('Skinthickness(in mm) :' ,min_value=0 , value=0, step=0)
    st.write("---")

# 4. Designing the Button Area and Calculating BMI
if st.button('Predict Diabetes Risk', use_container_width=True):
        # Step A: Calculate the BMI
        height_m = height_cm / 100
        calculated_bmi = weight / (height_m ** 2)
        st.info(f"Your calculated BMI is: {calculated_bmi:.1f}")
        
        # Step B: Package the data EXACTLY in the order Anik's model expects it
        # Assuming the model trained on: Age, Glucose, Blood Pressure, BMI
        input_data = np.array([[age, glucose, blood_pressure, calculated_bmi,insulin ,number_of_pregnancies, skinthickness,diabetespedigreefunction]])
        
        # Step C: Ask the loaded model to make a prediction
        prediction = loaded_model.predict(input_data)
        
        # Step D: Display the final result
        st.write("---")
        if prediction[0] == 1:
         st.error("⚠️ HIGH RISK: The model indicates a high probability of diabetes. Please consult a doctor.")
        else:
         st.success("✅ LOW RISK: The model indicates a low probability of diabetes. Keep up the healthy lifestyle!")
            
else:
    st.write("please fill the valid details")


