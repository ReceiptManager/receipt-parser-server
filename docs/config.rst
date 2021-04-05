Server configuration
========================

Following keys need to be defined.

+---------------+-------------------------------------------------+-------------------------------------+
| Config key    | Default value                                   | Description                         |
+---------------+-------------------------------------------------+-------------------------------------+
| language      | de                                              | Define the tesseract language       |
+---------------+-------------------------------------------------+-------------------------------------+
| https         | true                                            | Enable HTTPS                        |
+---------------+-------------------------------------------------+-------------------------------------+
| zeroconf      | false                                           | Enable zeroconf service             |
+---------------+-------------------------------------------------+-------------------------------------+
| receipts_path | "data/txt"                                      | Path where receipts are stored      |
+---------------+-------------------------------------------------+-------------------------------------+
| markets       | markets:                                        | Markets name                        |
|               |   store name:                                   |                                     |
|               |      - likely name 1                            |                                     |
|               |      - likely name 2                            |                                     |
+---------------+-------------------------------------------------+-------------------------------------+
| sum_keys      | - summe                                         | Keys to identify sum                |
|               | - gesamtbetrag                                  |                                     |
|               | - gesamt                                        |                                     |
|               | - total                                         |                                     |
|               | - sum                                           |                                     |
|               | - zwischensumme                                 |                                     |
|               | - bar                                           |                                     |
|               | - te betalen                                    |                                     |
+---------------+-------------------------------------------------+-------------------------------------+
| ignore_keys   | - rockgeld                                      | Keys                                |
|               | - rusckgeld                                     |                                     |
|               | - rückgeld                                      |                                     |
|               | - mwst                                          |                                     |
+---------------+-------------------------------------------------+-------------------------------------+
| sum_format    | \d+(\.\s?                                       | Regex to identify the receipt total |
|               | |,\s?|[^a-zA-Z\d])\d{2}                         |                                     |
+---------------+-------------------------------------------------+-------------------------------------+
| item_format   | ([a-zA-Z].+)\s(-|)(\d,\d\d)\s                   | Regex to identify the receipt items |
+---------------+-------------------------------------------------+-------------------------------------+
| date_format   | ((\d{2}\.\d{2}\.\d{2,4})                        | Regex to identify the receipt date  |
|               | |(\d{2,4}\/\d{2}\/\d{2})|(\d{2}\/\d{2}\/\d{4})) |                                     |
+---------------+-------------------------------------------------+-------------------------------------+

Add new market names
"""""""""""""""""""""
You can add new market entry below the ``markets`` key e.g.

.. code-block:: bash

     Store name:
             - likely name 1
             - likely name 2

Note: that the store name is returned and the likely names are used to scan the receipt
for these names. You can consider the receipt parser output in ``data/txt``

In this example, the tesseract output looks like:

.. code-block:: text

    EWE Rene Müller 0HGCITY
    org-Friedrich-Str.9

    }
    —
    L
    L
    E
    /
    D “il s

    L „é„ 31 Karlsruhe
    | | 50 /
    R 0/Z1 / 664 87 954
    LL UID Nr. : DE326445229
    B ) EUR
    —— MIO MIO MATE —
    | | )
    _„*}„%_ PF£N3t% ?5 1108 4
    | 6 Sal ‚19 .EUR X
    f““j“i$“ 2 5Stk x \ 0,15 V
    E E O
    _; Ge R "*M—w—‘—-»»——————*_„::_;:::..:‘::.;:_:‚;r::::.::ä..b-ö-«"
    ; ‚ Rückgeld BAR EHE 0, 32
    %———%———i S£Buer % Netto: steuer B[9£15
    | HAL En 2,25 0,43 . 268
    / ““‘};l@samtbetrag 2,25 0,43 a Z
    f ı TSE-Signatur: M631mP54IvkcwnNk+H7th3&meTdLüö[w
    8 0bo5B71skamunHSsZC1Z4q9ds6BRoDNWg
    Sa aUfagzEbyt TDVULU2ecc4rUk5/3211shY

The output looks horrible but you might noticed that the store name
is Rewe but the output is: ``EWE Rene Müller 0HGCITY``. Now, add the following market
in the ``config.yml``.

.. code-block:: text

    REWE:
     - ewe

To identify the market name Rewe but be carefully for duplicate store names. If the store name
Rewe exist please only add the likely name ``ewe``.

For docker users
========================


Forward config
""""""""""""""""
If you use the Docker image, you can forward the configuration file ``config.yml``.
If the ``config.yml`` is in your current directory you can add the following flag

