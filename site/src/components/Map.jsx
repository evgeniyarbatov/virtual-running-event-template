import polyline from "@mapbox/polyline";

import L from "leaflet";
import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polyline,
  Marker,
  Popup,
} from "react-leaflet";

const makePinIcon = ({ fill, stroke }) =>
  L.divIcon({
    className: "custom-pin-icon",
    html: `
      <svg width="32" height="44" viewBox="0 0 32 44" xmlns="http://www.w3.org/2000/svg">
        <path d="M16 1C8.3 1 2 7.3 2 15c0 10.7 14 28 14 28s14-17.3 14-28C30 7.3 23.7 1 16 1z" fill="${fill}" stroke="${stroke}" stroke-width="1.6"/>
        <circle cx="16" cy="15" r="5.5" fill="#ffffff" stroke="${stroke}" stroke-width="1.2"/>
      </svg>
    `,
    iconSize: [32, 44],
    iconAnchor: [16, 43],
    popupAnchor: [0, -38],
  });

const startIcon = makePinIcon({ fill: "#1b7a5e", stroke: "#0f3f31" });
const currentIcon = makePinIcon({ fill: "#d21f3c", stroke: "#5b0f1d" });
const endIcon = makePinIcon({ fill: "#2a4b8d", stroke: "#131f38" });

const Map = () => {
  const [currentLocation, setCurrentLocation] = useState([]);
  const [polylineCoords, setPolylineCoords] = useState([]);
  const [startLabel, setStartLabel] = useState("");
  const [stopLabel, setStopLabel] = useState("");

  useEffect(() => {
    fetch("/map.json")
      .then((res) => res.json())
      .then((data) => {
        const decodedCoords = polyline.decode(data.polyline);
        setPolylineCoords(decodedCoords);
        setCurrentLocation(data.current_location);
      })
      .catch((err) => console.error("Failed to load polyline data:", err));
  }, []);

  useEffect(() => {
    fetch("/event.json")
      .then((res) => res.json())
      .then((data) => {
        setStartLabel(data.start_point);
        setStopLabel(data.stop_point);
      })
      .catch((err) => console.error("Failed to load event:", err));
  }, []);

  if (!currentLocation.length || !polylineCoords.length) {
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ height: "100vh" }}
      >
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Map Loading</span>
        </div>
      </div>
    );
  }

  return (
    <MapContainer
      center={currentLocation}
      zoom={10}
      scrollWheelZoom={false}
      style={{ height: "100vh", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <Polyline positions={polylineCoords} color="black" weight="4" />

      <Marker position={polylineCoords[0]} icon={startIcon}>
        <Popup>{startLabel}</Popup>
      </Marker>

      <Marker position={currentLocation} icon={currentIcon}>
        <Popup>Current Location</Popup>
      </Marker>

      <Marker
        position={polylineCoords[polylineCoords.length - 1]}
        icon={endIcon}
      >
        <Popup>{stopLabel}</Popup>
      </Marker>
    </MapContainer>
  );
};

export default Map;
