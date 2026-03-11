import { useEffect, useState } from "react";

const Log = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch("/log.json")
      .then((res) => res.json())
      .then((data) => setLogs(data))
      .catch((err) => console.error("Failed to load log:", err));
  }, []);

  return (
    <div className="p-4">
      <h2>Log</h2>
      <br />
      <br />
      <style>
        {`
          table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
          }
          td {
            width: 33.33%;
            padding: 8px;
          }
        `}
      </style>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Distance</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((run, i) => (
            <tr key={i}>
              <td>{run.date}</td>
              <td>{run.distance}km</td>
              <td>
                <a href={run.link} target="_blank" rel="noopener noreferrer">
                  {run.link.includes("strava.com")
                    ? "Strava"
                    : run.link.includes("polar.com")
                      ? "Polar"
                      : "Link"}
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Log;
