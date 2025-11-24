import React, { useEffect, useRef } from 'react'
import './ProviderMap.css'

function ProviderMap({ providers, center = { lat: 28.6139, lng: 77.2090 }, zoom = 10 }) {
  const mapRef = useRef(null)
  const mapInstanceRef = useRef(null)
  const markersRef = useRef([])

  useEffect(() => {
    if (mapRef.current && window.google && providers.length > 0) {
      // Initialize map
      if (!mapInstanceRef.current) {
        mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
          center: center,
          zoom: zoom,
          mapTypeControl: true,
          streetViewControl: true,
          fullscreenControl: true
        })
      }

      // Clear existing markers
      markersRef.current.forEach(marker => marker.setMap(null))
      markersRef.current = []

      // Create markers for each provider
      const bounds = new window.google.maps.LatLngBounds()

      providers.forEach(provider => {
        if (provider.user?.city && provider.user?.state) {
          // Geocode address to get coordinates
          const geocoder = new window.google.maps.Geocoder()
          const address = `${provider.user.city}, ${provider.user.state}, India`

          geocoder.geocode({ address: address }, (results, status) => {
            if (status === 'OK' && results[0]) {
              const location = results[0].geometry.location
              
              // Create marker
              const marker = new window.google.maps.Marker({
                position: location,
                map: mapInstanceRef.current,
                title: provider.user.full_name,
                icon: {
                  url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
                }
              })

              // Create info window
              const infoWindow = new window.google.maps.InfoWindow({
                content: `
                  <div class="map-info-window">
                    <h3>${provider.user.full_name}</h3>
                    <p><strong>Role:</strong> ${provider.user.role}</p>
                    ${provider.specialization ? `<p><strong>Specialization:</strong> ${provider.specialization}</p>` : ''}
                    <p><strong>Rating:</strong> ⭐ ${provider.rating.toFixed(1)}</p>
                    <p><strong>Fee:</strong> ₹${provider.consultation_fee}</p>
                    <p><strong>Location:</strong> ${provider.user.city}, ${provider.user.state}</p>
                  </div>
                `
              })

              marker.addListener('click', () => {
                infoWindow.open(mapInstanceRef.current, marker)
              })

              markersRef.current.push(marker)
              bounds.extend(location)

              // Fit map to show all markers
              if (markersRef.current.length === providers.length) {
                mapInstanceRef.current.fitBounds(bounds)
              }
            }
          })
        }
      })
    }
  }, [providers, center, zoom])

  if (!providers || providers.length === 0) {
    return (
      <div className="map-container">
        <div className="map-placeholder">No providers to display on map</div>
      </div>
    )
  }

  return (
    <div className="map-container">
      <div ref={mapRef} className="map" />
    </div>
  )
}

export default ProviderMap

