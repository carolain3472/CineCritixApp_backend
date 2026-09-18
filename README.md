# CineCritix — API

Django REST backend for a film and series review platform: catalogue, ratings,
comments and favourites, with a native Android client.

## Data model

The catalogue splits films and series into separate apps, because a series needs
seasons and a film does not, and collapsing the two into one polymorphic model
costs more than it saves.

| App | Models |
|---|---|
| `users_cinecritix` | `CustomUser`, `Actor`, `Genero`, `ExtendToken` |
| `modulo_peliculas_cinecritix` | `Pelicula`, `Puntuacion_pelicula`, `Favorito_pelicula`, `Comentarios_pelicula` |
| `modulo_series_cinecritix` | `Serie`, `Temporada`, `Puntuacion_serie`, `Favorito_serie`, `Comentarios_serie` |

`Actor` and `Genero` are shared across both through many-to-many relations, so an
actor's page can list their films and their series from the same record.

### Account lifecycle

More thought went into accounts than the usual register/login pair:

- `ExtendToken` carries an attempt counter, so a password-reset token can be
  rate-limited rather than just expired
- `darme-de-baja/` deactivates an account and stamps `deactivated_timestamp`,
  keeping the user's comments and ratings intact instead of cascading them away
- `validate_token/`, `update_contra/` and `quitar-profile/` round out the flows
  that a "forgot my password" path actually needs

Profile images and season artwork are stored in Google Cloud Storage.

## Endpoints

Grouped under `users/`, `peliculas/` and `series/`. Browsable documentation at
`/docs/`.

## Running it

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python manage.py migrate
python manage.py runserver
```

`.env.example` lists every variable, including the path to a Google Cloud service
account JSON that lives outside the repository.

## Android client

[CineCritixApp](https://github.com/carolain3472/CineCritixApp) — Kotlin, Jetpack
Compose, with unit and UI tests.

## Known limitations

- No automated tests on the API side, unlike the Android client
- `Pelicula.titulo_pelicula` is unique and capped at 30 characters, which rejects
  legitimate titles and forbids two films sharing a name
- Ratings and comments have no moderation path
- Media URLs were committed as long-expired pre-signed links rather than being
  generated at request time
