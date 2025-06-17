import requests

def execute_request(request):
    """Execute the HTTP request based on the parsed request object."""
    try:
        headers = {'User-Agent': 'PurlWebRequest/1.0'}
        if request['headers']:
            headers.update(request['headers'])
        
        method = request['method'].lower()
        kwargs = {
            'url': request['url'],
            'cookies': request['cookies'],
            'headers': headers
        }
        
        if method in ['post', 'put', 'patch']:
            if isinstance(request['payload'], dict):
                kwargs['json'] = request['payload']
            else:
                kwargs['data'] = request['payload']
        
        response = requests.request(method, **kwargs)
        
        result = {
            'status_code': response.status_code,
            'url': response.url,
            'headers': dict(response.headers),
            'content': response.text
        }
        
        try:
            result['json'] = response.json()
        except ValueError:
            result['json'] = None
            
        return result
    
    except requests.RequestException as e:
        return {'error': str(e)}
