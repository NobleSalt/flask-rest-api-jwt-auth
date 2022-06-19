# A REST-API using flask, jwt and mongodb

# Api Endpoints
## auth
  - */auth/signup*
    - requirements
        ``` js
        let method = 'POST'
        let params = {first_name, last_name, email, password}
        ```
  - */auth/login*
    - requirements
        ``` js
        let method = 'POST'
        let params = {email, password}
        ```
  - */auth/refresh-token*
    - requirements
        ``` js
        let method = 'POST' || 'GET'
        let params = {email, password}
        let headers = {
            'context-type': 'application/json',
            Authorization : 'Bearer token'
        }
        ```
## user
  - */users*
    - requirements
        ``` js
        let method = 'GET'
        let headers = {
            'context-type': 'application/json',
            Authorization : 'Bearer token'
        }
        ```
## template
  - */template*
    - requirements
        ``` js
        let method = 'POST'
        let params = {
            template_name,
            subject,
            body
            }
        ```
  - */template*
    - requirements
        ``` js
        let method = 'GET'
        ```
  - */template/:id*
    - requirements
        ``` js
        let method = 'GET'
        ```
  - */template/:id*
    - requirements
        ``` js
        let method = 'PUT'
        ```
  - */template/:id*
    - requirements
        ``` js
        let method = 'DELETE'
        ```
