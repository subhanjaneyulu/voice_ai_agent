def process_text(text: str):
    text = text.lower()
    
    if "book" in text or "appointment" in text or "schedule" in text:
        intent = "booking"
    elif "cancel" in text:
        intent = "cancel"
    elif "reschedule" in text or "change" in text:
        intent = "reschedule"
    elif "available" in text or "availability" in text or "slots" in text:
        intent = "check_availability"
    else:
        intent = "unknown"
    
    SPECIALISTS = {
        "cardio": "cardiologist",
        "heart": "cardiologist",
        "derma": "dermatologist",
        "skin": "dermatologist",
        "neuro": "neurologist",
        "brain": "neurologist",
        "ortho": "orthopedic",
        "bone": "orthopedic",
        "ent": "ent specialist",
        "ear": "ent specialist",
        "eye": "ophthalmologist",
        "vision": "ophthalmologist",
        "dentist": "dentist",
        "tooth": "dentist",
        "teeth": "dentist",
        "child": "pediatrician",
        "kid": "pediatrician",
        "general": "general physician"
    }

    doctor = None
    for key, value in SPECIALISTS.items():
        if key in text:
            doctor = value
            break

    
    date = None
    if "today" in text:
        date = "today"
    elif "tomorrow" in text:
        date = "tomorrow"
    elif "friday" in text:
        date = "friday"
    elif "next week" in text:
        date = "next week"
  
    time = None

    if "10" in text:
        time = "10:30 AM"
    elif "2" in text:
        time = "2:00 PM"
    elif "4" in text:
        time = "4:30 PM"
   
    if time is None and intent == "booking":
        time = "10:30 AM"
   
    return {
        "intent": intent,
        "doctor": doctor,
        "date": date,
        "time": time
    }