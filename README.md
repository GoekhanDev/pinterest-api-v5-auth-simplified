# pinterest-api-v5-auth-simplified
A easier and faster way to get the access token for the Pinterest v5 API. 
The request uri is set to localhost.

## Requirements
 ```bash 
 pip install -r requirements.txt
```

## How to use
 
```python 
 pinterest().auth("client_id", "client_secret", "redirect_uri", "scope")
```

## Result

```json
 {
 "access_token": "{an access token string prefixed with 'pina'}",
 "refresh_token": "{a refresh token string prefixed with 'pinr'}",
 "response_type": "authorization_code",
 "token_type": "bearer",
 "expires_in": "access token expiry: int",
 "refresh_token_expires_in": "refresh token expiry: int",
 "scope": "scopes"
 }
```

<br/>
<br/>
<a href="https://www.buymeacoffee.com/GoekhanA" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 100px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
