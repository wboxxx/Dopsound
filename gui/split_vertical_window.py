#!/usr/bin/env python3
"""
Split Vertical GUI Window with Impact Visualization
==================================================

Version avec split vertical permanent :
- 80% gauche : Interface principale avec onglets
- 20% droite : Status/Logs toujours visible
"""

import tkinter as tk
from typing import Dict, List
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from realtime_magicstomp import RealtimeMagicstomp
from magicstomp_parameter_map import EFFECT_PARAMETERS

from adapter_magicstomp import MagicstompAdapter
from gui.split_vertical_setup import SplitVerticalGUISetupMixin
from gui.split_vertical_analysis import SplitVerticalGUIAnalysisMixin
from gui.split_vertical_effects import SplitVerticalGUIEffectsMixin
from gui.split_vertical_devices import SplitVerticalGUIDeviceMixin
from gui.split_vertical_shared import EffectMatch


class SplitVerticalGUI(
    SplitVerticalGUIDeviceMixin,
    SplitVerticalGUIEffectsMixin,
    SplitVerticalGUIAnalysisMixin,
    SplitVerticalGUISetupMixin,
):
    """
    GUI avec split vertical permanent.
    
    Layout:
    - 80% gauche : Interface principale avec onglets
    - 20% droite : Status/Logs toujours visible
    """
    
    def __init__(self):
        """Initialize the split vertical GUI."""
        # Load effect metadata before the GUI starts so heuristics use official names
        self.official_effect_names = set()
        self.official_effect_lookup: Dict[str, str] = {}
        self.supported_effect_name_to_type: Dict[str, int] = {}
        self.supported_effect_normalized_to_name: Dict[str, str] = {}
        self.supported_effect_normalized_to_type: Dict[str, int] = {}
        self.canonical_to_official_name: Dict[str, str] = {}
        self.effect_metadata_loaded = False

        # Load Magicstomp catalog to align analysis suggestions with official effects
        self.load_official_effect_catalog()

        # GUI root configuration
        self.root = tk.Tk()
        self.root.title("🎸 Magicstomp HIL - Split Vertical")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')

        # Minimum size
        self.root.minsize(1200, 700)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # State variables
        self.target_file = None
        self.di_file = None
        self.current_patch = None
        self.is_live_monitoring = False
        self.is_live_di_capturing = False
        self.audio_stream = None
        self.live_di_stream = None
        self.analysis_data = {}

        # Effect cascade management
        self.effect_widget_cascade = []
        self.last_identified_effects: Dict[str, List[EffectMatch]] = {}

        # Audio/MIDI settings
        self.audio_input_device = None
        self.audio_output_device = None
        self.midi_input_device = None
        self.midi_output_device = None
        self.sample_rate = 44100
        self.buffer_size = 1024
        self.audio_channels = 2
        self.midi_channels = [1]  # Default to channel 1

        # HIL system
        self.hil_matcher = None
        self.audio_manager = None
        self.is_optimizing = False

        # Enhanced components
        self.magicstomp_adapter = MagicstompAdapter()
        self.current_effect_widget = None
        self.current_effect_type = None
        self.impact_visualizer = None

        # MIDI/Sysex communication
        self.realtime_magicstomp = RealtimeMagicstomp()

        # Create reverse mapping: parameter name -> offset
        self.parameter_to_offset = {v: k for k, v in EFFECT_PARAMETERS.items()}

        # Parameter state
        self.original_parameters = {}
        self.target_parameters = {}
        self.current_parameters = {}

        # Settings file path
        self.settings_file = Path("magicstomp_gui_settings.json")

        # Initialize
        self.setup_styles()
        self.load_settings()
        self.create_widgets()
        self.init_hil_system()
        self.init_midi_connection()
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing."""
        if self.audio_stream:
            self.audio_stream.stop()
        if self.live_di_stream:
            self.live_di_stream.stop()
        self.root.destroy()


def main():
    """Main function."""
    app = SplitVerticalGUI()
    app.run()


if __name__ == "__main__":
    main()
