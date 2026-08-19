def apply(state, event):
    data = event["data"]
    if event["type"] == "StudentAdded":
        return {"id": data["id"], "name": data["name"], "score": None}
    if event["type"] == "ScoreRecorded":
        return {**state, "score": data["score"]}
    return state

