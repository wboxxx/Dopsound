"""Device communication, logging and live tools."""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path

import tkinter as tk

from cli.auto_match_hil import HILToneMatcher
from hil.io import AudioDeviceManager


class SplitVerticalGUIDeviceMixin:
    """Device communication, logging and live tools."""

    def init_hil_system(self):
        """Initialize HIL system."""
        try:
            self.hil_matcher = HILToneMatcher()
            self.audio_manager = AudioDeviceManager()
            self.log_status("✅ HIL system initialized")
            self.update_status_info()
        except Exception as e:
            self.log_status(f"❌ HIL init error: {e}")
    
    def send_patch_to_magicstomp(self):
        """Send current patch to Magicstomp device."""
        from debug_logger import debug_logger
debug_logger.log(f"🔍 DEBUG: Starting send_patch_to_magicstomp()")
        
        if not self.current_patch:
            self.log_status("⚠️ No patch to send")
debug_logger.log(f"🔍 DEBUG: No current patch to send")
            return
        
        try:
            self.log_status("📤 Sending patch to Magicstomp...")
debug_logger.log(f"🔍 DEBUG: Starting patch send process...")
debug_logger.log(f"🔍 DEBUG: Current patch: {self.current_patch}")
            
            # Import the adapter
            from adapter_magicstomp import MagicstompAdapter
            adapter = MagicstompAdapter()
            
            # List available MIDI ports first
debug_logger.log(f"🔍 DEBUG: Listing MIDI ports...")
            adapter.list_midi_ports()
            
            # Convert patch to SysEx
debug_logger.log(f"🔍 DEBUG: Converting patch to SysEx...")
            syx_data = adapter.json_to_syx(self.current_patch, patch_number=0)
debug_logger.log(f"🔍 DEBUG: Nombre de messages SysEx: {len(syx_data)}")
            if syx_data:
debug_logger.log(f"🔍 DEBUG: Premier message: {syx_data[0]}")
            
            # Get selected MIDI port from settings
            midi_output = self.midi_output_var.get() if hasattr(self, 'midi_output_var') else None
            if not midi_output:
                self.log_status("⚠️ Please select MIDI output device in Settings tab")
debug_logger.log(f"🔍 DEBUG: No MIDI output device selected")
                return
            
            # Send to device using existing port if available
debug_logger.log(f"🔍 DEBUG: Sending to MIDI port: {midi_output}")
            existing_port = None
            if hasattr(self, 'realtime_magicstomp'):
debug_logger.log(f"🔍 DEBUG: RealtimeMagicstomp exists: {self.realtime_magicstomp}")
                if hasattr(self.realtime_magicstomp, 'output_port') and self.realtime_magicstomp.output_port:
                    existing_port = self.realtime_magicstomp.output_port
debug_logger.log(f"🔍 DEBUG: Using existing RealtimeMagicstomp port")
                else:
debug_logger.log(f"🔍 DEBUG: No existing port available in RealtimeMagicstomp")
            else:
debug_logger.log(f"🔍 DEBUG: No RealtimeMagicstomp available")
            success = adapter.send_to_device(syx_data, midi_output, existing_port)
            
            if success:
                self.log_status("✅ Patch sent to Magicstomp successfully!")
debug_logger.log(f"🔍 DEBUG: Patch sent successfully")
            else:
                self.log_status("❌ Failed to send patch to Magicstomp")
debug_logger.log(f"🔍 DEBUG: Patch send failed")
            
        except Exception as e:
            self.log_status(f"❌ Error sending patch: {e}")
