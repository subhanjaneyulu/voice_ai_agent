from scheduler.appointment_engine.booking import book_appointment
from scheduler.appointment_engine.availability import check_availability
from scheduler.appointment_engine.cancel import cancel_appointment
from scheduler.appointment_engine.reschedule import reschedule_appointment

def handle_tools(agent_output):

    if not isinstance(agent_output, dict):
        return {
            "status": "failed",
            "message": "Invalid agent output"
        }

    intent = agent_output.get("intent")
    doctor = agent_output.get("doctor")
    date = agent_output.get("date")
    time = agent_output.get("time")

    if intent == "booking":

        if doctor == "unknown_doctor":
            return {
                "status": "failed",
                "message": "Invalid doctor"
            }

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

        if not time:
            availability = check_availability(doctor, date)

            slots = availability.get("available_slots") if isinstance(availability, dict) else []

            return {
                "status": "failed",
                "message": "Please choose a time slot",
                "doctor": doctor,
                "date": date,
                "available_slots": slots or []
            }

        result = book_appointment(doctor, date, time)

        if not isinstance(result, dict):
            return {
                "status": "failed",
                "message": "Booking failed due to internal error"
            }

        return result

    elif intent == "check_availability":

        if doctor == "unknown_doctor":
            return {
                "status": "failed",
                "message": "Invalid doctor"
            }

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

        result = check_availability(doctor, date)
        
        if isinstance(result, dict) and "available_slots" in result:
            return {
                "status": "success",
                "message": f"Available slots are {', '.join(result['available_slots'])}",
                "available_slots": result["available_slots"]
            }

        return result

    elif intent == "cancel":
        result = cancel_appointment()

        return {
            "status": "success",
            "message": result.get("message", "Appointment cancelled") if isinstance(result, dict) else "Appointment cancelled"
        }

    elif intent == "reschedule":

        if not date:
            return {
                "status": "failed",
                "message": "Please specify new date"
            }

        result = reschedule_appointment(date)

        return {
            "status": "success",
            "message": result.get("message", "Appointment rescheduled") if isinstance(result, dict) else "Appointment rescheduled"
        }

    return {
        "status": "failed",
        "message": "I didn't understand your request. Please try again."
    }