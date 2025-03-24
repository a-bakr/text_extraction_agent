# Text Extraction Agent

A Streamlit application that helps you extract and analyze text from images using advanced AI technology.

## Features

- Upload custom images or use demo examples
- Extract text from images
- Analyze extracted text based on custom prompts
- Modern and intuitive user interface

## Deployment to Vercel

1. Install the Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy the application:
```bash
vercel
```

4. Set up environment variables in Vercel:
   - Go to your project settings in Vercel
   - Add the following environment variables:
     - `OPENAI_API_KEY`
     - Any other API keys required by your application

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_api_key_here
```

## License

MIT
