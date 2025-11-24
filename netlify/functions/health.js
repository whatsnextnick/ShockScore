/**
 * Netlify Function: Health Check
 *
 * Simple health check endpoint to verify the API is running
 */

exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      status: 'operational',
      service: 'Shock Score API',
      version: '1.0.0',
      platform: 'netlify',
      timestamp: new Date().toISOString()
    })
  };
};
