PyPI Cloud for Elastic Beanstalk
===

This package is a Pyramid application that runs PyPI Cloud on AWS Elastic
Beanstalk.

Features
---

* Reads RDS configuration from the environment variables
* Redirect HTTP to HTTPS with `pyramid_hsts`
* Serve static files through Apache
