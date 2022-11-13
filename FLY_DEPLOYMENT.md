# 🌐 Fly.io Deployment

## Deploy

### 🤖 GitHub Actions

GitHub Actions is used to deploy automatically on branch updates to separate Fly.io apps.

See GitHub Actions [workflow files](.github/workflows) for more details.

Depends on the `FLY_API_TOKEN` repository secret.

### 💪 Manually

#### Initial setup and database
1. Install [`flyctl`](https://fly.io/docs/hands-on/install-flyctl/)
2. Create an account with `fly auth signup` or login with `fly auth login`
3. Create PostgreSQL cluster app
    ```
    fly postgres create -n <unique-psql-app-name>
    ```

#### Development app

1. Create fly app
    ```
    fly apps create <unique-dev-app-name>
    ```
2. Connect to the PostgreSQL cluster you created above
    ```
    fly postgres attach --app <unique-dev-app-name> <unique-psql-app-name>
    ```
3. Set the `app` property to `<unique-dev-app-name>` in `fly.dev.toml`
4. Deploy
    ```
    fly deploy -c fly.dev.toml
    ```

#### Production app

1. Create fly app
    ```
    fly apps create <unique-prod-app-name>
    ```
2. Connect to the PostgreSQL cluster you created above
    ```
    fly postgres attach --app <unique-prod-app-name> <unique-psql-app-name>
    ```
3. Set the `app` property to `<unique-prod-app-name>` in `fly.prod.toml`
4. Deploy
    ```
    fly deploy -c fly.prod.toml
    ```

## Database

### 🖥️ Console
A `psql` console can be accessed with
```
fly postgres connect -a <app-name>
```

### 💣️ Delete data

You can use the `TRUNCATE` command from a `psql` console to delete table data. Below is an example to delete all data in "user data" tables.

```
TRUNCATE TABLE "eventParticipation","events","itemOwnerships","items","questDependencies","questItems","questParticipations","quests","users"; 
```

### 🌱 Seed data

#### 1. Proxy connection

In order to pass a local seed file to the deployed database, we must first proxy the database connection to a local port

```
fly proxy 15432:5432 -a <database-app-name>
```
> uses local port `15432`, make sure it's free or use another one

#### 2. (Optional) Delete existing data
Seed data might conflict with existing data, so you might want to delete any existing data.

See [Delete data](#💣️-delete-data)

#### 3. Seed
> requires `psql` installed on local machine

Execute seed command with the local proxy port
```
psql postgres://postgres:<password>@localhost:15432/<database> < maraudersmap/database/seed.sql
```
> `<password>` and `<database>` must be replaced with app-specific Fly.io credentials