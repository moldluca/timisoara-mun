# Timișoara MUN Website

This repository contains the Flask application that powers the official Timișoara Model United Nations website. The project bundles the public-facing pages, registration flows, and supporting assets used by the conference organizers.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Provide the required environment variables in a `.env` file (see `.env.example` if available) for mail delivery, database configuration, and secret key settings.
3. Run the development server:
   ```bash
   flask --app app run --debug
   ```

## Managing Media Assets

GitHub enforces a hard 100&nbsp;MB limit for individual files. To keep the repository pushable:

- Compress videos to web-friendly formats (H.264/H.265) and target sizes well below 100&nbsp;MB before committing.
- Store raw/original video exports outside the repository (e.g., in `static/vid/raw/`, which remains untracked) or in a dedicated cloud bucket.
- Consider breaking long footage into shorter clips or hosting it on a streaming platform and embedding it instead of storing the master file in `static/`.

Remember to keep the optimized versions required for the site in `static/vid/`, and ensure they remain under the size limit to avoid push rejections.

## Deployment Notes

The application can be deployed behind a production web server such as Gunicorn + Nginx or on a PaaS platform that supports Flask. When deploying manually:

- Configure environment variables via systemd service files or platform-specific settings.
- Run database migrations or seed scripts as needed before switching traffic.
- Use HTTPS and a modern TLS configuration for any login or registration flows.

## Contributing

Before opening a pull request:

- Run automated tests (if available) and lint the codebase.
- Ensure that static assets are optimized and free of oversized binaries.
- Describe the changes and include any relevant screenshots for UI updates.
