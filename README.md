# MOV to MP4 Converter

A simple, user-friendly desktop application for converting MOV video files to MP4 format using FFmpeg.


## Features

- Convert single MOV files or entire directories of MOV files
- Custom output directory selection
- Video codec options: H.264 or HEVC (H.265)
- Quality presets: Low, Medium, High
- Progress tracking with status updates
- Multi-language support (Turkish UI)

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)
- FFmpeg must be installed and accessible in your system PATH

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/mov-to-mp4-converter.git
cd mov-to-mp4-converter
```

2. Install FFmpeg if you don't have it already:

   - **Windows**: 
     - Download from [FFmpeg official website](https://ffmpeg.org/download.html)
     - Add FFmpeg to your system PATH

   - **macOS** (using Homebrew):
     ```bash
     brew install ffmpeg
     ```

   - **Linux**:
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```

3. Run the application:
```bash
python mov_to_mp4_converter.py
```

## Usage

1. Launch the application
2. Select a MOV file or a folder containing MOV files
3. (Optional) Choose an output folder (defaults to the same directory as input)
4. Select your preferred video codec and quality settings
5. Click "Dönüştür" (Convert) to start the conversion process
6. Monitor progress and conversion status in the application

## How It Works

The application uses FFmpeg (a powerful multimedia processing tool) to convert MOV files to MP4 format. The conversion process maintains high quality while providing various customization options:

- **H.264 Codec**: Standard video compression, widely compatible
- **HEVC (H.265) Codec**: More efficient compression, smaller file sizes with similar quality
- **Quality Settings**: Adjust compression rate for balancing file size and quality


## License

This project is licensed under the MIT License - see the LICENSE file for details.
