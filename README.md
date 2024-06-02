Wersja 0.0.1

Uruchomienie dockera:
=====================
docker-compose up -d


Po pierwszym uruchomieniu dockera należy stworzyć bazę.
=======================================================

W tym celu należy wejść do docker: tag-rest:
===================================
    docker exec -it tags-rest /bin/sh

następnie wejść w konsolę flash:
================================
    flask shell

a następnie wykonać:
====================
    from db import db
    db.create_all()


Mikroserwis obsługujący następujące endpointy:
=============================================

```
openapi: 3.0.3
info:
  title: Tagi
  version: 0.0.1
servers:
  - url: http://127.0.0.1/v1
paths:
  /tags:
    post:
      summary: Dodaje nowy tag
      requestBody:
        content:
          application/json:
            schema:
                $ref: '#/components/schemas/Tag'
        required: true
      responses:
        '200':
          description: Operacja powiodła się
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tag'  
          headers:
              Location:
                schema:
                    type: string
                description: Adres do pobrania obiektu tagu
                example: "http://127.0.0.1/tags/061cb26a-54b8-7a52-8000-2124e7041024"
        '400':
          description: Niepoprawne dane wejściowe.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'  
              example:
                code: "invalid_tag_name"
                type: "https://127.0.0.1/docs/problem-details/invalid_tag_name"
                detail: "Nieprawna nazwa taga. Nazwa musi składać się z jednego lub więcej słów w skład których wchodza jedynie litery i cyfry."
                status: 400
        '405':
          description: Niepoprawny format danych. Oczekiwano application/json.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'  
              example:
                code: "invalid_format"
                type: "https://127.0.0.1/docs/problem-details/invalid_format"
                detail: "Nieprawny format danych. Oczekiwano application/json"
                status: 405
  /tags/{tag_id}:
    get:
      summary: Wyszukuje tag po identyfikatorze
      parameters:
        - name: tag_id
          in: path
          description: Identyfikator taga
          required: true
          schema:
            type: string
            format: uuid7
            example: '061cb26a-54b8-7a52-8000-2124e7041024'
      responses:
        '200':
          description: Poprawnie wykonana operacja
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tag'          
        '400':
          description: Niepoprawione id taga
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'  
              example:
                code: "invalid_tag_id"
                type: "https://127.0.0.1/docs/problem-details/invalid_tag_id"
                detail: "Nieprawny identyfikator taga."
                status: 400
        '404':
          description: Tag nie znaleziony
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'  
              example:
                code: "tag_is_missing"
                type: "https://127.0.0.1/docs/problem-details/tag_is_missing"
                detail: "Tag nie został znaleziony."
                status: 404
    delete:
      summary: Usuwa tag
      parameters:
        - name: tag_id
          in: path
          description: Identyfikator taga do usunięcia
          required: true
          schema:
            type: string
            format: uuid7
            example: '061cb26a-54b8-7a52-8000-2124e7041024'
      responses:
        '204':
          description: Usunięto tag
        '400':
          description: Niepoprawne id taga
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetail'  
              example:
                code: "invalid_tag_id"
                type: "https://127.0.0.1/docs/problem-details/invalid_tag_id"
                detail: "Nieprawny identyfikator taga."
                status: 400
components:
  schemas:
    Tag:
      type: object
      properties:
        id:
          type: string
          format: uuid7
          example: '061cb26a-54b8-7a52-8000-2124e7041024'
          description: Identyfikator taga w formacie uuid7
        name:
          type: string
          example: 'Nowa Huta'
          description: Nazwa taga
    ProblemDetail:  # https://www.rfc-editor.org/rfc/rfc7807
      type: object
      properties:
        code:
          type: string
        type:
          type: string
        title:
          type: string
        detail:
          type: string
        status:
          type: integer
```