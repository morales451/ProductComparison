#!/usr/bin/env python3
"""
RoofSpec Matcher - Interactive Deployment Helper

This script helps you deploy your app step-by-step.
Just run: python deploy_helper.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def ask_yes_no(question):
    """Ask a yes/no question."""
    while True:
        response = input(f"{Colors.OKBLUE}{question} (y/n): {Colors.ENDC}").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please answer 'y' or 'n'")

def check_python_version():
    """Check if Python version is 3.10+."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version.major}.{version.minor} detected")
        return True
    else:
        print_error(f"Python 3.10+ required. You have {version.major}.{version.minor}")
        return False

def check_venv_exists():
    """Check if virtual environment exists."""
    if Path("venv").exists():
        print_success("Virtual environment found")
        return True
    else:
        print_warning("Virtual environment not found")
        return False

def check_env_file():
    """Check if .env file exists and has API key."""
    env_path = Path(".env")

    if not env_path.exists():
        print_warning(".env file not found")
        return False

    # Read .env file
    with open(env_path) as f:
        content = f.read()

    # Check if API key is set
    has_openai = "OPENAI_API_KEY=sk-" in content
    has_anthropic = "ANTHROPIC_API_KEY=sk-ant-" in content

    if has_openai or has_anthropic:
        print_success(".env file configured with API key")
        return True
    else:
        print_warning(".env file exists but no API key configured")
        return False

def setup_local_environment():
    """Setup local development environment."""
    print_header("🔧 Setting Up Local Environment")

    # Check if setup script exists
    is_windows = platform.system() == "Windows"
    setup_script = "setup.bat" if is_windows else "setup.sh"

    if not Path(setup_script).exists():
        print_error(f"Setup script {setup_script} not found!")
        return False

    # Run setup script
    print_info(f"Running {setup_script}...")

    try:
        if is_windows:
            subprocess.run([setup_script], shell=True, check=True)
        else:
            subprocess.run(["bash", setup_script], check=True)

        print_success("Setup completed!")
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Setup failed: {e}")
        return False

def configure_api_key():
    """Guide user through API key configuration."""
    print_header("🔑 API Key Configuration")

    print_info("You need an API key from OpenAI or Anthropic.")
    print("\nOption 1: OpenAI (Recommended)")
    print("  1. Go to: https://platform.openai.com/api-keys")
    print("  2. Create new secret key")
    print("  3. Copy the key (starts with 'sk-proj-')")
    print("  4. Add $5-10 credit at: https://platform.openai.com/billing")

    print("\nOption 2: Anthropic/Claude")
    print("  1. Go to: https://console.anthropic.com/settings/keys")
    print("  2. Create key")
    print("  3. Copy the key (starts with 'sk-ant-')")
    print("  4. Add credits in billing section")

    print("\n")

    if not ask_yes_no("Have you obtained an API key?"):
        print_info("Please get an API key first, then run this script again.")
        return False

    # Ask which provider
    print("\n")
    provider = input(f"{Colors.OKBLUE}Which provider? (openai/anthropic): {Colors.ENDC}").lower().strip()

    if provider not in ['openai', 'anthropic']:
        print_error("Please choose 'openai' or 'anthropic'")
        return False

    # Ask for API key
    print("\n")
    api_key = input(f"{Colors.OKBLUE}Paste your API key: {Colors.ENDC}").strip()

    if not api_key:
        print_error("No API key provided")
        return False

    # Validate key format
    if provider == 'openai' and not api_key.startswith('sk-'):
        print_warning("OpenAI keys usually start with 'sk-proj-' or 'sk-'")
        if not ask_yes_no("Continue anyway?"):
            return False

    if provider == 'anthropic' and not api_key.startswith('sk-ant-'):
        print_warning("Anthropic keys usually start with 'sk-ant-'")
        if not ask_yes_no("Continue anyway?"):
            return False

    # Write to .env file
    try:
        # Read existing .env or use template
        if Path(".env").exists():
            with open(".env") as f:
                lines = f.readlines()
        else:
            with open(".env.example") as f:
                lines = f.readlines()

        # Update the appropriate line
        new_lines = []
        for line in lines:
            if provider == 'openai' and line.startswith('OPENAI_API_KEY='):
                new_lines.append(f'OPENAI_API_KEY={api_key}\n')
            elif provider == 'anthropic' and line.startswith('ANTHROPIC_API_KEY='):
                new_lines.append(f'ANTHROPIC_API_KEY={api_key}\n')
            else:
                new_lines.append(line)

        # Write back
        with open(".env", 'w') as f:
            f.writelines(new_lines)

        print_success("API key saved to .env file!")
        return True

    except Exception as e:
        print_error(f"Failed to write .env file: {e}")
        return False

