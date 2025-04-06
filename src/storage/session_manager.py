import json
import uuid
from datetime import datetime
from pathlib import Path

class PracticeSession:
    def __init__(self, session_id, start_time, stop_time, midi_file_path):
        self.id = session_id
        self.start_time = start_time
        self.stop_time = stop_time
        self.duration = (stop_time - start_time).total_seconds()
        self.midi_file_path = midi_file_path

    def to_dict(self):
        """オブジェクトを辞書形式に変換"""
        return {
            "id": self.id,
            "start_time": self.start_time.isoformat(),
            "stop_time": self.stop_time.isoformat(),
            "duration": self.duration,
            "midi_file_path": self.midi_file_path,
        }

    @classmethod
    def from_dict(cls, data):
        """辞書形式からオブジェクトを生成"""
        return cls(
            session_id=data["id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            stop_time=datetime.fromisoformat(data["stop_time"]),
            midi_file_path=data["midi_file_path"],
        )

class PracticeSessionManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.sessions = self.load_sessions()

    def load_sessions(self):
        """JSONファイルからセッションを読み込む"""
        if not self.file_path.exists():
            return []
        with open(self.file_path, "r") as file:
            data = json.load(file)
            return [PracticeSession.from_dict(item) for item in data]

    def save_sessions(self):
        """セッションをJSONファイルに保存する"""
        with open(self.file_path, "w") as file:
            json.dump([session.to_dict() for session in self.sessions], file, indent=4)

    def add_session(self, start_time, stop_time, midi_file_path):
        """新しいセッションを追加する"""
        new_session = PracticeSession(
            session_id=str(uuid.uuid4()),  # GUIDを生成
            start_time=start_time,
            stop_time=stop_time,
            midi_file_path=midi_file_path,
        )
        self.sessions.append(new_session)
        self.save_sessions()