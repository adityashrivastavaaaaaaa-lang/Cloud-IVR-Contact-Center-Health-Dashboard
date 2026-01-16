def ivr_routing(user_input):
    """
    Simulates IVR routing based on DTMF input.
    """
    if user_input == "1":
        return {
            "message": "Routing to Sales Queue...",
            "queue": "Sales",
            "action": "transfer"
        }
    elif user_input == "2":
        return {
            "message": "Routing to Support Queue...",
            "queue": "Support",
            "action": "transfer"
        }
    else:
        return {
            "message": "Target not found. Routing to Fallback/Operator...",
            "queue": "General",
            "action": "fallback"
        }