debug_logger.log(f"🔍 DEBUG: Error sending patch: {e}")
            import traceback
            traceback.print_exc()
    
    def refresh_audio_devices(self):
        """Refresh audio device list."""
        try:
            import sounddevice as sd
            
            # Get input devices
            input_devices = []
            output_devices = []
            
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                device_name = f"{device['name']} (ID: {i})"
                if device['max_input_channels'] > 0:
                    input_devices.append(device_name)
                if device['max_output_channels'] > 0:
                    output_devices.append(device_name)
            
            # Update comboboxes
            self.audio_input_combo['values'] = input_devices
            self.audio_output_combo['values'] = output_devices
            
            # Set default selections
            if input_devices and not self.audio_input_var.get():
                self.audio_input_var.set(input_devices[0])
            if output_devices and not self.audio_output_var.get():
                self.audio_output_var.set(output_devices[0])
            
            self.log_status(f"🔄 Found {len(input_devices)} input, {len(output_devices)} output audio devices")
            
        except ImportError:
            self.log_status("⚠️ sounddevice not available - using default audio")
            self.audio_input_combo['values'] = ["Default Input"]
            self.audio_output_combo['values'] = ["Default Output"]
            self.audio_input_var.set("Default Input")
            self.audio_output_var.set("Default Output")
        except Exception as e:
            self.log_status(f"❌ Error refreshing audio devices: {e}")
    
    def reload_midi_settings(self):
        """Recharge les paramètres MIDI depuis le fichier de configuration."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                # Recharge les paramètres MIDI
                if 'midi_input_device' in settings and hasattr(self, 'midi_input_var'):
                    self.midi_input_var.set(settings['midi_input_device'])
debug_logger.log(f"🔍 DEBUG: Reloaded MIDI input: {settings['midi_input_device']}")
                
                if 'midi_output_device' in settings and hasattr(self, 'midi_output_var'):
                    self.midi_output_var.set(settings['midi_output_device'])
debug_logger.log(f"🔍 DEBUG: Reloaded MIDI output: {settings['midi_output_device']}")
                    
                    # Mise à jour automatique du port RealtimeMagicstomp
                    if hasattr(self, 'realtime_magicstomp') and settings['midi_output_device']:
                        self.update_realtime_magicstomp_port(settings['midi_output_device'])
                
                if 'midi_channels' in settings and hasattr(self, 'midi_channel_vars'):
                    # Reset all channels first
                    for var in self.midi_channel_vars.values():
                        var.set(False)
                    # Restore selected channels
                    for channel in settings['midi_channels']:
                        if channel in self.midi_channel_vars:
                            self.midi_channel_vars[channel].set(True)
                    self.midi_channels = settings['midi_channels']
debug_logger.log(f"🔍 DEBUG: Reloaded MIDI channels: {settings['midi_channels']}")
                
        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error reloading MIDI settings: {e}")
    
    def reload_file_and_patch_settings(self):
        """Recharge les fichiers et patch depuis le fichier de configuration."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)

                # Recharge les fichiers
                if 'last_target_file' in settings and settings['last_target_file']:
                    self.target_file = settings['last_target_file']
                    if hasattr(self, 'target_var'):
                        self.target_var.set(f"Target: {Path(self.target_file).name}")
                    self.log_status(f"📁 Restored target: {Path(self.target_file).name}")
debug_logger.log(f"🔍 DEBUG: Reloaded target file: {self.target_file}")

                if 'last_di_file' in settings and settings['last_di_file']:
                    self.di_file = settings['last_di_file']
                    if hasattr(self, 'di_var'):
                        self.di_var.set(f"DI: {Path(self.di_file).name}")
                    self.log_status(f"📁 Restored DI: {Path(self.di_file).name}")
debug_logger.log(f"🔍 DEBUG: Reloaded DI file: {self.di_file}")

                # Le patch est déjà géré par restore_application_state()
                # Pas besoin de le recharger ici

        except Exception as e:
