/**
 * Python Bridge Service
 *
 * Interfaces with the Python Shock Score engine to process videos
 * and return emotion analytics data.
 */

const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs').promises;

class PythonBridgeService {
  constructor() {
    this.pythonPath = process.env.PYTHON_PATH || path.join(__dirname, '../../venv/bin/python');
    this.scriptPath = process.env.PYTHON_SCRIPT_PATH || path.join(__dirname, '../../shock_score_engine.py');
  }

  /**
   * Process a video file through the Shock Score engine
   *
   * @param {string} videoPath - Absolute path to video file
   * @param {string} outputPath - Path for JSON output
   * @param {Function} progressCallback - Called with progress updates
   * @returns {Promise<object>} - Shock Score report data
   */
  async processVideo(videoPath, outputPath, progressCallback = null) {
    return new Promise((resolve, reject) => {
      const options = {
        mode: 'text',
        pythonPath: this.pythonPath,
        pythonOptions: ['-u'], // Unbuffered output
        scriptPath: path.dirname(this.scriptPath),
        args: [
          '--input', videoPath,
          '--output', outputPath,
          '--no-display' // Headless mode
        ]
      };

      const pyshell = new PythonShell(path.basename(this.scriptPath), options);

      // Capture real-time output
      pyshell.on('message', (message) => {
        console.log('Python:', message);

        // Parse progress updates
        if (message.includes('Progress:')) {
          const match = message.match(/Progress: ([\d.]+)%/);
          if (match && progressCallback) {
            progressCallback({
              type: 'progress',
              percent: parseFloat(match[1])
            });
          }
        }

        // Parse frame updates
        if (message.includes('Frame:')) {
          const match = message.match(/Frame: (\d+)/);
          if (match && progressCallback) {
            progressCallback({
              type: 'frame',
              frame: parseInt(match[1])
            });
          }
        }
      });

      // Handle errors
      pyshell.on('error', (err) => {
        console.error('Python error:', err);
        reject(new Error(`Python processing failed: ${err.message}`));
      });

      // Handle completion
      pyshell.end(async (err, code, signal) => {
        if (err) {
          reject(new Error(`Python script error: ${err.message}`));
          return;
        }

        try {
          // Read the generated JSON report
          const reportData = await fs.readFile(outputPath, 'utf8');
          const report = JSON.parse(reportData);

          resolve({
            success: true,
            report,
            outputPath
          });
        } catch (readErr) {
          reject(new Error(`Failed to read output: ${readErr.message}`));
        }
      });
    });
  }

  /**
   * Test if Python environment is correctly configured
   *
   * @returns {Promise<boolean>}
   */
  async testPythonEnvironment() {
    try {
      const options = {
        mode: 'text',
        pythonPath: this.pythonPath,
        args: ['--version']
      };

      const results = await PythonShell.run('python', options);
      console.log('Python environment test:', results);
      return true;
    } catch (err) {
      console.error('Python environment test failed:', err);
      return false;
    }
  }

  /**
   * Get Shock Score component status
   *
   * @returns {Promise<object>}
   */
  async getComponentStatus() {
    try {
      const options = {
        mode: 'json',
        pythonPath: this.pythonPath,
        scriptPath: path.dirname(this.scriptPath),
        args: []
      };

      // Run simple test
      const script = path.join(__dirname, '../../simple_test.py');
      const results = await PythonShell.run(script, options);

      return {
        available: true,
        components: {
          faceDetector: true,
          emotionAnalyzer: true,
          shockCalculator: true,
          anonymizer: true
        }
      };
    } catch (err) {
      return {
        available: false,
        error: err.message
      };
    }
  }
}

module.exports = new PythonBridgeService();
