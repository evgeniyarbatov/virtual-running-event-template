import { useEffect, useState } from "react";

const App = () => {
  const [event, setEvent] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/event.json")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load event data");
        }
        return res.json();
      })
      .then((data) => setEvent(data))
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div className="app">
        <div className="container">
          <div className="panel">{error}</div>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="app">
        <div className="container">
          <div className="panel">Loading event data...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="hero">
        <div className="container">
          <div className="eyebrow">{event.country}</div>
          <h1>{event.title}</h1>
          <p className="subtitle">{event.subtitle}</p>
        </div>
      </header>
      <main className="content">
        <div className="container">
          <section className="panel">
            <h2>About the event</h2>
            {event.custom_texts.map((text, index) => (
              <p key={index}>{text}</p>
            ))}
          </section>
          <section className="panel points">
            <div>
              <h3>Start</h3>
              <p>{event.start_point}</p>
            </div>
            <div>
              <h3>Finish</h3>
              <p>{event.stop_point}</p>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
};

export default App;