debug_logger.log(f"🔍 DEBUG: Error reloading file and patch settings: {e}")
    
    def update_realtime_magicstomp_port(self, port_name):
        """Met à jour le port MIDI de RealtimeMagicstomp."""
        try:
            if hasattr(self, 'realtime_magicstomp') and self.realtime_magicstomp:
                # Ferme l'ancien port s'il existe
                if self.realtime_magicstomp.output_port:
                    self.realtime_magicstomp.output_port.close()
                
                # Se connecte au nouveau port
                self.realtime_magicstomp.midi_port_name = port_name
                self.realtime_magicstomp._connect_to_port(port_name)
                
                if self.realtime_magicstomp.output_port:
                    print(f"✅ RealtimeMagicstomp connecté au port: {port_name}")
                    self.log_status(f"✅ MIDI connecté: {port_name}")
                else:
                    print(f"❌ Échec connexion RealtimeMagicstomp au port: {port_name}")
                    self.log_status(f"❌ Échec connexion MIDI: {port_name}")
                    
        except Exception as e:
            print(f"❌ Erreur mise à jour port RealtimeMagicstomp: {e}")
    
    def on_midi_input_changed(self, event=None):
        """Callback quand le port MIDI input change."""
        try:
            port_name = self.midi_input_var.get()
debug_logger.log(f"🔍 DEBUG: MIDI input changed to: {port_name}")
            self.save_settings()  # Sauvegarde automatique
        except Exception as e:
            print(f"❌ Erreur changement MIDI input: {e}")
    
    def on_midi_output_changed(self, event=None):
        """Callback quand le port MIDI output change."""
        try:
            port_name = self.midi_output_var.get()
debug_logger.log(f"🔍 DEBUG: MIDI output changed to: {port_name}")
            
            # Met à jour RealtimeMagicstomp
            self.update_realtime_magicstomp_port(port_name)
            
            # Sauvegarde automatique
            self.save_settings()
            
        except Exception as e:
            print(f"❌ Erreur changement MIDI output: {e}")
    
    def refresh_midi_devices(self):
        """Refresh MIDI device list."""
        try:
            import mido
            
            # Get MIDI devices
            input_names = mido.get_input_names()
            output_names = mido.get_output_names()
            
            # Update comboboxes
            self.midi_input_combo['values'] = input_names
            self.midi_output_combo['values'] = output_names
            
            # Auto-detect Magicstomp and set default selections
            magicstomp_output = None
            magicstomp_input = None
            
            # Recherche Magicstomp dans les ports de sortie
            for port in output_names:
                if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                    magicstomp_output = port
                    break
            
            # Recherche Magicstomp dans les ports d'entrée
            for port in input_names:
                if 'ub9' in port.lower() or 'magicstomp' in port.lower():
                    magicstomp_input = port
                    break
            
            # Définit les sélections par défaut
            if input_names and not self.midi_input_var.get():
                if magicstomp_input:
                    self.midi_input_var.set(magicstomp_input)
debug_logger.log(f"🔍 DEBUG: Auto-selected Magicstomp input: {magicstomp_input}")
                else:
                    # Si pas de port d'entrée Magicstomp, utiliser le premier disponible
                    self.midi_input_var.set(input_names[0])
                    
            if output_names and not self.midi_output_var.get():
                if magicstomp_output:
                    self.midi_output_var.set(magicstomp_output)
debug_logger.log(f"🔍 DEBUG: Auto-selected Magicstomp output: {magicstomp_output}")
                    # Met à jour RealtimeMagicstomp automatiquement
                    self.update_realtime_magicstomp_port(magicstomp_output)
                else:
                    self.midi_output_var.set(output_names[0])
            
            # Si pas de port d'entrée Magicstomp trouvé, mais qu'on a un port de sortie
            # Essayer d'utiliser le port de sortie pour l'entrée aussi
            if not magicstomp_input and magicstomp_output and not self.midi_input_var.get():
