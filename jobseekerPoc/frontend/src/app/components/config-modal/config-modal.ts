import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Config } from '../../models';

@Component({
  selector: 'app-config-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './config-modal.html',
  styleUrls: ['./config-modal.css']
})
export class ConfigModalComponent {
  @Output() configSaved = new EventEmitter<void>();

  config: Config = {
    maps_api_key: '',
    search_api_key: '',
    search_cx: '',
    llm_provider: 'ollama',
    llm_base_url: 'http://localhost:11434',
    llm_api_key: ''
  };

  isVisible = true;

  constructor(private apiService: ApiService) {}

  saveConfig() {
    this.apiService.setConfig(this.config).subscribe({
      next: () => {
        this.isVisible = false;
        this.configSaved.emit();
      },
      error: (err) => {
        alert('Failed to save config: ' + err.message);
      }
    });
  }
}
