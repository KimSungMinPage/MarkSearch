from app.constants import CREDENTIAL_PATH
class CredentialService:
    def save_key(self, key: str) -> bool:
        try:
            import win32crypt  # type: ignore
            CREDENTIAL_PATH.parent.mkdir(parents=True, exist_ok=True)
            blob = win32crypt.CryptProtectData(key.encode("utf-8"), "GmpCompanyCollector", None, None, None, 0)[1]
            CREDENTIAL_PATH.write_bytes(blob); return True
        except Exception:
            return False
    def load_key(self) -> str:
        try:
            import win32crypt  # type: ignore
            if not CREDENTIAL_PATH.exists(): return ""
            return win32crypt.CryptUnprotectData(CREDENTIAL_PATH.read_bytes(), None, None, None, 0)[1].decode("utf-8")
        except Exception:
            return ""
    def delete_key(self) -> None:
        if CREDENTIAL_PATH.exists(): CREDENTIAL_PATH.unlink()