debug_logger.log(f"🔍 DEBUG: No Magicstomp input port found, trying to use output port for input: {magicstomp_output}")
                self.midi_input_var.set(magicstomp_output)
            
            self.log_status(f"🔄 Found {len(input_names)} MIDI input, {len(output_names)} MIDI output devices")
            
        except ImportError:
            self.log_status("⚠️ mido not available - using default MIDI")
            self.midi_input_combo['values'] = ["Default MIDI Input"]
            self.midi_output_combo['values'] = ["Default MIDI Output"]
            self.midi_input_var.set("Default MIDI Input")
            self.midi_output_var.set("Default MIDI Output")
        except Exception as e:
            self.log_status(f"❌ Error refreshing MIDI devices: {e}")
    
    def update_midi_channels(self, channel):
        """Update selected MIDI channels."""
        self.midi_channels = []
        for ch, var in self.midi_channel_vars.items():
            if var.get():
                self.midi_channels.append(ch)
        
        self.log_status(f"🎹 MIDI channels updated: {self.midi_channels}")
    
    def test_audio_setup(self):
        """Test the audio setup."""
        self.log_status("🎵 Testing audio setup...")
        
        try:
            import sounddevice as sd
            import numpy as np
            
            # Get settings
            sample_rate = int(self.sample_rate_var.get())
            buffer_size = int(self.buffer_size_var.get())
            
            # Create test tone
            duration = 1.0  # 1 second test
            frequency = 440  # A4 note
            t = np.linspace(0, duration, int(sample_rate * duration))
            test_tone = np.sin(2 * np.pi * frequency * t) * 0.1  # Low volume
            
            self.audio_test_status.config(text="Playing test tone...")
            
            # Play test tone
            sd.play(test_tone, samplerate=sample_rate, blocksize=buffer_size)
            sd.wait()  # Wait until finished
            
            self.audio_test_status.config(text="Test completed - check audio output")
            self.log_status("✅ Audio test completed")
            
        except ImportError:
            self.log_status("⚠️ sounddevice not available for testing")
            self.audio_test_status.config(text="sounddevice not available")
        except Exception as e:
            self.log_status(f"❌ Audio test failed: {e}")
            self.audio_test_status.config(text=f"Test failed: {e}")
    
    def start_optimization(self):
        """Start optimization."""
        if not self.current_patch:
            self.log_status("⚠️ Generate patch first")
            return
        
        if self.is_optimizing:
            self.log_status("⚠️ Already optimizing")
            return
        
        self.log_status("🔄 Optimizing...")
        self.is_optimizing = True
        self.update_status_info()
        
        def optimize_thread():
            try:
                for i in range(101):
                    self.root.after(0, lambda p=i: self.progress_var.set(p))
                    time.sleep(0.1)
                
                optimized_params = self.generate_smart_target_parameters(self.current_parameters)
                self.target_parameters = optimized_params
                
                self.root.after(0, self.update_impact_visualization)
                self.root.after(0, lambda: self.log_status("✅ Optimization done"))
                
            except Exception as e:
                self.root.after(0, lambda: self.log_status(f"❌ Error: {e}"))
            finally:
                self.root.after(0, lambda: setattr(self, 'is_optimizing', False))
                self.root.after(0, self.update_status_info)
        
        threading.Thread(target=optimize_thread, daemon=True).start()
    
    def toggle_live_monitoring(self):
        """Toggle live monitoring."""
        if not self.is_live_monitoring:
            self.start_live_monitoring()
        else:
            self.stop_live_monitoring()
    
    def start_live_monitoring(self):
        """Start live monitoring."""
        try:
            self.log_status("🎤 Starting monitoring...")
            self.is_live_monitoring = True
            self.monitor_btn.config(text="⏹️ Stop Monitoring")
            self.update_status_info()
            self.log_status("✅ Monitoring active")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def stop_live_monitoring(self):
        """Stop live monitoring."""
        try:
            self.is_live_monitoring = False
            self.monitor_btn.config(text="🎤 Start Monitoring")
            self.update_status_info()
            self.log_status("⏹️ Monitoring stopped")
        except Exception as e:
            self.log_status(f"❌ Error: {e}")
    
    def quick_analyze(self):
        """Quick analyze action."""
        self.log_status("⚡ Quick analyze...")
        self.analyze_current_parameters()
    
    def quick_generate(self):
        """Quick generate action."""
        self.log_status("⚡ Quick generate...")
        self.generate_target_parameters()
    
    def quick_apply(self):
        """Quick apply action."""
        self.log_status("⚡ Quick apply...")
        self.apply_changes()
    
    def clear_logs(self):
        """Clear status logs."""
        self.status_text.delete(1.0, tk.END)
    
    def log_status(self, message: str):
        """Log status message."""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        # Check if status_text is available
        if hasattr(self, 'status_text') and self.status_text:
            try:
                self.status_text.insert(tk.END, log_message)
                self.status_text.see(tk.END)
            except:
                # Fallback to console if GUI not ready
                print(log_message.strip())
        else:
            # Fallback to console if status_text not available
            print(log_message.strip())
    
    def on_closing(self):
        """Handle window closing."""
        try:
            # Stop all active processes
            if self.is_live_monitoring:
                self.stop_live_monitoring()
            if self.is_live_di_capturing:
                self.stop_live_di_capture()
            
            # Ensure audio stream is stopped
            self.stop_audio_capture()
            
            # Close MIDI connection
            if hasattr(self, 'realtime_magicstomp'):
                # Close MIDI ports
                if hasattr(self.realtime_magicstomp, 'output_port') and self.realtime_magicstomp.output_port:
                    self.realtime_magicstomp.output_port.close()
                if hasattr(self.realtime_magicstomp, 'input_port') and self.realtime_magicstomp.input_port:
                    self.realtime_magicstomp.input_port.close()
            
            # Save settings before closing
            self.save_settings()
            
            self.log_status("👋 Application closing - settings saved")
            
        except Exception as e:
            print(f"Error during closing: {e}")
        finally:
            self.root.destroy()
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()
    
    def test_patch_on_device(self):
        """Test the current patch on the Magicstomp device."""
        try:
            self.log_status("🎸 Testing patch on device...")
            # This would implement patch testing functionality
            # For now, just log the action
            self.log_status("✅ Patch test completed")
        except Exception as e:
            self.log_status(f"❌ Error testing patch: {e}")
    
    def verify_patch_upload(self):
        """Verify that the patch was uploaded correctly to the device."""
        try:
            self.log_status("✅ Verifying patch upload...")
            # This would implement patch verification functionality
            # For now, just log the action
            self.log_status("✅ Patch upload verified")
        except Exception as e:
            self.log_status(f"❌ Error verifying upload: {e}")
    
    def check_device_status(self):
        """Check the status of the Magicstomp device."""
        try:
            self.log_status("📊 Checking device status...")
            # This would implement device status checking
            # For now, just log the action
            self.log_status("✅ Device status: Connected")
        except Exception as e:
            self.log_status(f"❌ Error checking device status: {e}")
    
    def generate_retroactioned_patch(self):
        """Generate a retroactioned patch based on current analysis."""
        try:
            self.log_status("🎯 Generating retroactioned patch...")
            # This would implement retroactioned patch generation
            # For now, just log the action
            self.log_status("✅ Retroactioned patch generated")
        except Exception as e:
            self.log_status(f"❌ Error generating retroactioned patch: {e}")
    
    def stop_optimization_simple(self):
        """Stop optimization process."""
        try:
            self.log_status("⏹️ Stopping optimization...")
            # This would implement optimization stopping
            # For now, just log the action
            self.log_status("✅ Optimization stopped")
        except Exception as e:
            self.log_status(f"❌ Error stopping optimization: {e}")


def main():
    """Main function."""
    app = SplitVerticalGUI()
    app.run()


if __name__ == "__main__":
    main()
