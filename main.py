import requests
import json
import streamlit as st

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fdcba4c7-5533-492c-9ef1-bb2146f2958e"
FLOW_ID = "c0f84caf-1c46-45f5-bdfd-f4368b56db9b"
ENDPOINT = "FMS" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"authorization": st.secrets ["auth_key"], "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Hartron FMS Portal")
    
    message = st.text_area("Message")
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Running flow..."):
                response = run_flow(message)
            
            response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
