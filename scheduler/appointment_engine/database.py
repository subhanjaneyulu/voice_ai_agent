appointments_db = []
doctor_master = {
    101: "cardiologist",
    102: "dermatologist",
    103: "neurologist",
    104: "orthopedic",
    105: "ent specialist",
    106: "ophthalmologist",
    107: "dentist",
    108: "pediatrician",
    109: "general physician",
    110: "gynecologist",
    111: "psychiatrist",
    112: "urologist",
    113: "oncologist",
    114: "gastroenterologist",
    115: "endocrinologist",
    116: "pulmonologist",
    117: "nephrologist"
}

doctor_name_to_id = {v: k for k, v in doctor_master.items()}
doctor_schedule_db = {
    "cardiologist": {
        "tomorrow": ["10:30 AM", "2:00 PM", "4:30 PM"]
    },
    "dermatologist": {
        "tomorrow": ["11:00 AM", "3:00 PM"]
    },
    "neurologist": {
        "tomorrow": ["1:00 PM", "5:00 PM"]
    },
    "orthopedic": {
        "tomorrow": ["9:30 AM", "12:30 PM"]
    },
    "ent specialist": {
        "tomorrow": ["10:00 AM", "1:30 PM"]
    },
    "ophthalmologist": {
        "tomorrow": ["11:30 AM", "3:30 PM"]
    },
    "dentist": {
        "tomorrow": ["9:00 AM", "12:00 PM", "4:00 PM"]
    },
    "pediatrician": {
        "tomorrow": ["10:00 AM", "2:30 PM"]
    },
    "general physician": {
        "tomorrow": ["9:00 AM", "11:00 AM", "1:00 PM", "5:00 PM"]
    },
    "gynecologist": {
        "tomorrow": ["10:15 AM", "1:15 PM"]
    },
    "psychiatrist": {
        "tomorrow": ["2:00 PM", "6:00 PM"]
    },
    "urologist": {
        "tomorrow": ["11:45 AM", "3:45 PM"]
    },
    "oncologist": {
        "tomorrow": ["12:30 PM", "4:30 PM"]
    },
    "gastroenterologist": {
        "tomorrow": ["9:45 AM", "2:15 PM"]
    },
    "endocrinologist": {
        "tomorrow": ["10:45 AM", "3:15 PM"]
    },
    "pulmonologist": {
        "tomorrow": ["11:15 AM", "4:45 PM"]
    },
    "nephrologist": {
        "tomorrow": ["1:15 PM", "5:15 PM"]
    }
}