# Flarum tool: import passwords from FluxBB

FluxBB stores passwords in SHA-1, while Flarum stores them using bcrypt.

This tool imports the old passwords into Flarum, using [MigrateToFlarum's Old Passwords extension](https://github.com/migratetoflarum/old-passwords) ([forum thread](https://discuss.flarum.org/d/8631-old-passwords)). **This extension must be installed and enabled before runnng this tool**, else it will fail (missing table column).

Both databases must be MySQL databases. But if you have another database system, it should be easy to update the code to support it.

## How to use

This is a standalone Python script that connect to both the old and the new database and import the passwords. FluxBB uses SHA-1, an insecure hashing method, so this script will re-hash them using bcrypt before saving them into the database. As bcrypt is slow by design, **it can take a long time if you have many users** (15 minutes for 4k users).

First, clone the repository:

```bash
git clone https://github.com/AmauryCarrade/flarum-tool-import-passwords-from-fluxbb.git
cd flarum-tool-import-passwords-from-fluxbb
```

Then copy `.env.example` to `.env` and fill both databases settings. Now, install the few dependencies, run the script, and wait:

```bash
pip install -r requirements.txt
python insert-old-passwords.py
```

If you use `pipenv`, you should run `pipenv install` instead of `pip install`.

You can safely run this tool multiple times, or in an already used forum, as if both old and new passwords are avaliable, both will work.
