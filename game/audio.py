import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.load_sounds()

    def load_sounds(self):
        """Load sound effects"""
        try:
            # Create simple sounds using basic wave forms
            self.sounds['attack'] = self.create_simple_sound(frequency=440, duration=100)  # A4 note
            self.sounds['heal'] = self.create_simple_sound(frequency=880, duration=100)    # A5 note
        except Exception as e:
            print(f"Warning: Could not create sounds: {e}")
            self.create_dummy_sounds()

    def create_simple_sound(self, frequency=440, duration=100):
        """Create a simple beep sound"""
        samples_per_second = 44100
        num_samples = int(duration * samples_per_second / 1000.0)
        sound_buffer = bytearray()

        for i in range(num_samples):
            # Simple square wave
            sample = 127 if i % (samples_per_second // frequency) < (samples_per_second // frequency // 2) else -127
            sound_buffer.append(abs(sample))

        try:
            return pygame.mixer.Sound(bytes(sound_buffer))
        except:
            return self.create_dummy_sound()

    def create_dummy_sounds(self):
        """Create silent sounds as fallback"""
        empty_buffer = bytearray([127] * 1000)  # Small silent buffer
        dummy_sound = pygame.mixer.Sound(bytes(empty_buffer))
        self.sounds['attack'] = dummy_sound
        self.sounds['heal'] = dummy_sound

    def create_dummy_sound(self):
        """Create a single silent sound as fallback"""
        empty_buffer = bytearray([127] * 1000)  # Small silent buffer
        return pygame.mixer.Sound(bytes(empty_buffer))

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                print(f"Warning: Could not play sound: {sound_name}")

    def play_music(self):
        """Background music is disabled for now to ensure stability"""
        self.music_playing = True

    def stop_music(self):
        """Stop background music"""
        self.music_playing = False