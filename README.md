# ModMyuTube
This script allows you to apply mods to an original YouTube IPA file.

**Made by** [Kleo08s](https://github.com/Kleo08s) • **Improved by** [ddevid_.1](https://github.com/dddevid)

> [!WARNING]  
> For legal reasons we do **not** provide the original YouTube IPA, you should search for it by yourself. Without the IPA you can't use this script.

## How does it work?
> [!NOTE]  
> This script uses [YTLite](https://github.com/dayanch96/YTLite) as main mod. Credits of the other mods are included below. Give the repo a star, it's really cool.

The script decompresses the original YouTube IPA file, applies the mods, and then recompresses it into a new IPA file using the `cyan` tool.

## Supported Operating Systems
- ✅ Linux
- ✅ macOS
- ❌ Windows (not supported)

> [!WARNING]  
> Windows is **not supported**. If you want to use the script on Windows you should install WSL (Windows Subsystem for Linux) and run the script from there.

## Requirements
The script automatically installs missing dependencies on first run. Required dependencies include:
- `git`: Version control system
- `cyan` (pyzule-rw): Tool used to compress the modified files back into an IPA file
- `requests`: Python library used to download the mods
- `tkinter`: Python library used to select the IPA using a GUI

## Installation

### Quick Start
1. Clone this repository:
```bash
git clone https://github.com/yourusername/ModMyuTube.git
cd ModMyuTube
```

2. Install Python requirements:
```bash
pip install requests
```

3. Run the script:
```bash
python3 modmyutube.py
```

The script will automatically detect your operating system and install any missing dependencies (git, cyan) on first run.

### Manual Installation (Optional)

If you prefer to install dependencies manually:

#### Linux
```bash
sudo apt update
sudo apt install git python3-pip python3-tk
pip install requests
```

#### macOS
```bash
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install git python3
pip3 install requests
```

## Usage
1. Run the script:
```bash
python3 modmyutube.py
```

2. Select your original YouTube IPA file when prompted

3. Configure the following options:
   - Tweak version (default: 5.2b4)
   - App name (default: YouTube)
   - Bundle ID (default: com.google.ios.youtube)

4. Wait for the script to download mods and build the modified IPA

5. The final IPA will be saved as `YouTubePlus_<version>.ipa` in your current directory

> [!NOTE]  
> When opening YouTube for the first time, you may see "Incompatible Tweaks Detected". Select "Don't Show for This Version" and "I Accept All Risks" to proceed.

## Included mods
<details>
<summary>YouPiP</summary>
<p>YouPiP is a tweak developed by <a href="https://github.com/PoomSmart">PoomSmart</a> that enables the native Picture-in-Picture feature for videos in the iOS YouTube app.</p>
<p>Source code and additional information are available <a href="https://github.com/PoomSmart/YouPiP">in its GitHub repository</a>.</p>
</details>

<details>
<summary>YTUHD</summary>
<p>YTUHD is a tweak developed by <a href="https://github.com/PoomSmart">PoomSmart</a> that unlocks 1440p (2K) and 2160p (4K) resolutions in the iOS YouTube app.</p>
<p>Source code and additional information are available <a href="https://github.com/PoomSmart/YTUHD">in PoomSmart's GitHub repository</a>.</p>
</details>

<details>
<summary>Return YouTube Dislikes</summary>
<p>Return YouTube Dislikes is a tweak developed by <a href="https://github.com/PoomSmart">PoomSmart</a> that brings back dislikes on the YouTube app.</p>
<p>Source code and additional information are available <a href="https://github.com/PoomSmart/Return-YouTube-Dislikes">in PoomSmart's GitHub repository</a>.</p>
</details>

<details>
<summary>YouQuality</summary>
<p>YouQuality is a tweak developed by <a href="https://github.com/PoomSmart">PoomSmart</a> that allows to view and change video quality directly from the video overlay.</p>
<p>Source code and additional information are available <a href="https://github.com/PoomSmart/YouQuality">in PoomSmart's GitHub repository</a>.</p>
</details>

<details>
<summary>DontEatMyContent</summary>
<p>DontEatMyContent is a tweak developed by <a href="https://github.com/therealFoxster">therealFoxster</a> that prevents the Notch/Dynamic Island from munching on 2:1 video content in the iOS YouTube app.</p>
<p>Source code and additional information are available <a href="https://github.com/therealFoxster/DontEatMyContent">in therealFoxster's GitHub repository</a>.</p>
</details>

<details>
<summary>iSponsorBlock</summary>
<p>iSponsorBlock is a tweak developed by <a href="https://github.com/Galactic-Dev">Galactic-Dev</a> that lets you block sponsors and other segments in videos.</p>
<p>Source code and additional information are available <a href="https://github.com/Galactic-Dev/iSponsorBlock">in Galactic-Dev's GitHub repository</a>.</p>
</details>

## Troubleshooting

### Dependencies not installing automatically
If automatic dependency installation fails, install them manually:
- **Linux**: `sudo apt install git python3-pip && pip3 install --user --break-system-packages setuptools`
- **macOS**: `brew install git python3`

### cyan command not found
The script automatically adds `~/.local/bin` to PATH during runtime. If issues persist, add it permanently:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### IPA not being created
Check the error output from cyan. Common issues:
- Corrupted original IPA file
- Insufficient disk space
- Missing dependencies

## Credits
- [YTLite](https://github.com/dayanch96/YTLite) - Main tweak by dayanch96
- [Cyan](https://github.com/asdfzxcvbn/pyzule-rw) - IPA patching tool
- All mod developers mentioned in the "Included mods" section

## License
This project is for educational purposes only. Respect the licenses of all included projects and mods.
