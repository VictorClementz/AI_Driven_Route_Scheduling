import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import L from 'leaflet';


const fixLeafletIcons = () => {
  delete L.Icon.Default.prototype._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
  });
};


const createIcon = (color) => {
  return L.divIcon({
    className: 'custom-div-icon',
    html: `<div style="background-color: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });
};

const MapComponent = ({ cleaner, jobs }) => {
  useEffect(() => {
    fixLeafletIcons();
  }, []);

  // Standardposition (Stockholm centrum)
  const defaultCenter = [59.3293, 18.0686];

  // Enkla koordinater för demo
  const getCoordinates = (address) => {
    const coordinates = {
      'Stockholm': [59.3293, 18.0686],
      'Göteborg': [57.7089, 11.9746],
      'Malmö': [55.6050, 13.0038],
      'Uppsala': [59.8586, 17.6389],
      'Huddinge': [59.2348, 17.9826]
    };

    // Hitta första matchande stad i adressen
    for (const [city, coords] of Object.entries(coordinates)) {
      if (address.toLowerCase().includes(city.toLowerCase())) {
        return coords;
      }
    }

    // Slumpmässiga koordinater runt Stockholm för demo
    return [
      59.3293 + (Math.random() - 0.5) * 0.2,
      18.0686 + (Math.random() - 0.5) * 0.3
    ];
  };

  const homeCoords = getCoordinates(cleaner.home_address);
  const jobCoords = jobs.map(job => ({
    ...job,
    coords: getCoordinates(job.address)
  }));

  // Skapa rutt mellan hem och jobb
  const routeCoords = [homeCoords, ...jobCoords.map(j => j.coords)];

  const homeIcon = createIcon('#10b981'); // Grön
  const jobIcon = createIcon('#ef4444');  // Röd

  return (
    <div style={{
      height: '320px',
      width: '100%',
      borderRadius: '12px',
      overflow: 'hidden',
      border: '1px solid #e2e8f0'
    }}>
      <MapContainer
        center={homeCoords}
        zoom={11}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Hem-markör */}
        <Marker position={homeCoords} icon={homeIcon}>
          <Popup>
            <div style={{ fontFamily: 'inherit' }}>
              <strong>{cleaner.name}s hem</strong><br />
              {cleaner.home_address}
            </div>
          </Popup>
        </Marker>

        {/* Jobb-markörer */}
        {jobCoords.map((job, index) => (
          <Marker key={job.id} position={job.coords} icon={jobIcon}>
            <Popup>
              <div style={{ fontFamily: 'inherit' }}>
                <strong>{job.client_name}</strong><br />
                {job.address}<br />
                <em>Tid: {job.scheduled_start_time} - {job.scheduled_end_time}</em>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Rutt */}
        {routeCoords.length > 1 && (
          <Polyline
            positions={routeCoords}
            color="#3b82f6"
            weight={3}
            opacity={0.7}
            dashArray="5, 10"
          />
        )}
      </MapContainer>
    </div>
  );
};

export default MapComponent;