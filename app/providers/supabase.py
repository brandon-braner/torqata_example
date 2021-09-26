from supabase_py import create_client, Client

from app.config import settings


class SupabaseClient:
    def __init__(self):
        self.url = settings.supabase_url
        self.key = settings.supabase_key
        self.client: Client = create_client(self.url, self.key)
