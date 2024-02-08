# Cell Rental Service

The project for creation of cell leases by users and reminding them about the end of the lease period.

## Run with Docker

**Docker must already be installed!**

```shell
git clone https://github.com/vitalii-babiienko/tt-cell-rental-service.git
cd tt-cell-rental-service
```

Create a **.env** file by copying the **.env.sample** file and populate it with the required values.

```shell
docker-compose up --build
```

## Run tests

```shell
docker exec -it django_cell_rental_service python manage.py test
```

## Endpoints

* /api/v1/orders/ POST
* /orders/ GET
* /orders/ POST
* /orders/`<slug>`/
