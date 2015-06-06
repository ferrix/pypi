PyPI Cloud for Elastic Beanstalk
================================

This package is a Pyramid application that runs PyPI Cloud on AWS Elastic
Beanstalk.

Features
--------

* Reads RDS configuration from the environment variables
* Redirect HTTP to HTTPS with `pyramid_hsts`
* Serve static files through Apache

Use
---

Prerequisites:

* Amazon Web Services account
* A SSL certificate uploaded to be used with Elastic Loadbalancer

Then execute::

    git clone https://github.com/codetry/pypicloud-beanstalk
    cd pypicloud-beanstalk
    pip install -r development.txt
    eb init -r REGION -p 'Python 2.7'
    eb create --database.engine postgres

Then enable SSL on the ELB. To do that from the command line
run `eb config` and replace HTTPS Port on loadbalancer with 443
also, set the SSLCertificateId to the ARN of the key. Here it is
in a oneliner spell. You may need to `brew install gnu-sed` on a
Mac. Here goes::

    EDITOR="sed -i -e '/HTTPSPort/ s/OFF/443/' -e '/LoadBalancerSSLPortProtocol: HTTPS/{n;s/null/arn:aws:iam::1234567890:server-certificates\/mycert/}'" eb config

When everything is really set up, the service should answer on both
HTTP and HTTPS ports the former redirecting to the latter with gusto.
The initial run will ask the admin to register an account.
