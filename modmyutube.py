import os, subprocess, requests, shutil, logging, sys, platform

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

mods = {
    "ugroupsettings": "https://repo.chariz.com/debs/se6MkXUxm66koz9o1JaFO9-asPWcbbvPDChKjNUe0h9q_m1GULg6ZX0kcQax_uooaI4Bd74EGfEe2ktvLUnprw/com.ps.yougroupsettings_1.0.4_iphoneos-arm64.deb",
    "ytvideooverlay": "https://poomsmart.github.io/repo/debs/youtube/ytvideooverlay/com.ps.ytvideooverlay_2.2.3_iphoneos-arm64.deb",
    "alderis": "https://repo.chariz.com/debs/zaMq1kEPPeYFlPHyTiINjcFsrndIF1iCXdwzLLS35GaYZ_1e5jFYZg4IDNsVETTMkT6ryA8ehztuDTSXh4D82A/ws.hbang.alderis_1.2.3_iphoneos-arm64.deb",
    "youpip": "https://poomsmart.github.io/repo/debs/youtube/youpip/com.ps.youpip_1.12.7_iphoneos-arm64.deb",
    "ytuhd": "https://poomsmart.github.io/repo/debs/youtube/ytuhd/com.ps.ytuhd_1.6.6_iphoneos-arm64.deb",
    "youquality": "https://poomsmart.github.io/repo/debs/youtube/youquality/com.ps.youquality_1.3.6_iphoneos-arm64.deb",
    "ryd": "https://repo.chariz.com/debs/oAwDTPS7Fp2k3tAW-BcqQIzKE2meooC3Sijk0anbWqlHHCareaMsW8g6-UwC7yRgnaXDJ1dEU47HTehn3pyM3w/weeb.lillie.youtubedislikesreturn_1.13.12_iphoneos-arm64.deb",
    "demc": "https://github.com/therealFoxster/DontEatMyContent/releases/download/v1.1.11/me.foxster.donteatmycontent_1.1.11_iphoneos-arm64.deb",
    "isponsorblock": "https://repo.icrazeios.com/debs/com.galacticdev.isponsorblock_1.2.12_iphoneos-arm64.deb"
}

workspace = Path.cwd() / "modmyutube"

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[90m',
        'INFO': '\033[96m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'CRITICAL': '\033[1;91m'
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        msg = super().format(record)
        return f"{color}{msg}{self.RESET}"

handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger("modmyutube")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False

def check_os():
    system = platform.system()
    if system not in ["Linux", "Darwin"]:
        logger.error(f"Unsupported OS: {system}")
        logger.error("This script only works on Linux and macOS")
        sys.exit(1)
    return system

def check_command(cmd):
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies():
    system = check_os()
    
    missing = []
    if not check_command("git"):
        missing.append("git")
    if not check_command("cyan"):
        missing.append("cyan")
    
    if not missing:
        logger.debug("All dependencies are already installed")
        return
    
    logger.info(f"Installing missing dependencies: {', '.join(missing)}")
    
    if "git" in missing:
        logger.debug("Installing git...")
        if system == "Darwin":
            if not check_command("brew"):
                logger.error("Homebrew not found. Install it from https://brew.sh")
                sys.exit(1)
            subprocess.run(["brew", "install", "git"], check=True)
        elif system == "Linux":
            try:
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "git"], check=True)
            except subprocess.CalledProcessError:
                try:
                    subprocess.run(["sudo", "yum", "install", "-y", "git"], check=True)
                except subprocess.CalledProcessError:
                    logger.error("Unable to install git automatically")
                    sys.exit(1)
    
    if "cyan" in missing:
        logger.debug("Installing cyan (pyzule-rw)...")
        
        if check_command("pipx"):
            try:
                subprocess.run([
                    "pipx", "install", "--force",
                    "https://github.com/asdfzxcvbn/pyzule-rw/archive/main.zip"
                ], check=True)
                logger.info("Cyan successfully installed via pipx")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing cyan: {e}")
                sys.exit(1)
        elif check_command("pip3") or check_command("pip"):
            pip_cmd = "pip3" if check_command("pip3") else "pip"
            
            try:
                logger.debug("Installing setuptools...")
                subprocess.run([
                    pip_cmd, "install", "--user", "--break-system-packages", "setuptools"
                ], check=True)
                
                logger.debug("Installing pyzule-rw...")
                subprocess.run([
                    pip_cmd, "install", "--user", "--break-system-packages",
                    "https://github.com/asdfzxcvbn/pyzule-rw/archive/main.zip"
                ], check=True)
                logger.info("Cyan successfully installed via pip")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error installing cyan: {e}")
                sys.exit(1)
        else:
            logger.error("Neither pipx nor pip found. Install Python3 and pip/pipx")
            sys.exit(1)
        
        user_bin = Path.home() / ".local" / "bin"
        if str(user_bin) not in os.environ.get("PATH", ""):
            os.environ["PATH"] = f"{user_bin}:{os.environ.get('PATH', '')}"