def run_local_app():
    """Run the app locally."""
    print_header("🚀 Running App Locally")

    is_windows = platform.system() == "Windows"

    print_info("Starting Streamlit app...")
    print_warning("Press Ctrl+C to stop the app when done testing\n")

    try:
        if is_windows:
            # Windows activation
            activate_cmd = "venv\\Scripts\\activate.bat && streamlit run app.py"
            subprocess.run(activate_cmd, shell=True)
        else:
            # Unix activation
            activate_cmd = "source venv/bin/activate && streamlit run app.py"
            subprocess.run(activate_cmd, shell=True, executable="/bin/bash")

    except KeyboardInterrupt:
        print_success("\nApp stopped.")
        return True
    except Exception as e:
        print_error(f"Failed to start app: {e}")
        return False

def show_streamlit_cloud_instructions():
    """Show instructions for Streamlit Cloud deployment."""
    print_header("☁️ Deploy to Streamlit Cloud")

    print("""
Follow these steps to deploy online:

1. Go to: https://share.streamlit.io/signup

2. Click "Continue with GitHub"

3. Click "New app" button

4. Fill in the form:
   - Repository: morales451/ProductComparison
   - Branch: claude/roofspec-matcher-app-8uuvR
   - Main file path: app.py

5. Click "Advanced settings"

6. In the "Secrets" section, paste your API key:

   For OpenAI:
   OPENAI_API_KEY = "your-key-here"

   For Anthropic:
   ANTHROPIC_API_KEY = "your-key-here"

7. Click "Deploy!"

8. Wait 2-3 minutes for deployment

9. Your app will be live at:
   https://[your-name].streamlit.app

That's it! 🎉
""")

    input(f"\n{Colors.OKBLUE}Press Enter when you've completed deployment...{Colors.ENDC}")
    print_success("Great! Your app should be live now!")

def main():
    """Main interactive deployment helper."""
    print(f"""
{Colors.HEADER}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           RoofSpec Matcher Deployment Helper             ║
║                                                           ║
║              Making deployment stupid-proof!              ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}
""")

    # Check Python version
    if not check_python_version():
        print_error("Please install Python 3.10 or higher")
        sys.exit(1)

    print_header("📋 Deployment Options")
    print("1. Test locally first (recommended for beginners)")
    print("2. Deploy to internet directly (faster)")
    print("3. Exit")

    choice = input(f"\n{Colors.OKBLUE}Choose an option (1-3): {Colors.ENDC}").strip()

    if choice == "3":
        print_info("Goodbye!")
        sys.exit(0)

    if choice == "1":
        # Local deployment path
        print_header("🏠 Local Testing Path")

        # Check if venv exists
        if not check_venv_exists():
            print_info("We need to set up your environment first.")
            if ask_yes_no("Run setup automatically?"):
                if not setup_local_environment():
                    print_error("Setup failed. Please check the errors above.")
                    sys.exit(1)
            else:
                print_info(f"Run setup manually: bash setup.sh (or setup.bat on Windows)")
                sys.exit(0)

        # Check API key
        if not check_env_file():
            print_info("We need to configure your API key.")
            if ask_yes_no("Configure API key now?"):
                if not configure_api_key():
                    print_error("API key configuration failed.")
                    sys.exit(1)
            else:
                print_info("Please configure your API key in the .env file manually.")
                sys.exit(0)

        # Run local app
        print_info("\nEverything is set up!")
        if ask_yes_no("Start the app now?"):
            run_local_app()

        # After testing, ask about cloud deployment
        print("\n")
        if ask_yes_no("Would you like to deploy to the internet now?"):
            show_streamlit_cloud_instructions()
        else:
            print_info("You can deploy later by running: python deploy_helper.py")

    elif choice == "2":
        # Direct cloud deployment
        print_header("☁️ Direct Cloud Deployment")

        # Check if API key is configured
        if not check_env_file():
            print_warning("You'll need an API key for deployment.")
            print_info("If you don't have one yet, follow the instructions in the next step.")

        show_streamlit_cloud_instructions()

    else:
        print_error("Invalid choice. Please run the script again.")
        sys.exit(1)

    print_header("🎉 All Done!")
    print_success("Your RoofSpec Matcher is ready to use!")
    print_info("\nFor more help, check:")
    print("  - START_HERE.md - Complete beginner guide")
    print("  - README.md - Detailed documentation")
    print("  - DEPLOYMENT.md - Advanced deployment options")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Interrupted by user. Goodbye!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
