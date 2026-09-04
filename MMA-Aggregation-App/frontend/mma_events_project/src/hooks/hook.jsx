import { useState, useEffect } from "react";

export default function useFetchEvents() {
  const [eventsList, setEventsList] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetch("/api/events");
        const data = await result.json();

        const formatted = data.map((item) => ({
          title: item.event_name, 
          start: item.event_date,
        }));

        setEventsList(formatted);
      } catch (error) {
        console.error("Failed to fetch events:", error);
      }
    };
    fetchData();
  }, []);

  return eventsList;
}
