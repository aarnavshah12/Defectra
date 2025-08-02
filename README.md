# PCB Defect Inspection Tool

A professional GUI application for automated PCB (Printed Circuit Board) defect detection using Roboflow's computer vision workflows. This tool provides real-time analysis of PCB images to identify defects like spurious copper, shorts, opens, and other manufacturing issues.

![PCB Defect Inspection](https://img.shields.io/badge/PCB-Defect%20Detection-blue) ![Python](https://img.shields.io/badge/Python-3.7+-green) ![Roboflow](https://img.shields.io/badge/Roboflow-Workflow-orange)

## Features

- 🖼️ **Image Processing**: Upload and analyze PCB images in various formats (JPG, PNG, BMP, TIFF)
- 🔍 **Defect Detection**: Automated detection of PCB defects using AI-powered computer vision
- 📊 **Analysis Dashboard**: Real-time display of inspection results and defect statistics
- 📈 **Defect Classification**: Categorization and counting of different defect types
- 💾 **Image Export**: Save annotated images with detection overlays
- 🎨 **Modern UI**: Professional dark-themed interface with responsive design
- 📱 **Responsive Layout**: Automatically adapts to different screen sizes
- 🔄 **Real-time Updates**: Live workflow updates without caching delays

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Required Dependencies

```bash
pip install -r requirements.txt
```

**Or install individually:**
```bash
pip install tkinter
pip install inference-sdk
pip install requests
pip install Pillow
pip install python-dotenv
```

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PCB-Defect-Inspector
   ```

2. **Create environment file:**
   Create a `.env` file in the project root with your Roboflow credentials:
   ```env
   API_KEY=your_roboflow_api_key
   WORKSPACE_NAME=your_workspace_name
   WORKFLOW_ID=your_workflow_id
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Configuration

### Environment Variables

The application uses environment variables for configuration. Create a `.env` file with:

| Variable | Description | Example |
|----------|-------------|---------|
| `API_KEY` | Your Roboflow API key | `BaHgg6pa3Dgv1HknymwA` |
| `WORKSPACE_NAME` | Your Roboflow workspace name | `aarnavs-space` |
| `WORKFLOW_ID` | Your workflow ID | `pcbspace` |

### Roboflow Setup

1. Create a Roboflow account at [roboflow.com](https://roboflow.com)
2. Set up a computer vision workflow for PCB defect detection
3. Train your model with PCB images and defect annotations
4. Deploy the workflow and get your API credentials

## Usage

### Basic Workflow

1. **Launch Application**
   ```bash
   python main.py
   ```

2. **Select Image**
   - Click "Select Image" button
   - Choose a PCB image file from your computer
   - Supported formats: JPG, JPEG, PNG, BMP, TIFF

3. **Process Image**
   - Click "Process Image" button
   - Wait for analysis to complete
   - View results in the interface

4. **Review Results**
   - **Status Panel**: Shows overall inspection result
   - **Analysis Summary**: Displays defect count and primary defect type
   - **Annotated Image**: Visual representation with detection overlays
   - **Detailed Report**: Complete breakdown of all detected defects

### Output Information

The application provides comprehensive analysis including:

- **Inspection Status**: Overall assessment (e.g., "further inspection needed by human")
- **Defect Count**: Total number of defects detected
- **Primary Defect Type**: Most common defect category
- **Class Distribution**: Percentage breakdown by defect type
- **Individual Detections**: Position, size, and confidence for each defect
- **Annotated Image**: Visual overlay showing detected defects

### Export Options

- **Annotated Image**: Automatically saved as `visualization_output.png`
- **Raw Data**: Access to complete JSON response from Roboflow API

## File Structure

```
PCB-Defect-Inspector/
├── main.py                 # Main application file
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── visualization_output.png # Generated annotated images
└── assets/                # Screenshots and documentation
```

## Technical Details

### Architecture

- **Frontend**: Tkinter-based GUI with modern styling
- **Backend**: Roboflow Inference SDK for computer vision processing
- **Image Processing**: PIL/Pillow for image manipulation
- **Configuration**: python-dotenv for environment management

### Supported Defect Types

The application can detect various PCB defects including:
- Spurious copper
- Missing copper
- Shorts and opens
- Component placement issues
- Soldering defects
- Trace width violations

### Performance

- **Response Time**: Typically 2-5 seconds per image
- **Image Size**: Supports high-resolution PCB images
- **Accuracy**: Depends on trained model quality
- **Caching**: Disabled for development (immediate workflow updates)

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd PCB-Defect-Inspector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run in development mode
python main.py
```

### Customization

#### UI Themes
Modify color scheme in `PCBInspectionGUI.__init__()`:
```python
self.bg_color = "#1E2A44"      # Background color
self.accent_color = "#00C4B4"   # Button/accent color
self.secondary_color = "#FF6F61" # Status text color
```

#### Workflow Configuration
Update workflow settings by modifying the `.env` file or the process_image function.

## Troubleshooting

### Common Issues

**Issue: "No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**Issue: "API key not found"**
- Verify `.env` file exists in project root
- Check environment variable names match exactly
- Ensure no extra spaces in `.env` file

**Issue: "Workflow not found"**
- Verify workspace name and workflow ID
- Check Roboflow dashboard for correct values
- Ensure workflow is deployed and active

**Issue: Images not displaying**
- Check image file format compatibility
- Verify sufficient system memory
- Ensure PIL/Pillow is properly installed

### Performance Optimization

- **Reduce image size** for faster processing
- **Enable caching** for production use (set `use_cache=True`)
- **Close other applications** to free up memory
- **Use SSD storage** for faster file access

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Roboflow Docs](https://docs.roboflow.com)
- **Issues**: Create an issue in this repository
- **Community**: [Roboflow Community Forum](https://community.roboflow.com)

## Acknowledgments

- **Roboflow** for providing the computer vision platform
- **Python Community** for excellent libraries and tools
- **Contributors** who helped improve this project

---

**Made with ❤️ for PCB Quality Assurance**

*This tool helps manufacturers ensure PCB quality through automated visual inspection, reducing manual inspection time and improving defect detection accuracy.*
