from scheduler.appointment_engine.database import (
    doctor_schedule_db,
    doctor_name_to_id
)
def check_availability(doctor, date):

    if not doctor:
        return {
            "status": "failed",
            "message": "Please specify doctor"
        }

    if not date:
        return {
            "status": "failed",
            "message": "Please specify date"
        }
    doctor_id = doctor_name_to_id.get(doctor)

    if not doctor_id:
        return {
            "status": "failed",
            "message": "Invalid doctor"
        }

    slots = doctor_schedule_db.get(doctor, {}).get(date, [])

    if not slots:
        return {
            "status": "failed",
            "message": "No slots available for this doctor. Please try another date."
        }

    return {
        "status": "success",
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": slots
    }