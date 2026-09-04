import requests
from datetime import datetime, timezone

ENTUR_API = "https://api.entur.io/journey-planner/v3/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "ET-Client-Name": "mikevidsen-trikkestopp",
}

ROSENHOFF = "NSR:StopPlace:58255"

QUERY = """
{
  stopPlace(id: "%s") {
    estimatedCalls(timeRange: 72100, numberOfDepartures: 5) {
      expectedDepartureTime
      destinationDisplay { frontText }
      serviceJourney {
        journeyPattern {
          line { publicCode }
        }
      }
    }
  }
}
""" % ROSENHOFF


def get_departures():
    response = requests.post(ENTUR_API, json={"query": QUERY}, headers=HEADERS, timeout=10)
    response.raise_for_status()
    calls = response.json()["data"]["stopPlace"]["estimatedCalls"]

    now = datetime.now(timezone.utc)
    departures = []
    for call in calls:
        line = call["serviceJourney"]["journeyPattern"]["line"]["publicCode"]
        destination = call["destinationDisplay"]["frontText"]
        expected = datetime.fromisoformat(call["expectedDepartureTime"])
        minutes = max(0, round((expected - now).total_seconds() / 60))
        if minutes == 0:
            departures.append(f"{line} {destination} Nå")
        else:
            departures.append(f"{line} {destination} {minutes} min")
    return departures

# TESTING
if __name__ == "__main__":
    for d in get_departures():
        print(d)