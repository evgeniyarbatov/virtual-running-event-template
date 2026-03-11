import { useEffect, useState } from "react";

const Status = () => {
  const [todayDate, setTodayDate] = useState("");
  const [startDate, setStartDate] = useState("");
  const [startPoint, setStartPoint] = useState("");
  const [finishDate, setFinishDate] = useState("");
  const [finishPoint, setFinishPoint] = useState("");
  const [currentPoint, setCurrentPoint] = useState("");

  useEffect(() => {
    const toLocalDateString = (unixTimestamp) => {
      const date = new Date(unixTimestamp * 1000);
      return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    };

    setTodayDate(toLocalDateString(Date.now() / 1000));

    fetch("/metadata.json")
      .then((res) => res.json())
      .then((metadata) => {
        setCurrentPoint(metadata.current_point);
        setStartDate(toLocalDateString(metadata.start_time));
        setFinishDate(toLocalDateString(metadata.finish_time));
      })
      .catch((err) => console.error("Failed to load metadata:", err));

    fetch("/event.json")
      .then((res) => res.json())
      .then((data) => {
        setStartPoint(data.start_point);
        setFinishPoint(data.stop_point);
      })
      .catch((err) => console.error("Failed to load event:", err));
  }, []);

  return (
    <div className="p-4">
      <h2>Start</h2>
      {startDate}
      <p>{startPoint}</p>
      <br />
      <br />
      <br />
      <br />
      <h2>Today</h2>
      {todayDate}
      <p>{currentPoint}</p>
      <br />
      <br />
      <br />
      <br />
      <h2>Finish</h2>
      {finishDate}
      <p>{finishPoint}</p>
    </div>
  );
};

export default Status;