def setup_workspace():
    try:
        if workspace.exists():
            logger.debug(msg="Cleaning up...")
            shutil.rmtree(workspace)
        workspace.mkdir()

        for f in Path.cwd().glob("YouTubePlus_*.ipa"):
            f.unlink()
    
    except Exception as e:
        logger.error(e)

def download_mods(enabled_mods):
    try:
        for mod in mods:
            url = mods[mod]
            filename = f"{mod}.deb"
            dest = workspace / filename
            logger.debug(f"Downloading {filename}")
            download_file(url, dest)
    except Exception as e:
        logger.error(e)

def pick_ipa_file():
    try:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select YouTube IPA File",
            filetypes=[("IPA files", "*.ipa")]
        )
        return file_path
    except Exception as e:
        logger.error(e)
        return None

def ask_bool(prompt):
    try:
        ans = input(f"{prompt} (y/n): ").lower()
        return ans == 'y'
    except Exception as e:
        logger.error(e)

def ask_str(prompt, default=""):
    try:
        ans = input(f"{prompt} (default: {default}): ").strip()
        return ans if ans else default
    except Exception as e:
        logger.error(e)

def run_cmd(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, shell=isinstance(cmd, str))
        if result.returncode != 0:
            logger.error(result.stderr.decode(errors='ignore'))
            logger.error(result.stdout.decode(errors='ignore'))
            raise Exception("Command failed")
        return result.stdout.decode()
    except Exception as e:
        logger.error(e)
        raise

def download_file(url, dest):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception(f"Failed to download {url}")
        with open(dest, "wb") as f:
            f.write(r.content)
    except Exception as e:
        logger.error(e)

def copy_file_no_chmod(src, dst):
    try:
        with open(src, "rb") as fsrc:
            with open(dst, "wb") as fdst:
                fdst.write(fsrc.read())
    except Exception as e:
        logger.error(e)

def copy_folder_no_chmod(src, dst):
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        if dst_path.exists():
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)
    except Exception as e:
        logger.error(e)

def git_clone_or_pull(repo_url, dest):
    try:
        dest_path = workspace / dest
        if dest_path.exists():
            logger.debug(f"Pulling updates in {dest}")
            run_cmd("git pull", cwd=dest_path)
        else:
            logger.debug(f"Cloning {repo_url} into {dest}")
            run_cmd(f"git clone --depth=1 {repo_url} {dest}", cwd=workspace)
    except Exception as e:
        logger.error(e)

def fix_makefile(path):
    try:
        makefile_path = Path(path) / "Makefile"
        if makefile_path.exists():
            text = makefile_path.read_text()
            if "include /tweak.mk" in text:
                text = text.replace("include /tweak.mk", "include $(THEOS)/tweak.mk")
                makefile_path.write_text(text)
                logger.debug(f"Fixed Makefile in {path}")
    except Exception as e:
        logger.error(e)

