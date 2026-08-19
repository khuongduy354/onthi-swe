def reservation_created(event_id, hotel_id):
    return {"eventId": event_id, "type": "ReservationCreated", "hotelId": hotel_id}

