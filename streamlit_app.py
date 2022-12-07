import streamlit
import pandas
import requests 
import snowflake.connector
	#Error message handler
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥗Omega 3 & Blueberry Oatmeal')
streamlit.text('🥣Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🍞🥑Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#------------------------------------------------------------------------------------------------------------
#		Choose Fruit
#------------------------------------------------------------------------------------------------------------
	#import pandas -- Moved to top
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

	# Picklist here so they can pick the furit they want to include
	# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
	# The dropdown is here in the list as my_fruit_index
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

	# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)  


#------------------------------------------------------------------------------------------------------------
#		Function
#------------------------------------------------------------------------------------------------------------
#create the repeatable code block - FUNCTION
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) 
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
	return fruityvice_normalized 

#------------------------------------------------------------------------------------------------------------
#		Select Fruit and show details from API above
#------------------------------------------------------------------------------------------------------------
	#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try: 
		#added after line 38
		#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	 
	if not fruit_choice:
		streamlit.error("Please select a fruit to get information.")
	else:
		back_from_function = get_fruityvice_data(fruit_choice) 
		#output it on the screen as a table
		streamlit.dataframe(back_from_function)
except URLError as e:
	streamlit.error()


#------------------------------------------------------------------------------------------------------------
#		List all fruit in Snowflake table using a button
#------------------------------------------------------------------------------------------------------------
streamlit.header("The fruit load list contains:") 
#Snowflake-related functions
def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from fruit_load_list") 
		return my_cur.fetchall()
#Add a button to load the fruit list
if streamlit.button('Get Fruit Load List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	my_data_rows = get_fruit_load_list()
	my_cnx.close()
	streamlit.dataframe(my_data_rows)
	

#------------------------------------------------------------------------------------------------------------
#		Add Fruit with button
#------------------------------------------------------------------------------------------------------------	
#	Allow the end user to add a fruit to the list
def insert_row_snoflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
		return 'Thanks for adding ' + new_fruit


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	back_from_function = insert_row_snoflake(add_my_fruit)
	my_cnx.close()
	streamlit.text(back_from_function)
	
	


	
		
		
# don't run anything past here for troubleshooting
streamlit.stop()
 

  


