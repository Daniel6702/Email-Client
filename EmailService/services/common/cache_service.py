import threading
from queue import Queue

class EmailCacheManager:
    def __init__(self):
        self.email_cache = {}
        self.cache_lock = threading.Lock()
        self.cache_update_queue = Queue()

    def get_cached_emails(self, folder_name, page_number):
        with self.cache_lock:
            return self.email_cache.get((folder_name, page_number))

    def set_cached_emails(self, folder_name, page_number, emails):
        with self.cache_lock:
            self.email_cache[(folder_name, page_number)] = emails

    def clear_cache(self):
        with self.cache_lock:
            self.email_cache.clear()

    def delete_cache_for_folder(self, folder_name):
        with self.cache_lock:
            keys_to_remove = [key for key in self.email_cache.keys() if key[0] == folder_name]
            for key in keys_to_remove:
                del self.email_cache[key]

    def update_cache_for_folder_move(self, from_folder_name, to_folder_name, email_id):
        with self.cache_lock:
            from_folder_keys = [key for key in self.email_cache.keys() if key[0] == from_folder_name]
            for key in from_folder_keys:
                self.email_cache[key] = [email for email in self.email_cache[key] if email.id != email_id]

            to_folder_key = (to_folder_name, 1)
            if to_folder_key in self.email_cache:
                email = next((email for email in self.email_cache[from_folder_keys[0]] if email.id == email_id), None)
                if email:
                    self.email_cache[to_folder_key].insert(0, email)

    def enqueue_for_cache_update(self, folder, query, max_results, page_number):
        self.cache_update_queue.put((folder, query, max_results, page_number))

    def get_next_cache_update_task(self):
        return self.cache_update_queue.get()

