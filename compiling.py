import requests
import json
import streamlit as st


def frontend():
    st.title("Aditya's Flight Scanner")

    # User inputs
    kaha_sai = st.text_input("Kaha Sai:")
    kaha_jaoge = st.text_input("Kaha Jaoge:")
    kis_din = st.date_input("Kis Din:")
    # kitne_log_ho = st.number_input("Kitne Log Ho:", min_value=1, step=1)



    # API Calling with values 
    json_data = api(kaha_sai, kaha_jaoge, kis_din)

    # Extracting needed info from json
    if type(json_data) == dict :
        extracted_op = extractor(json_data)
    else:
        extracted_op = json_data


    if st.button("Submit"):    
        st.write("Here is the travel information you entered:")
        st.write(extracted_op)





def api(a,b,c):
    # API calling
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"

    querystring = {
        "fromEntityId": a,
        "toEntityId": b,
        "departDate": c,
        "currency": "INR",
        "cabinClass": "economy"
    }

    headers = {
        "x-rapidapi-key": "4f9529f17amsh7d137d2c5202282p11d28ajsncc975fbcbdff",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    # Check if response is valid
    if response.status_code == 200:
        json_data = response.json()

    else:
        json_data = "Error in fetching" + str(response.status_code) +"\n; API Quota is finished for this Month"

    return json_data
    # Check if json_data is None
    # if json_data == "Error in fetching" + str(response.status_code):
        




def extractor(json_data):
    output = ""

    # with open('final.txt', 'a') as dataa:
    #     dataa.write(Number)
    # dataa.close


    if json_data["data"] == None:
        output += str(json_data["errors"])
    else:
        for i in range(len(json_data['data']['itineraries'])):
            extracted_data = {
                "price": json_data['data']['itineraries'][i]['price']['raw'],
                "origin": json_data['data']['itineraries'][i]['legs'][0]['origin']['name'],
                "destination": json_data['data']['itineraries'][i]['legs'][0]['destination']['name'],
                "Time": json_data['data']['itineraries'][i]['legs'][0]['durationInMinutes'],
                "Stops": json_data['data']['itineraries'][i]['legs'][0]['stopCount'],
                "departure": json_data['data']['itineraries'][i]['legs'][0]['departure'].split("T")[-1],
                "arrival": json_data['data']['itineraries'][i]['legs'][0]['arrival'].split("T")[-1],
                "Airline": json_data['data']['itineraries'][i]['legs'][0]['carriers']['marketing'][0]['name'],
                "Airline Number": json_data['data']['itineraries'][i]['legs'][0]['segments'][0]['flightNumber']
            }
            search_number = f"{i+1})"
            # with open('final.txt', 'a') as dataa:
            #     dataa.write(search_number)
            #     dataa.write(json.dumps(extracted_data, indent=4))
            #     dataa.write("\n\n")
            

            output += search_number
            output += str(extracted_data).replace(",","\n")
            output += "\n\n"
    
    return output



# if st.button("Submit"):
#     # Creating a dictionary with the user input
#     travel_info = ""    
    
    
#     st.write("Here is the travel information you entered:")
#     st.write(travel_info)


# dry run 
frontend()