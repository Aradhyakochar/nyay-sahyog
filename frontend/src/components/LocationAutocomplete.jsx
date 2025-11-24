import React, { useEffect, useRef } from 'react'
import './LocationAutocomplete.css'

function LocationAutocomplete({ value, onChange, placeholder = "Enter location..." }) {
  const inputRef = useRef(null)
  const autocompleteRef = useRef(null)

  useEffect(() => {
    // Wait for Google Maps to load
    const initAutocomplete = () => {
      if (inputRef.current && window.google && window.google.maps && window.google.maps.places) {
        // Initialize Google Places Autocomplete
        autocompleteRef.current = new window.google.maps.places.Autocomplete(
          inputRef.current,
          {
            types: ['geocode', 'establishment'],
            componentRestrictions: { country: 'in' } // Restrict to India
          }
        )

        // Listen for place selection
        autocompleteRef.current.addListener('place_changed', () => {
          const place = autocompleteRef.current.getPlace()
          
          if (place.geometry && onChange) {
            // Extract address components
            let city = ''
            let state = ''
            let pincode = ''
            let fullAddress = place.formatted_address

            place.address_components.forEach(component => {
              const types = component.types
              if (types.includes('locality') || types.includes('administrative_area_level_2')) {
                city = component.long_name
              }
              if (types.includes('administrative_area_level_1')) {
                state = component.long_name
              }
              if (types.includes('postal_code')) {
                pincode = component.long_name
              }
            })

            // Call onChange with structured data
            onChange({
              address: fullAddress,
              city: city,
              state: state,
              pincode: pincode,
              lat: place.geometry.location.lat(),
              lng: place.geometry.location.lng()
            })
          }
        })
      }
    }

    // Check if Google Maps is already loaded
    if (window.google && window.google.maps && window.google.maps.places) {
      initAutocomplete()
    } else {
      // Wait for Google Maps to load
      const checkGoogle = setInterval(() => {
        if (window.google && window.google.maps && window.google.maps.places) {
          clearInterval(checkGoogle)
          initAutocomplete()
        }
      }, 100)

      // Cleanup interval after 10 seconds
      setTimeout(() => clearInterval(checkGoogle), 10000)
    }

    return () => {
      if (autocompleteRef.current) {
        window.google?.maps?.event?.clearInstanceListeners(autocompleteRef.current)
      }
    }
  }, [onChange])

  return (
    <input
      ref={inputRef}
      type="text"
      className="location-autocomplete"
      placeholder={placeholder}
      defaultValue={value}
    />
  )
}

export default LocationAutocomplete

