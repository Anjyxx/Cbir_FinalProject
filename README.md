# Housing Website with CBIR (Content-Based Image Retrieval)

A real estate website featuring image-based search powered by ResNet-18 for content-based image retrieval.

## Features

- Property listings with detailed views
- Content-Based Image Retrieval (CBIR) using ResNet-18
- Admin dashboard for property management
- User authentication and authorization
- Responsive design

## Prerequisites

- Python 3.9+
- MySQL/PostgreSQL database
- Git
- Railway CLI (for deployment)

## Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd housing-website
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the database and other settings in `.env`

5. **Initialize the database**
   - Set up a MySQL/PostgreSQL database
   - Run the database initialization script:
     ```bash
     python setup_database.py
     ```

6. **Run the application**
   ```bash
   python app.py
   ```

## Deployment to Railway

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Create a new Railway project**
   ```bash
   railway init
   ```

4. **Add a database**
   - Go to your Railway dashboard
   - Click "New" and select "Database"
   - Choose PostgreSQL
   - Note the connection URL

5. **Set environment variables**
   - In your Railway project settings, go to the "Variables" tab
   - Add all variables from your `.env` file
   - Update the `DATABASE_URL` with your PostgreSQL connection string

6. **Deploy your application**
   ```bash
   git push railway main
   ```

7. **Set up storage for uploads**
   - Railway provides ephemeral storage, so consider using a service like AWS S3 or Cloudinary for file uploads in production

## Project Structure

- `app.py` - Main application file
- `cbir_search.py` - CBIR implementation using ResNet-18
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
  - `uploads/` - Uploaded property images
  - `features/` - Extracted image features for CBIR
- `migrations/` - Database migration scripts

## License

This project is licensed under the MIT License.
