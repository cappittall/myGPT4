import streamlit as st
import pandas as pd
import numpy as np 
import time


def what_happening(img):
    print(type(image), image )
    
image = st.camera_input('Taka a picture leen', on_change="what_happening")

