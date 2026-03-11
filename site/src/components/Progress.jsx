import { useEffect, useState } from "react";

const Progress = () => {
  const [currentDistance, setCurrentDistance] = useState(null);
  const [totalDistance, setTotalDistance] = useState(null);

  useEffect(() => {
    fetch("/metadata.json")
      .then((res) => res.json())
      .then((metadata) => {
        setCurrentDistance(metadata.current_distance);
        setTotalDistance(metadata.total_distance);
      })
      .catch((err) => console.error("Failed to load metadata:", err));
  }, []);

  const formatNumber = (num) => new Intl.NumberFormat("en-US").format(num);
  const percentage =
    currentDistance !== null && totalDistance !== null
      ? ((currentDistance / totalDistance) * 100).toFixed(1)
      : null;

  return (
    <div className="p-4">
      <div className="display-1 fw-bold">{formatNumber(currentDistance)}km</div>
      <div className="h2 fw-light text-muted">
        / {formatNumber(totalDistance)}km
      </div>
      <div className="small text-secondary mt-3">
        This journey is {percentage}% complete
      </div>
    </div>
  );
};

export default Progress;
