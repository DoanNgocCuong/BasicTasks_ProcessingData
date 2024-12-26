    def process_audio(self, audio_path: str, language: str = 'en') -> Optional[Dict]:
        if not os.path.exists(audio_path):
            self.logger.error(f"Audio file not found: {audio_path}")
            return None

        with open(audio_path, 'rb') as audio_file:
            try:
                response = requests.post(
                    self.config.TRANSCRIBE_API_URL,
                    files={'audio': audio_file},
                    data={
                        'secret_key': self.config.SECRET_KEY,
                        'language': language
                    }
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                self.logger.error(f"Error processing audio: {e}")
                return None
