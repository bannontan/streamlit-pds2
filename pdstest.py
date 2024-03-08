import streamlit as st
from google.cloud import firestore
import json

st.set_page_config(page_title = "Ninkatec", page_icon = ":syringe:", layout = 'wide')
# Authenticate to Firestore with the JSON account key.
#db = firestore.Client.from_service_account_json("firestore.json")

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
df = firestrore.Client(credentials=creds, project='streamlit-pds2')
syringes_data = []
# Create a reference
##doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
##doc = doc_ref.get()

# Let's see what we got!
##st.write("The id is: ", doc.id)
##st.write("The contents are: ", doc.to_dict())

# Create a reference
##doc_ref = db.collection("syringes").document("syringe12345")

# Then get the data at that reference.
##doc = doc_ref.get()

# Let's see what we got!
##st.write("The id is: ", doc.id)
##st.write("The contents are: ", doc.to_dict())

##doc_ref = db.collection("syringes").document("syringe2")

# And then uploading some data to that reference
##doc_ref.set({
#	"syringe_sn": "sn2",
#	"syringe_needle_length": 4,
#    	"syringe_dosage_amount": 2
#})
##syringes_ref = db.collection("syringes")

# For a reference to a collection, we use .stream() instead of .get()
#for doc in syringes_ref.stream():
#	st.write("The id is: ", doc.id)
#	st.write("The contents are: ", doc.to_dict())

syringe_sn = st.number_input("Enter syringe serial number (Eg: 12345)", step = 1)
submit = st.button("Add new syringe")
if syringe_sn and submit:
	doc_ref = db.collection("syringes").document(f"sn{syringe_sn}")
	doc_ref.set({
		"syringe_sn": syringe_sn,
		"syringe_needle_length": 4,
		"syringe_dosage_amount": 1.0,
		"patient": "NIL"
	})

syringes_ref = db.collection("syringes")
for doc in syringes_ref.stream():
	syringe = doc.to_dict()
	#syringe_sn = doc["syringe_sn"]
	#syringe_needle_length = doc["syringe_needle_length"]
	#syringe_dosage_amount = doc["syringe_dosage_amount"]
	#patient = doc["patient"]
	syringes_data.append(syringe)

st.write("---")
st.table(syringes_data)
st.write("---")
	
st.title("Welcome to Ninkatec! :wave:" )

if 'needle_length' not in st.session_state:
    st.session_state['needle_length'] = 4
    
if 'dosage_amount' not in st.session_state:
    st.session_state['dosage_amount'] = 1.0

if 'device_sn' not in st.session_state:
    st.session_state['device_sn'] = 'sn 12345' # Device serial number

needle_length_col, dosage_amount_col = st.columns(2)

# Remotely adjust needle length
with needle_length_col:

    def set_needle_length(length_of_needle):
        # link to arduino and database, if successful then st.success else is the failure one
        #st.error(f"Needle length could not be adjusted remotely! Please try again or adjust manually.")
        st.session_state['needle_length'] = length_of_needle
        st.success(f"Needle length has successfully been set to {length_of_needle}!")

    st.header("Needle Length")
    needle_length = st.select_slider("Adjust the needle length here", options = [4, 6, 8, 10], value = 4)
    
    if st.button('Confirm Needle Length'):
        set_needle_length(needle_length)
    st.write(f'Needle length is {st.session_state.needle_length}mm')
    

# Remotely adjust dosage amount
    
with dosage_amount_col:

    def adjust_dosage(dosage):
        # link to db and send information to inform arduino to execute the change
        # if successful then return success, else return error
        #st.error(f"Dosage amount could not be adjusted remotely! Please try again or adjust manually.")
        st.session_state['dosage_amount'] = dosage
        st.success(f"Dosage amount has successfully been set to {dosage}!")
        

    st.header("Dosage amount")
    dosage_amount = st.number_input("Enter the dosage amount in ml: ", value = 1.0, step = 0.1)
    if st.button("Confirm Dosage Amount"):
        adjust_dosage(dosage_amount)

    st.write(f'Dosage amount is {st.session_state.dosage_amount}ml')

st.write("---")
# -- Connect to driver for injection of drugs --
#def device_connection(device, device_status):
#    if device_status == 'Disconnected':
        # connect to specific device
def administer_injection(device_serial_number):
    # link to the database and send input the adminster the injection
    # receive status from db if injection is done then output a success message
    st.success(f'{st.session_state.dosage_amount}ml injection for {device_serial_number} Administered Successfully on time and date.')
    # if unsuccessful then need to say to try again / ask them to do so manually

with st.container():
    st.header("Administer Injection")
    if st.button(f"Click To Adminster Injection for {st.session_state.device_sn}"):
        administer_injection(st.session_state.device_sn)
    

# Step by step tutorial for caregiver

# FAQ section

# Data/table of devices + users
#device_selection = st.selectbox("Select Device", ('Please Select', *available_devices))
