class Request:
    def __init__(self, request_id: str, data: dict, client_ip: str):
        self.request_id = request_id
        self.data = data
        self.client_ip = client_ip
        self.is_valid = True
        self.cache_hit = False
        self.response = None

    def __str__(self):
        return f"Request(ID={self.request_id}, IP={self.client_ip}, Valid={self.is_valid}, Cache={self.cache_hit})"

from abc import ABC, abstractmethod

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return request

class DataValidationHandler(Handler):
    def handle(self, request):
        print(f"DataValidationHandler: Validating request {request.request_id}")
        
        # Check if data exists
        if not request.data:
            request.is_valid = False
            request.response = {"error": "No data provided"}
            return request
            
        # Simple validation example - check for required fields
        if 'action' not in request.data:
            request.is_valid = False
            request.response = {"error": "Missing required field: action"}
            return request
            
        # Sanitize data (simple example)
        if 'username' in request.data:
            request.data['username'] = request.data['username'].strip()
            
        print(f"DataValidationHandler: Request {request.request_id} validated successfully")
        return super().handle(request)



class IPFilteringHandler(Handler):
    def __init__(self, blocked_ips=None):
        super().__init__()
        self.blocked_ips = blocked_ips or []
        
    def handle(self, request):
        print(f"IPFilteringHandler: Checking IP {request.client_ip} for request {request.request_id}")
        
        if request.client_ip in self.blocked_ips:
            request.is_valid = False
            request.response = {"error": f"IP {request.client_ip} is blocked"}
            return request
            
        print(f"IPFilteringHandler: IP {request.client_ip} is allowed")
        return super().handle(request)


class CachingHandler(Handler):
    def __init__(self):
        super().__init__()
        self.cache = {}
        
    def handle(self, request):
        print(f"CachingHandler: Checking cache for request {request.request_id}")
        
        cache_key = f"{request.client_ip}:{str(request.data)}"
        if cache_key in self.cache:
            request.cache_hit = True
            request.response = self.cache[cache_key]
            return request
            
        print(f"CachingHandler: No cache hit for request {request.request_id}")
        # Process through chain
        processed_request = super().handle(request)
        
        # Only cache if request is valid and wasn't from cache
        if processed_request.is_valid and not processed_request.cache_hit:
            self.cache[cache_key] = processed_request.response
            
        return processed_request


class FinalProcessingHandler(Handler):
    def handle(self, request):
        if not request.is_valid:
            print(f"FinalProcessingHandler: Request {request.request_id} failed earlier checks")
            return request
            
        if request.cache_hit:
            print(f"FinalProcessingHandler: Request {request.request_id} served from cache")
            return request
            
        print(f"FinalProcessingHandler: Processing request {request.request_id}")
        # Simulate processing
        request.response = {
            "status": "success",
            "request_id": request.request_id,
            "data": request.data,
            "message": "Request processed successfully"
        }
        return request


def setup_chain(blocked_ips=None):
    # Create handlers
    data_validator = DataValidationHandler()
    ip_filter = IPFilteringHandler(blocked_ips)
    cache_handler = CachingHandler()
    final_handler = FinalProcessingHandler()
    
    # Set up the chain
    data_validator.set_next(ip_filter).set_next(cache_handler).set_next(final_handler)
    
    return data_validator


def test_system():
    # Set up chain with some blocked IPs
    blocked_ips = ["10.0.0.1", "192.168.1.100"]
    chain = setup_chain(blocked_ips)
    
    print("\n=== TEST 1: Valid Request ===")
    valid_request = Request(
        request_id="req_123",
        data={"action": "get_data", "username": "  user1  "},
        client_ip="172.16.0.1"
    )
    result = chain.handle(valid_request)
    print(f"Result: {result.response}")
    
    print("\n=== TEST 2: Blocked IP ===")
    blocked_ip_request = Request(
        request_id="req_456",
        data={"action": "get_data", "username": "user2"},
        client_ip="10.0.0.1"
    )
    result = chain.handle(blocked_ip_request)
    print(f"Result: {result.response}")
    
    print("\n=== TEST 3: Cached Request ===")
    # This is the same as the first valid request
    cached_request = Request(
        request_id="req_789",
        data={"action": "get_data", "username": "user1"},  # username is trimmed now
        client_ip="172.16.0.1"
    )
    result = chain.handle(cached_request)
    print(f"Result: {result.response}")
    print(f"Was this served from cache? {result.cache_hit}")

if __name__ == "__main__":
    test_system()
