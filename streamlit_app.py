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

	#New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try: 
		#added after line 38
		#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
		#streamlit.write('The user entered', fruit_choice) 
if not fruit_choice:
	streamlit.error("Please select a fruit to get information.")
else
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
			#streamlit.text(fruityvice_response.json()) # Asked to remove this line after line 38 -- Removes the json data format line
			#take the json version of the respone and normalize it - put it into a table
	fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
			#output it on the screen as a table
	streamlit.dataframe(fruityvice_normalized)
except URLError as e:
	streamlit.error()
		
		
		
		
# don't run anything past here for troubleshooting
streamlit.stop()

#Add file to snowflake - Requirements.txt
#import snowflake.connector moved to top

#Lesson 12

#Streamlit Secrets
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
#my_cur.execute("select current_user(), Current_Account(), Current_Region()")
my_cur.execute("select * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()

#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
#streamlit.text(my_data_row)
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")

