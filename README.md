# Bot Template

Welcome to the Bot Template, a project built with Django and Aiogram by **Nodirbek Abduraimov**, designed to be incredibly user-friendly.

## Getting Started

1. **Configure Environment:**
   - Create a `.env` file by copying the provided `.env.dist` file.

2. **Create Super User:**
   - After setting up your models, create a superuser for administrative tasks.

3. **Define Your Functions:**
   - Implement your custom functions in the designated file: [utils/db_api/connector_db.py](utils/db_api/connector_db.py).

## Quick Setup Guide

### 1. Configure Environment

Begin by configuring your environment variables. Duplicate the provided `.env.dist` file and name it `.env`.

### 2. Create Super User

Once your models are in place, establish a superuser account for administrative tasks.

```bash
python manage.py createsuperuser
```

### 3. Define Your Functions

Customize the bot's behavior by adding your own functions in the [connector_db.py](utils/db_api/connector_db.py) file.

## Additional Resources

For more details on Django and Aiogram, refer to their official documentation:

- [Django Documentation](https://docs.djangoproject.com/)
- [Aiogram Documentation](https://docs.aiogram.dev/)

Feel free to explore and expand upon this bot template to suit your specific needs. Happy coding!
