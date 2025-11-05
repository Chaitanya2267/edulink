import os


def get_database_url() -> str:
    """Return SQLAlchemy-compatible DATABASE URL.

    Defaults to SQLite file `edulink.db` in project root. To use MySQL, set
    the `DATABASE_URL` env var, e.g.:

    mysql+pymysql://username:password@localhost:3306/edulink
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # Default to SQLite file in current directory
    return f"sqlite:///{os.path.abspath('edulink.db')}"


class Settings:
    SQLALCHEMY_DATABASE_URI: str = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH_MB", "16")) * 1024 * 1024