def build_tweak(name, path):
    try:
        logger.debug(f"Building {name}")
        build_path = workspace / path
        fix_makefile(build_path)

        theos_path = "/opt/theos"

        env = os.environ.copy()
        env["THEOS"] = theos_path

        result = subprocess.run(
            "make clean package DEBUG=0 FINALPACKAGE=1",
            cwd=build_path,
            capture_output=True,
            shell=True,
            env=env,
        )
        if result.returncode != 0:
            logger.error(result.stderr.decode(errors='ignore'))
            raise Exception("Command failed")

        deb_files = list((build_path / "packages").glob("*.deb"))
        if not deb_files:
            raise Exception(f"No deb file found for {name}")
        target_deb = workspace / f"{name}.deb"
        deb_files[0].rename(target_deb)
        logger.debug(f"Moved deb to {target_deb}")
    except Exception as e:
        logger.error(e)

def download_safari_extension():
    try:
        ext_url = "https://github.com/CokePokes/YoutubeExtensions.git"
        ext_folder = workspace / "YoutubeExtensions"

        if ext_folder.exists():
            logger.debug("Pulling YoutubeExtensions")
            run_cmd("git pull", cwd=ext_folder)
        else:
            logger.debug("Cloning YoutubeExtensions")
            run_cmd(["git", "clone", "--depth=1", "--quiet", "--depth=1", ext_url, str(ext_folder)])

        appex_path = workspace / "YoutubeExtensions" / "OpenYoutubeSafariExtension.appex"
        target_path = workspace / "OpenYoutubeSafariExtension.appex"
        if appex_path.exists():
            copy_folder_no_chmod(appex_path, target_path)
        else:
            raise Exception("OpenYoutubeSafariExtension.appex not found after cloning!")
    except Exception as e:
        logger.error(e)

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("=== ModMyuTube ===")
    
    system = check_os()
    logger.info(f"Detected operating system: {system}")
    
    install_dependencies()
    
    setup_workspace()

    logger.info("Please select the original YouTube IPA file")
    ipa_path = pick_ipa_file()
    if not ipa_path:
        logger.error("You didn't select any file, bro.")
        return
    logger.debug(f"Copying {ipa_path} to {workspace / 'youtube.ipa'}")
    copy_file_no_chmod(ipa_path, workspace / "youtube.ipa")

    print()
    logger.info("For more info on versions see https://github.com/dayanch96/YTLite/tags")
    tweak_version = ask_str("Tweak version", "5.2b4")
    display_name = ask_str("App name", "YouTube")
    bundle_id = ask_str("Bundle ID", "com.google.ios.youtube")
    print()

    logger.debug("Downloading Safari extension")
    download_safari_extension()

    deb_url = f"https://github.com/dayanch96/YTLite/releases/download/v{tweak_version}/com.dvntm.ytlite_{tweak_version}_iphoneos-arm.deb"
    download_file(deb_url, workspace / "ytplus.deb")

    enabled_mods = list(mods.keys())

    download_mods(enabled_mods)

    tweaks = ["modmyutube/ytplus.deb", "OpenYoutubeSafariExtension.appex"] + [f"{m}.deb" for m in enabled_mods]
    tweaks_str = " modmyutube/".join(tweaks)

    logger.debug("Building IPA file")
    cmd_inject = f"cyan -i modmyutube/youtube.ipa -o YouTubePlus_{tweak_version}.ipa -uwef {tweaks_str} -n \"{display_name}\" -b {bundle_id}"
    try:
        run_cmd(cmd_inject)
    except Exception:
        logger.error("Error creating IPA file")
        return

    output_ipa = Path.cwd() / f"YouTubePlus_{tweak_version}.ipa"
    if not output_ipa.exists():
        logger.error(f"File {output_ipa.name} not found after build")
        return

    print()
    logger.info(f"IPA successfully created: {output_ipa.name}")
    logger.warning('When opening YouTube ignore "Incompatible Tweaks Detected" by selecting "Dont Show for This Version" and "I Accept All Risks".')

if __name__ == "__main__":
    main()
