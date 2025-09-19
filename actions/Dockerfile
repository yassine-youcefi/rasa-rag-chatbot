FROM rasa/rasa-sdk:3.6.2

WORKDIR /app

USER root

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy actions code
COPY . /app/

USER 1001

EXPOSE 5055

CMD ["start", "--actions", "actions"]