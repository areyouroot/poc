import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ConfigModalComponent } from './components/config-modal/config-modal';
import { ApiService } from './services/api';
import { Company, IntelligenceData } from './models';

declare var google: any;

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, ConfigModalComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  latitude: number = 0;
  longitude: number = 0;
  radius: number = 5; // km
  selectedSectors: string[] = ['IT'];
  availableSectors: string[] = ['IT', 'Hospital', 'Finance', 'Education', 'Retail'];

  companies: (Company & { intelligence?: IntelligenceData; analyzing?: boolean })[] = [];

  map: any;
  markers: any[] = [];

  configSaved = false;
  isScanning = false;

  constructor(private apiService: ApiService) {}

  onConfigSaved() {
    this.configSaved = true;
    this.getLocation();
  }

  getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.latitude = position.coords.latitude;
          this.longitude = position.coords.longitude;
          this.loadMapScript();
        },
        (error) => {
          console.error("Error getting location", error);
          this.latitude = 37.7749; // SF default
          this.longitude = -122.4194;
          this.loadMapScript();
        }
      );
    } else {
      this.latitude = 37.7749;
      this.longitude = -122.4194;
      this.loadMapScript();
    }
  }

  loadMapScript() {
    this.apiService.getConfig().subscribe(config => {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${config.maps_api_key}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => {
        this.initMap();
      };
      document.head.appendChild(script);
    });
  }

  initMap() {
    const mapOptions = {
      center: { lat: this.latitude, lng: this.longitude },
      zoom: 12
    };
    this.map = new google.maps.Map(document.getElementById('map'), mapOptions);

    // User marker
    new google.maps.Marker({
      position: { lat: this.latitude, lng: this.longitude },
      map: this.map,
      title: "Your Location",
      icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
    });
  }

  scan() {
    this.isScanning = true;
    // clear old markers
    this.markers.forEach(m => m.setMap(null));
    this.markers = [];

    this.apiService.scan({
      latitude: this.latitude,
      longitude: this.longitude,
      radius_km: this.radius,
      sectors: this.selectedSectors
    }).subscribe({
      next: (companies) => {
        this.companies = companies;
        this.isScanning = false;
        this.plotCompanies();
        this.analyzeAll();
      },
      error: (err) => {
        this.isScanning = false;
        alert("Scan failed: " + err.message);
      }
    });
  }

  plotCompanies() {
    this.companies.forEach(company => {
      if (company.latitude && company.longitude) {
        const marker = new google.maps.Marker({
          position: { lat: company.latitude, lng: company.longitude },
          map: this.map,
          title: company.name
        });

        const infoWindow = new google.maps.InfoWindow({
            content: `<b>${company.name}</b><br>${company.address}`
        });

        marker.addListener("click", () => {
            infoWindow.open(this.map, marker);
        });

        this.markers.push(marker);
      }
    });
  }

  analyzeAll() {
    // Analyze each company one by one or in parallel?
    // Parallel might hit rate limits. Let's do parallel but with UI indication.
    this.companies.forEach(company => {
      this.analyzeCompany(company);
    });
  }

  analyzeCompany(company: any) {
    company.analyzing = true;
    // We assume the first sector is the primary one for search context, or join them?
    const sector = this.selectedSectors.join(" ");
    this.apiService.analyze(company, sector).subscribe({
      next: (data) => {
        company.intelligence = data;
        company.analyzing = false;
      },
      error: () => {
        company.analyzing = false;
      }
    });
  }

  toggleSector(sector: string, event: any) {
      if (event.target.checked) {
          if (!this.selectedSectors.includes(sector)) {
              this.selectedSectors.push(sector);
          }
      } else {
          const index = this.selectedSectors.indexOf(sector);
          if (index > -1) {
              this.selectedSectors.splice(index, 1);
          }
      }
  }
}
