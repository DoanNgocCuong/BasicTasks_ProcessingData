from flask import Flask
from flask_cors import CORS
from api.scripts import bp as scripts_bp
# from api.files import bp as files_bp  # Comment out this line
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(scripts_bp, url_prefix='/api/scripts')
# app.register_blueprint(files_bp, url_prefix='/api/files')  # Comment out this line too

# Set up scheduler
scheduler = BackgroundScheduler()

def trigger_daily_queries():
    """Trigger both queries via API endpoints"""
    try:
        # Call rating query
        requests.post('http://localhost:5000/api/scripts/run/queryRating_logLarkbase')
        logger.info("Rating query triggered")
        
        # Call workflow query
        requests.post('http://localhost:5000/api/scripts/run/queryRatingToolsWorkflowMindpal_logLarkbase')
        logger.info("Workflow query triggered")
        
    except Exception as e:
        logger.error(f"Error triggering queries: {str(e)}")

# Schedule queries to run at midnight
scheduler.add_job(trigger_daily_queries, 'cron', hour=0, minute=0)
scheduler.start()

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)