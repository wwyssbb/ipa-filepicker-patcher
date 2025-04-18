import os
import re
import plistlib
import argparse
import subprocess

def validate_file(file_path: str, extension: str) -> str:
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File not found: {file_path}")
    if not file_path.endswith(extension):
        raise argparse.ArgumentTypeError(f"File must end with {extension}")
    return file_path

def strip_team_id(app_identifier: str) -> str:
    match = re.match(r'^([A-Z0-9]{10})\.(.+)$', app_identifier)
    return match.group(2) if match else app_identifier

def extract_application_identifier(mobileprovision_path: str) -> str:
    with open(mobileprovision_path, 'rb') as f:
        content = f.read()

    start = content.find(b"<?xml")
    end = content.find(b"</plist>") + len(b"</plist>")

    if start == -1 or end == -1:
        raise ValueError("Invalid mobileprovision file.")

    plist_data = content[start:end]
    plist = plistlib.loads(plist_data)

    entitlements = plist.get('Entitlements', {})
    app_id = entitlements.get('application-identifier')

    if not app_id:
        raise ValueError("No application-identifier found.")

    return strip_team_id(app_id)

def main():
    parser = argparse.ArgumentParser(description="IPA Patcher")

    parser.add_argument(
        "-c", "--certificate",
        type=lambda x: validate_file(x, ".p12"),
        required=True,
        help="Path to the .p12 certificate file"
    )

    parser.add_argument(
        "-m", "--mobileprovision",
        type=lambda x: validate_file(x, ".mobileprovision"),
        required=True,
        help="Path to the .mobileprovision file"
    )

    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Password for the .p12 certificate"
    )

    parser.add_argument(
        "-i", "--ipa",
        type=lambda x: validate_file(x, ".ipa"),
        required=True,
        help="Path to the .ipa file to be patched"
    )

    args = parser.parse_args()

    try:
        original_ipa_name = os.path.splitext(os.path.basename(args.ipa))[0]
        output_ipa = f"{original_ipa_name}_patched.ipa"

        new_bundle_id = extract_application_identifier(args.mobileprovision)
        
        command = [
            "bin\\zsign.exe",
            "-z", "9",
            "-k", args.certificate,
            "-m", args.mobileprovision,
            "-p", args.password,
            "-b", new_bundle_id,
            "-o", output_ipa,
            args.ipa
        ]

        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Successfully patched IPA file as '{output_ipa}'")

    except subprocess.CalledProcessError as e:
        print("Failed to sign IPA file:")
        print(e.stderr)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
