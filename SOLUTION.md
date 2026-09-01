# Instructor-Only Answer Key

Do not place or link this file from the web app.

## Brute-Forceable Directories

The five common-wordlist directories are:

- `/admin/`
- `/backup/`
- `/config/`
- `/dev/`
- `/test/`

The real branch is under `/config/`.

## Hidden Path Chain

1. `/` contains this source-only comment:

   ```html
   <!-- Follow this -> /f -->
   ```

2. `/f` contains this source-only comment:

   ```html
   <!-- next review path: /f/l -->
   ```

3. `/f/l` contains this source-only comment:

   ```html
   <!-- next review path: /f/l/a -->
   ```

4. `/f/l/a` contains this source-only comment:

   ```html
   <!-- next review path: /f/l/a/g -->
   ```

5. `/f/l/a/g` returns a `302` redirect to `https://youtu.be/dQw4w9WgXcQ`.
6. Brute forcing reveals the five top-level directories listed above.
7. `/config/` visibly links to `/config/env` and `/config/staging`.
8. `/config/staging` contains this source-only comment:

   ```html
   <!-- staging mirror moved: /hidden/ -->
   ```

9. `/hidden/` is the hidden directory.

## Credentials

`/hidden/notes` contains this source-only comment:

```html
<!-- reminder: reset svc_backup password after audit -->
```

Username: `svc_backup`

Password: `password123`

Password difficulty note: `password123` is commonly present in RockYou-derived top-1000 lists. Its exact line number varies by curated list; place it around line 100-200 in the training wordlist if you want a quick classroom crack, or later if you want a longer Hydra run.

## Final Flag

`/hidden/vault` displays:

```text
FLAG{h1dd3n_1n_pl41n_s1ght_9f3a2c}
```
