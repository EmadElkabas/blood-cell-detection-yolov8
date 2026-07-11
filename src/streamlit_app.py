import streamlit as st
from PIL import Image
from ultralytics import YOLO

st.set_page_config(page_title="Blood Cell Detection (YOLOv8)")
st.title("Blood Cell Detection (YOLOv8)")
st.write("Upload a blood cell microscope image to detect RBC, WBC, and Platelets.")

WEIGHTS_PATH = "weights/best.pt"

@st.cache_resource
def load_model():
    model = YOLO(WEIGHTS_PATH)
    model.model.names = {0: "Platelets", 1: "RBC", 2: "WBC"}
    return model

model = load_model()

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)

    result = model.predict(image, conf=0.4)[0]
    st.image(result.plot()[..., ::-1], caption="Detections", use_column_width=True)

    st.subheader("Predictions")
    for box in result.boxes:
        st.write(f"{model.names[int(box.cls)]} — confidence: {float(box.conf):.2f}")
