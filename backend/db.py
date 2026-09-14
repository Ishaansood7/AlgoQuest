import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
from config import Config

logger = logging.getLogger("algoquest.db")

class Database:
    """MongoDB Atlas database connection manager."""
    _instance = None
    _client = None
    _db = None
    _is_connected = False
    _connection_error = None

    @classmethod
    def initialize(cls):
        """Initializes the MongoDB connection pool."""
        if cls._client is not None:
            return cls._db

        mongo_uri = Config.MONGO_URI
        if not mongo_uri:
            cls._is_connected = False
            cls._connection_error = "MONGO_URI not configured in .env"
            logger.warning("MongoDB URI not set. Running in offline/mock mode.")
            return None

        try:
            logger.info("Attempting to connect to MongoDB Atlas...")
            cls._client = MongoClient(
                mongo_uri,
                connectTimeoutMS=Config.MONGO_CONNECT_TIMEOUT_MS,
                serverSelectionTimeoutMS=Config.MONGO_SERVER_SELECTION_TIMEOUT_MS,
                appname="AlgoQuest-Backend"
            )
            
            # Fast ping check to verify connectivity
            cls._client.admin.command('ping')
            cls._db = cls._client[Config.DB_NAME]
            cls._is_connected = True
            cls._connection_error = None
            logger.info(f"Connected successfully to MongoDB Atlas database: {Config.DB_NAME}")
        except (ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError) as err:
            cls._is_connected = False
            cls._connection_error = str(err)
            logger.warning(f"MongoDB connection failed: {err}. Backend running without active database.")
        except Exception as err:
            cls._is_connected = False
            cls._connection_error = str(err)
            logger.error(f"Unexpected MongoDB initialization error: {err}")

        return cls._db

    @classmethod
    def get_db(cls):
        """Returns the active database instance."""
        if cls._db is None and cls._client is None:
            cls.initialize()
        return cls._db

    @classmethod
    def get_status(cls):
        """Returns the current database connection health."""
        if not cls._is_connected and cls._client is not None:
            # Retry quick ping in case network recovered
            try:
                cls._client.admin.command('ping')
                cls._is_connected = True
                cls._connection_error = None
            except Exception as err:
                cls._is_connected = False
                cls._connection_error = str(err)

        return {
            "configured": bool(Config.MONGO_URI),
            "connected": cls._is_connected,
            "database_name": Config.DB_NAME if cls._is_connected else None,
            "error": cls._connection_error if not cls._is_connected else None
        }

    @classmethod
    def close(cls):
        """Closes the MongoDB connection pool."""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            cls._is_connected = False
            logger.info("MongoDB connection closed.")


def get_db():
    return Database.get_db()
