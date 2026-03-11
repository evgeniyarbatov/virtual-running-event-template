import { useEffect, useState } from "react";

const Intro = () => {
  const [event, setEvent] = useState(null);

  useEffect(() => {
    fetch("/event.json")
      .then((res) => res.json())
      .then((data) => setEvent(data))
      .catch((err) => console.error("Failed to load event:", err));
  }, []);

  if (!event) {
    return null;
  }

  return (
    <div className="text-justify px-3">
      <h1>{event.title}</h1>
      <h4>{event.subtitle}</h4>
      <br />
      <br />
      <p className="text-center mb-4">{event.country}</p>
      {event.custom_texts.map((text, index) => (
        <p className="mb-4" key={index}>
          {text}
        </p>
      ))}
    </div>
  );
};

export default Intro;
