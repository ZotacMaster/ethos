class Format:
    @staticmethod
    def seconds_to_min_sec(seconds: int) -> str:
        """
        Convert seconds to a string in the format min:sec.

        Args:
        - seconds (int): The duration in seconds.

        Returns:
        - str: The duration in min:sec format.
        """
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02}"


    def resolve_playlists(playlist_path: str) -> list:
        """
        Function to check if any playlist exists.
        
        Args:
        - playlist_path (str): Path to playlist directory
        
        Returns:
        - list: List of playlist files
        """
        import os
        return os.listdir(playlist_path)

    
    def is_recents(recent_file_path: str) -> bool:
        """
        Function to check if any recent file exists.
        
        Args:
        - recent_file_path (str): Path to recents file
        
        Returns:
        - bool: True if file exists, False otherwise
        """
        import os
        return os.path.exists(recent_file_path)

    
    def resolve_recents(recents_path: str) -> list:
        """
        Function to resolve last 5 played songs.
        
        Args:
        - recents_path (str): Path to recents JSON file
        
        Returns:
        - list: List of recent songs
        """
        import json
        if Format.is_recents(recents_path):
            with open(recents_path) as f:
                return json.loads(f.read())
        return []
    
    
    def fetch_tracks_from_playlist(playlist_path: str) -> list:
        """
        Function to fetch all songs from a playlist.json file.

        Args:
        - playlist_path (str): Path to a playlist

        Returns:
        - list: List of all songs in a particular playlist
        """
        import os
        import json
        if os.path.exists(playlist_path):
            with open(playlist_path) as f:
                return json.loads(f.read())
        return []