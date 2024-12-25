import streamlit as st
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",          # Replace with your MySQL username
            password="ramana",  # Replace with your MySQL password
            database="event management"   # Replace with your database name
        )
        if conn.is_connected():
            return conn
    except Error as e:
        st.error(f"Database Error: {e}")
        return None

def fetch_events():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT event_id, user_id, title, description, event_date FROM events"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            st.error(f"Error fetching events: {e}")
            return None
        finally:
            conn.close()

def display_events():
    events = fetch_events()
    if events:
        st.subheader("Events Found:")
        for event in events:
            st.write(f"**Event ID:** {event[0]}")
            st.write(f"**User ID:** {event[1]}")
            st.write(f"**Title:** {event[2]}")
            st.write(f"**Description:** {event[3]}")
            st.write(f"**Event Date:** {event[4]}")
            st.write("---")
    else:
        st.write("No events found in the database.")

def add_event(user_id, title, description, event_date):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO events (user_id, title, description, event_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user_id, title, description, event_date))
            conn.commit()
            st.success("Event added successfully!")
        except Exception as e:
            st.error(f"Error adding event: {e}")
        finally:
            conn.close()

def delete_event(event_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "DELETE FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            conn.commit()
            st.success("Event deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting event: {e}")
        finally:
            conn.close()

def update_event(event_id, title=None, description=None, event_date=None):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = "UPDATE events SET title = %s, description = %s, event_date = %s WHERE event_id = %s"
            cursor.execute(query, (title, description, event_date, event_id))
            conn.commit()
            st.success("Event updated successfully!")
        except Exception as e:
            st.error(f"Error updating event: {e}")
        finally:
            conn.close()

def main():
    st.title("Event Management System")

    menu = ["View All Events", "Add Event", "Update Event", "Delete Event"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "View All Events":
        display_events()

    elif choice == "Add Event":
        st.subheader("Add a New Event")
        user_id = st.text_input("User ID")
        title = st.text_input("Event Title")
        description = st.text_area("Event Description")
        event_date = st.date_input("Event Date")
        if st.button("Add Event"):
            add_event(user_id, title, description, event_date)

    elif choice == "Update Event":
        st.subheader("Update an Event")
        event_id = st.text_input("Event ID")
        title = st.text_input("New Title")
        description = st.text_area("New Description")
        event_date = st.date_input("New Event Date")
        if st.button("Update Event"):
            update_event(event_id, title, description, event_date)

    elif choice == "Delete Event":
        st.subheader("Delete an Event")
        event_id = st.text_input("Event ID to Delete")
        if st.button("Delete Event"):
            delete_event(event_id)

if __name__ == "__main__":
    main()
