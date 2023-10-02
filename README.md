# Chronicle API

An OIDC-protected resource server and API that makes up the back-end of Chronicle, as the data delivery and storage component of the content management system built for my persosnal site. Configured to store, sort, manage and deliver data and files related to projects and blog posts, store and send e-mail and authorize users through OpenID Connect and OAuth 2.0 token introspection using the Echo Social Network as an identity provider.


## Features

- Custom API testing interface to construct requests and visualize data
- Endpoints for project and blog CRUD operations with REST API architecture
- Models and serializers with content management logic built in
- E-mail authoring and storage through Twilio SendGrid and Django ORM
- Custom OAuth 2.0 authorization flow for OpenID Connect token verification and management

## Roadmap

- Add comments and other application interactivity for users
- Implement e-mail server

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- OAuth 2.0
- JavaScript
- CSS
- HTML

## License

[MIT](https://choosealicense.com/licenses/mit/)

