from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import logging
from datetime import datetime
import os
from pathlib import Path

class BaseIntegration(ABC):
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logger()
        # Get project root directory
        self.project_root = Path(__file__).parent.parent
        self.artifacts_base = self.project_root / "artifacts"
        self.data_cache = self.project_root / "data" / "cache"
        os.makedirs(self.data_cache, exist_ok=True)
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        log_dir = self.project_root / "logs"
        os.makedirs(log_dir, exist_ok=True)
        handler = logging.FileHandler(log_dir / f"{self.__class__.__name__}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    @abstractmethod
    def authenticate(self) -> bool:
        pass
    
    @abstractmethod
    def fetch_data(self, customer_id: str, **kwargs) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    def cache_data(self, customer_id: str, data: Dict[str, Any]):
        # Save to both cache and artifacts
        timestamp = datetime.now()
        
        # Cache for quick access
        cache_file = self.data_cache / f"{customer_id}_{self.__class__.__name__}.json"
        data['cached_at'] = timestamp.isoformat()
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Archive in artifacts
        content_type = self.__class__.__name__.replace('Integration', '').lower()
        customer_dir = self.artifacts_base / customer_id / content_type
        customer_dir.mkdir(parents=True, exist_ok=True)
        
        archive_file = customer_dir / f"{content_type}_data_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        with open(archive_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_cached_data(self, customer_id: str) -> Optional[Dict[str, Any]]:
        cache_file = self.data_cache / f"{customer_id}_{self.__class__.__name__}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def sync_customer_data(self, customer_id: str, force_refresh: bool = False, **kwargs) -> Dict[str, Any]:
        if not force_refresh:
            cached = self.get_cached_data(customer_id)
            if cached:
                cache_time = datetime.fromisoformat(cached['cached_at'])
                if (datetime.now() - cache_time).seconds < 3600:
                    self.logger.info(f"Using cached data for {customer_id}")
                    return cached
        
        self.logger.info(f"Fetching fresh data for {customer_id}")
        if not self.authenticate():
            raise Exception("Authentication failed")
        
        raw_data = self.fetch_data(customer_id, **kwargs)
        processed_data = self.process_data(raw_data)
        self.cache_data(customer_id, processed_data)
        
        return processed_data