.. code-block:: text

    -v "$(pwd):/config" -e RECEIPT_PARSER_CONFIG_DIR="/config"

If the config file is not in your current working directory. Replace ``$(pwd)`` with
you the configuration folder.


Forward IP
""""""""""""""""
Additionally, you can forward the Docker IP using:

.. code-block:: text

    -p $IP:8721:8721

Example config
===============

.. code-block:: text

        # Define the tesseract language
    language: deu

    # Enable https
    https: true

    # Enable zeroconf
    zeroconf: false

    # Where the receipts are stored
    # Receipts should be simple text files
    receipts_path: "data/txt"

    # Market names roughly ordered by likelihood.
    # Can contain market locations for fuzzy parsing
    markets:
      Colruyt:
         - colruyt
         - Colruyt
      Delhaize:
         - Delhaize
         - delhaize
      Penny:
         - penny
         - p e n n y
         - m a r k t gmbh
      REWE:
         - rewe
      Real:
         - real
      Netto:
         - netto-online
      Kaiser's:
         - kaiser
         - kaiserswerther straße 270
      Aldi:
         - aldi
         - friedrichstr 128—133
      Lidl:
         - lidl
      Edeka:
        - edeka
      Drogerie:
         - drogerie
      Kodi:
         - kodi
      Getraenke:
        - Getraenke Tempel
      Tanken:
         - text
         - esso station
         - aral
         - total tankstelle
         - RK Tankstellen
      Migros:
         - genossenschaft migros

    sum_keys:
      - summe
        - gesamtbetrag
        - gesantbetrag
        - gesamt
        - total
        - sum
        - zwischensumme
        - bar
        - te betalen
        - rockgeld
        - rusckgeld
        - rückgeld

        ignore_keys:
          - mwst
          - kg x
          - stkx
          - stk


    sum_format: '\d+(\.\s?|,\s?|[^a-zA-Z\d])\d{2}'

    item_format: '([a-zA-Z].+)\s(-|)(\d,\d\d)\s'

    date_format: '((\d{2}\.\d{2}\.\d{2,4})|(\d{2,4}\/\d{2}\/\d{2})|(\d{2}\/\d{2}\/\d{4}))'

Reverse proxy
=================

To use a reverse proxy, you need to disable `HTTPS` in the receipt parser config.
Change this line

.. code-block:: text

     # Enable https
     https: true

to

.. code-block:: text

     # Disable https
     https: false

After, use this example NGINX configuration and replace `DOMAIN` with your domain and `CERT PATH`
with your SSL certificate path.

.. code-block:: text

    server {
            listen 443 ssl http2;
            listen [::]:443 ssl http2;
            server_name [DOMAIN] [DOMAIN];

            # optional
            access_log /var/log/nginx/[DOMAIN].access.log;
            error_log /var/log/nginx/[DOMAIN].log;

            client_max_body_size 0;
            underscores_in_headers on;

            ssl on;
            ssl_certificate [CERT PATH]; # managed by Certbot
            ssl_certificate_key [CERT PATH]; # managed by Certbot

            ssl_stapling on;
            ssl_stapling_verify on;
            include /etc/nginx/snippets/ssl.conf;


            location / {
                    proxy_headers_hash_max_size 512;
                    proxy_headers_hash_bucket_size 64;
                    proxy_set_header Host $host;
                    proxy_set_header X-Forwarded-Proto $scheme;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    add_header Strict-Transport-Security "max-age=15768000; includeSubDomains;";
                    add_header Front-End-Https on;

                    # whatever the IP of your receipt server server is
                    proxy_pass http://localhost:8721;
            }
    }

    server {
            listen 80;
            listen [::]:80;
            server_name [DOMAIN] [DOMAIN];
            access_log /var/log/nginx/[DOMAIN].access.log;
            error_log /var/log/nginx/[DOMAIN].80.error.log;
            root /usr/share/nginx/html/[DOMAIN]/;

            location ^~ /.well-known/acme-challenge/ {
                allow all;
                default_type "text/plain";
            }
            location ^~ /.well-known/pki-validation/ {
                allow all;
                default_type "text/plain";
            }
            location / {
                return 403;
            }
    }

Don't forget to reload your NGINX server, after.
