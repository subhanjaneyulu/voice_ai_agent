from scheduler.appointment_engine.database import appointments_db
from scheduler.appointment_engine.database import doctor_schedule_db

DOCTOR_NAMES = {
    "cardiologist": "Dr. Sharma",
    "dermatologist": "Dr. Mehta",
    "neurologist": "Dr. Rao",
    "orthopedic": "Dr. Reddy",
    "ent specialist": "Dr. Khan",
    "ophthalmologist": "Dr. Iyer",
    "dentist": "Dr. Gupta",
    "pediatrician": "Dr. Priya",
    "general physician": "Dr. Kumar",
    "gynecologist": "Dr. Anjali",
    "psychiatrist": "Dr. Verma",
    "urologist": "Dr. Singh",
    "oncologist": "Dr. Das",
    "gastroenterologist": "Dr. Nair",
    "endocrinologist": "Dr. Patel",
    "pulmonologist": "Dr. Ali",
    "nephrologist": "Dr. Joseph"
}


def book_appointment(doctor, date, time):

    
    if not doctor:
        return {"status": "failed", "message": "Doctor not specified"}

    if not date:
        return {"status": "failed", "message": "Date not specified"}

    if not time:
        return {"status": "failed", "message": "Please specify time"}

    
    available_slots = doctor_schedule_db.get(doctor, {}).get(date, [])

    
    if not available_slots:
        tomorrow_slots = doctor_schedule_db.get(doctor, {}).get("tomorrow", [])

        if tomorrow_slots:
            return {
                "status": "failed",
                "message": f"No slots available for {date}. Available slots for tomorrow are {', '.join(tomorrow_slots)}",
                "suggested_date": "tomorrow",
                "available_slots": tomorrow_slots
            }
        else:
            return {
                "status": "failed",
                "message": "No slots available. Please try another doctor."
            }

   
    if time not in available_slots:
        return {
            "status": "failed",
            "message": f"Requested slot not available. Available slots are {', '.join(available_slots)}",
            "available_slots": available_slots
        }

    
    for appt in appointments_db:
        if appt["doctor"] == doctor and appt["date"] == date and appt["time"] == time:

            remaining_slots = [slot for slot in available_slots if slot != time]

            if remaining_slots:
                return {
                    "status": "failed",
                    "message": f"That slot is already booked. Available slots are {', '.join(remaining_slots)}",
                    "available_slots": remaining_slots
                }
            else:
                return {
                    "status": "failed",
                    "message": "All slots are booked for this date. Try another day."
                }

    appointment = { 
        "id": len(appointments_db) + 1,
        "patient_id": 101,  
        "doctor": doctor,
        "doctor_name": DOCTOR_NAMES.get(doctor, f"Dr. {doctor.title()}"),
        "date": date,
        "time": time,
        "status": "booked"
    }

   
    appointments_db.append(appointment)

    return {
        "status": "success",
        "message": f"Your appointment with {appointment['doctor_name']} is booked for {date} at {time}",
        "appointment": appointment
    }